import math
from typing import *

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch import einsum, nn
import random


class MeanMaxPooling(nn.Module):
    """
    [B, S, E] -> [B, 2*E]
    """
    def __init__(self, axis=1, dropout=0.0):
        super().__init__()
        self.axis = axis
        self.dropout = nn.Dropout(p=dropout)

    def forward(self, inputs, valid_length=None):
        """
        :param inputs: Tensor, shape [batch_size, seq_len, embedding_dim]
        :param valid_length: None or Tensor, valid len of token in the sequence with shape [batch_size]
        :return: Tensor, shape [batch_size, 2 * embedding_dim]
        """
        # TODO: broadcast indexing to mean over first vl
        mean_out = torch.mean(inputs, dim=self.axis) if valid_length is None \
            else torch.sum(inputs, dim=self.axis) / valid_length.add(1E-7).unsqueeze(1)
        max_out = torch.max(inputs, dim=self.axis).values
        outputs = torch.cat((mean_out, max_out), dim=1)
        outputs = self.dropout(outputs)
        return outputs


class MeanMaxPoolingMasked(nn.Module):
    """
    [B, S, E] -> [B, 2*E]
    """

    def __init__(self, axis=1, dropout=0.0):
        super().__init__()
        self.axis = axis
        self.dropout = nn.Dropout(p=dropout)

    def forward(self, inputs, src_key_padding_mask=None):
        """
        :param inputs: Tensor, shape [batch_size, seq_len, embedding_dim]
        :param valid_length: None or Tensor, valid len of token in the sequence with shape [batch_size]
        :return: Tensor, shape [batch_size, 2 * embedding_dim]
        """
        if src_key_padding_mask is not None:
            mask = 1 - src_key_padding_mask.int()
            mean_sum = torch.sum(inputs * mask.unsqueeze(-1), dim=self.axis)
            mean_count = torch.sum(mask, dim=self.axis, keepdim=True)
            mean_out = mean_sum / mean_count.clamp(min=1)
        else:
            mean_out = torch.mean(inputs, dim=self.axis)
        max_out = torch.max(inputs, dim=self.axis).values
        outputs = torch.cat((mean_out, max_out), dim=1)
        outputs = self.dropout(outputs)

        return outputs


class Whitening:
    def __init__(self, vecs, n_components=248):
        super().__init__()
        self.vecs = vecs
        self.n_components = n_components
    
    def compute_kernel_bias(self, axis=0, keepdims=True):
        mu = self.vecs.mean(axis=axis, keepdims=keepdims)
        cov = np.cov(self.vecs.T)
        u, s, vh = np.linalg.svd(cov)
        W = np.dot(u, np.diag(1 / np.sqrt(s)))
        return W[:, :self.n_components], -mu

    def transform_and_normalize(self, kernel=None, bias=None):
        if not (kernel is None or bias is None):
            vecs = (self.vecs + bias).dot(kernel)
        return vecs / (self.vecs**2).sum(axis=1, keepdims=True)**0.5
    

class SwiGLU(nn.Module):
    """
    Swish + GLU (SwiGLU) activation function used for Multilayer perceptron(MLP) intermediate activations in transformers.
    classic Noam Shazeer paper, except here they use SwiGLU instead of the more popular GEGLU for gating the feedforward
    https://arxiv.org/abs/2002.05202
    """
    def forward(self, x):
        """
        takes in x input data and returns swiglu

        Args :
            x : input data
        Return : 
                SwiGLU applied activated output
        """
        x, gate = x.chunk(2, dim=-1)
        return F.silu(gate) * x
    
    
class LayerNorm(nn.Module):
    """
    Applies Layer Normalization for last certain number of dimensions.

    Args :
        dim : Dimension of input
    """
    def __init__(self, dim):
        super().__init__()
        self.gamma = nn.Parameter(torch.ones(dim))
        self.register_buffer("beta", torch.zeros(dim))

    def forward(self, x):
        """
        takes input data x and applies layer normalization

        Args :
            x : input data

        Return :
            The layer normalized values for the input data using gamma and beta init parameters.
        """
        return F.layer_norm(x, x.shape[-1:], self.gamma, self.beta)


class Residual(nn.Module):
    """
    Residual networks

    Args :
        fn : function
    """
    def __init__(self, fn):
        super().__init__()
        self.fn = fn

    def forward(self, x, vl):
        """
        takes in x (input data) ,vl (values) and return residual values

        Args :
            x : input data
            vl : valid length to be used, Tensor, shape [batch_size]

        Return : 
            residual value after applying to a function
        """
        x_out= self.fn(x, vl)
        x_out += x
        return x_out


class ResidualTransformerEncoderLayer(nn.Module):
    """
    Residual networks

    Args :
        fn : function
    """

    def __init__(self, fn):
        super().__init__()
        self.fn = fn

    def forward(self, x, src_mask=None, src_key_padding_mask=None):
        """
        Residual connection for TransformerEncoderLayer

        Args :
            x : input data
            src_mask : attention mask
            src_key_padding_mask: sequence padding mask

        Return :
            residual value after applying to a function
        """
        x_out = self.fn(x, src_mask=src_mask, src_key_padding_mask=src_key_padding_mask)
        x_out += x
        return x_out

    
class RotaryEmbedding(nn.Module):
    """
    Rotatory positional (RoPE) embeddings, paper -  https://arxiv.org/abs/2104.09864.
    RoPE encodes the absolute position with a rotation matrix and meanwhile incorporates the explicit relative position dependency in self-attention formulation

    Args :
        dim : dimensions
    """
    def __init__(self, dim):
        super().__init__()
        inv_freq = 1.0 / (10000 ** (torch.arange(0, dim, 2).float() / dim))
        self.register_buffer("inv_freq", inv_freq)

    def forward(self, max_seq_len, *, device):
        """
        takes in max_seq_len, *, device as input and return embeddings

        Args :
            max_seq_len : input data
            * :
            device : device to be used, cpu or gpu

        Return : 
            embeddings
        """
        seq = torch.arange(max_seq_len, device=device, dtype=self.inv_freq.dtype)
        freqs = einsum("i , j -> i j", seq, self.inv_freq)
        return torch.cat((freqs, freqs), dim=-1)


class PositionalEncoding(nn.Module):
    """
    PositionalEncoding module injects some information about the relative or absolute position of the tokens in the sequence. 
    The positional encodings have the same dimension as the embeddings so that the two can be summed

    Args :
        d_model: dimension of token embedding
        max_len: max length of sequence
        dropout: dropout field for regularization
    """
    def __init__(self, d_model, max_len=5000, dropout=0.1):
        super().__init__()
        self.dropout = nn.Dropout(p=dropout)

        position = torch.arange(max_len).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2) * (-math.log(10000.0) / d_model))
        pe = torch.zeros(1, max_len, d_model)
        pe[0, :, 0::2] = torch.sin(position * div_term)
        pe[0, :, 1::2] = torch.cos(position * div_term)
        self.register_buffer('pe', pe)

    def forward(self, x):
        """
        Takes in the input value and add the positional value, apply the dropout on top of it and then return the final value.

        Args :
            x: input data

        Return :
            output of positional encoding

        Shape :
            x: [batch_size, seq_len, embedding_dim]
            
            out : [batch_size, seq_len, embedding_dim]

        """
        x = x + self.pe[:, :x.size(1), :]
        return self.dropout(x)
    
    
class AutomaticWeightedLoss(nn.Module):
    """automatically weighted multi-task loss
    Params：
        num: int，the number of loss
        x: multi-task loss
    Examples：
        loss1=1
        loss2=2
        awl = AutomaticWeightedLoss(2)
        loss_sum = awl(loss1, loss2)
    """
    def __init__(self, num=2):
        super(AutomaticWeightedLoss, self).__init__()
        params = torch.ones(num, requires_grad=True)
        self.params = torch.nn.Parameter(params)

    def forward(self, *x):
        loss_sum = 0
        for i, loss in enumerate(x):
            loss_sum += 0.5 / (self.params[i] ** 2) * loss + torch.log(1 + self.params[i] ** 2)
        return loss_sum

    
class FocalLoss(nn.Module):
    r"""Criterion that computes Focal loss.

    According to [1], the Focal loss is computed as follows:

    .. math::

        \text{FL}(p_t) = -\alpha_t (1 - p_t)^{\gamma} \, \text{log}(p_t)

    where:
       - :math:`p_t` is the model's estimated probability for each class.


    Arguments:
        alpha (float): Weighting factor :math:`\alpha \in [0, 1]`.
        gamma (float): Focusing parameter :math:`\gamma >= 0`.
        reduction (Optional[str]): Specifies the reduction to apply to the
         output: ‘none’ | ‘mean’ | ‘sum’. ‘none’: no reduction will be applied,
         ‘mean’: the sum of the output will be divided by the number of elements
         in the output, ‘sum’: the output will be summed. Default: ‘none’.

    Shape:
        - Input: :math:`(N, C, H, W)` where C = number of classes.
        - Target: :math:`(N, H, W)` where each value is
          :math:`0 ≤ targets[i] ≤ C−1`.

    Examples:
        >>> N = 5  # num_classes
        >>> loss = tgm.losses.FocalLoss(alpha=0.5, gamma=2.0, reduction='mean')
        >>> input = torch.randn(1, N, 3, 5, requires_grad=True)
        >>> target = torch.empty(1, 3, 5, dtype=torch.long).random_(N)
        >>> output = loss(input, target)
        >>> output.backward()

    References:
        [1] https://arxiv.org/abs/1708.02002
    """

    def __init__(self, alpha: float, gamma: Optional[float] = 2.0,
                 reduction: Optional[str] = 'none') -> None:
        super(FocalLoss, self).__init__()
        self.alpha: float = alpha
        self.gamma: Optional[float] = gamma
        self.reduction: Optional[str] = reduction
        self.eps: float = 1e-6

    def forward(
            self,
            input: torch.Tensor,
            target: torch.Tensor) -> torch.Tensor:
        if not torch.is_tensor(input):
            raise TypeError("Input type is not a torch.Tensor. Got {}"
                            .format(type(input)))
        if not len(input.shape) == 4:
            raise ValueError("Invalid input shape, we expect BxNxHxW. Got: {}"
                             .format(input.shape))
        if not input.shape[-2:] == target.shape[-2:]:
            raise ValueError("input and target shapes must be the same. Got: {}"
                             .format(input.shape, input.shape))
        if not input.device == target.device:
            raise ValueError(
                "input and target must be in the same device. Got: {}" .format(
                    input.device, target.device))
        # compute softmax over the classes axis
        input_soft = F.softmax(input, dim=1) + self.eps

        # create the labels one hot tensor
        target_one_hot = one_hot(target, num_classes=input.shape[1],
                                 device=input.device, dtype=input.dtype)

        # compute the actual focal loss
        weight = torch.pow(1. - input_soft, self.gamma)
        focal = -self.alpha * weight * torch.log(input_soft)
        loss_tmp = torch.sum(target_one_hot * focal, dim=1)

        loss = -1
        if self.reduction == 'none':
            loss = loss_tmp
        elif self.reduction == 'mean':
            loss = torch.mean(loss_tmp)
        elif self.reduction == 'sum':
            loss = torch.sum(loss_tmp)
        else:
            raise NotImplementedError("Invalid reduction mode: {}"
                                      .format(self.reduction))
        return loss


class RMSNorm(nn.Module):
    def __init__(self, d, eps=1e-8):
        """
        Root Mean Square Layer Normalization, from https://github.com/bzhangGo/rmsnorm
        :param d: model size
        :param eps:  epsilon value, default 1e-8
        """
        super(RMSNorm, self).__init__()

        self.eps = eps
        self.d = d

        self.scale = nn.Parameter(torch.ones(d))
        self.register_parameter("scale", self.scale)

    def forward(self, x):
        norm_x = x.norm(2, dim=-1, keepdim=True)
        rms_x = norm_x * self.d ** (-1.0 / 2)
        x_normed = x / (rms_x + self.eps)

        return self.scale * x_normed


class Padding:
    """
    A utility class for padding sequences to a specific length.

    This class provides a method to right-pad sequences with zeros to a specified length.
    It is useful for preparing sequences of varying lengths for input to sequence models like RNNs.
    """
    def __init__(self):
        """
        Constructor for the Padding class.
        """
        pass

    def rpad(self, batch, seq_len):
        """
        Right-pad sequences in a batch to a specified length.

        This method takes a batch of sequences and a sequence length as input.
        It pads each sequence in the batch on the right with zeros until it reaches the specified length.
        If a sequence is longer than the specified length, it is trimmed from the left.

        Parameters:
        batch (list of np.array): A batch of sequences.
        seq_len (int): The desired sequence length after padding.

        Returns:
        torch.Tensor: A tensor containing the padded sequences.
        """
        trimmed_arr = [
            np.pad(
                seq[-seq_len:],
                (0, seq_len - len(seq[-seq_len:])),
                mode="constant",
                constant_values=0,
            )
            for seq in batch
        ]
        tensor = torch.stack(
            [torch.tensor(seq, dtype=torch.int) for seq in trimmed_arr]
        )
        return tensor


class BCELossClassWeighted(nn.Module):
    """
    Binary Cross Entropy Loss with class weights.

    This loss function is used for binary classification tasks where the classes are imbalanced.
    It applies class weights to the positive and negative classes to address the class imbalance problem.

    Args:
        weights (list): A list of two elements representing the class weights for the positive and negative classes.

    Attributes:
        weights (list): A list of two elements representing the class weights for the positive and negative classes.
    """

    def __init__(self, weights):
        super().__init__()
        self.weights = weights

    def forward(self, input, target):
        """
        Compute the forward pass of the loss function.

        Args:
            input (torch.Tensor): The predicted output of the model.
            target (torch.Tensor): The target labels.

        Returns:
            torch.Tensor: The computed loss value.
        """
        input = torch.clamp(input, min=1e-7, max=1 - 1e-7)
        bce = -self.weights[1] * target * torch.log(input) - (
            1 - target
        ) * self.weights[0] * torch.log(1 - input)
        return torch.mean(bce)

    
class RMSNorm(nn.Module):
    def __init__(self, dim):
        super().__init__()
        self.scale = dim**0.5
        self.g = nn.Parameter(torch.ones(dim))

    def forward(self, x):
        return F.normalize(x, dim=-1) * self.scale * self.g
    

class FFSwiGLU(nn.Module):
    def __init__(
        self,
        dim: int,
        hidden_dim: int,
        multiple_of: int
    ):
        super().__init__()
        hidden_dim = int(2 * hidden_dim / 3)
        hidden_dim = multiple_of * ((hidden_dim + multiple_of - 1) // multiple_of)

        self.w1 = nn.Linear(
            dim, hidden_dim, bias=False)
        self.w2 = nn.Linear(
            hidden_dim, dim, bias=False)
        self.w3 = nn.Linear(
            dim, hidden_dim, bias=False)

    def forward(self, x):
        return self.w2(F.silu(self.w1(x)) * self.w3(x))
