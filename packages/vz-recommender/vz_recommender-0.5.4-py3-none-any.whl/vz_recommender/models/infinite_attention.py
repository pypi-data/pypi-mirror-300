import torch.nn.functional as F
from typing import Optional
import torch
import torch.nn as nn


class InfiniAttention(nn.Module):
    def __init__(self, seq_len: int, emb_dim: int,
                 d_head: int, n_head: int, n_segments: int,
                 is_causal: Optional[bool] = True, update: Optional[str] = 'linear',
                 use_rope: Optional[bool] = True, ):
        super().__init__()

        """
        Args:
        seq_len: Sequence length of the inputs.
        n_segments: Number of segments (must be divisible to seq_len).
        n_head: Number of attention heads.
        emb_dim: Embedding dimension of the input.
        d_head: Embedding dimension of each head.
        is_causal: Whether the model causal or not.
        use_rope: Use Rotary Positional Embeddings or not. Default: True.
        """
        if update not in ['linear', 'delta']:
            raise ValueError('Update takes only one of these parameters - linear, delta')

        assert seq_len % n_segments == 0, 'seq_len must be divisible to n_segments'
        assert emb_dim % n_head == 0, 'emb_dim must be divisible to n_head'

        self.seq_len = seq_len
        self.n_segments = n_segments
        self.n_head = n_head
        self.emb_dim = emb_dim
        self.d_head = d_head
        self.is_causal = is_causal
        self.use_rope = use_rope
        self.update = update

        self.beta = nn.Parameter(torch.ones((1,)))  # -> A learnable scalar from the paper.
        self.q = nn.Linear(emb_dim, emb_dim)
        self.k = nn.Linear(emb_dim, emb_dim)
        self.v = nn.Linear(emb_dim, emb_dim)
        self.o = nn.Linear(emb_dim, emb_dim)
        self.elu = nn.ELU()
        self.freq_cis = compute_freq_cis(emb_dim, seq_len, 10000.0)

    @staticmethod
    def create_key_padding_mask(seq_in, valid_length=None):
        device = seq_in.device
        vl_len = torch.cat((seq_in.size(0) * [torch.tensor([seq_in.size(1)])]), dim=0).to(
            device) if valid_length is None else valid_length
        mask = torch.arange(seq_in.size(1)).repeat(seq_in.size(0), 1).to(device)
        mask = ~mask.lt(vl_len.unsqueeze(1))
        return mask

    def forward(self, x: torch.Tensor, vl=None) -> torch.Tensor:

        batch_size, _, _ = x.size()

        # TODO: change init
        memory = torch.zeros((self.n_head, self.d_head, self.d_head)).to(x)
        z = torch.zeros((self.n_head, self.d_head, 1)).to(x)

        query = self.q(x)
        key = self.k(x)
        value = self.v(x)

        if self.use_rope:
            query, key = RoPE(self.freq_cis, query, key)

        query = query.view(batch_size, self.n_head, self.n_segments, self.seq_len // self.n_segments, self.d_head)
        key = key.view(batch_size, self.n_head, self.n_segments, self.seq_len // self.n_segments, self.d_head)
        value = value.view(batch_size, self.n_head, self.n_segments, self.seq_len // self.n_segments, self.d_head)

        output = []

        masks = self.create_key_padding_mask(seq_in=x, valid_length=vl)
        masks = masks.split(self.seq_len // self.n_segments, dim=-1)

        for idx in range(self.n_segments):

            mask_tmp = masks[idx].clone()
            # always have vl=1 in each segment
            mask_tmp[:, 0] = False

            sigma_q = self.elu(query[:, :, idx, :, :]) + 1.0
            sigma_k = self.elu(key[:, :, idx, :, :]) + 1.0
            A_mem = (sigma_q @ memory) / ((sigma_q @ z) + 1e-6)  # Adding 1e-6 for preventing division to 0

            A_dot = query[:, :, idx, :, :] @ key[:, :, idx, :, :].transpose(-2, -1)
            if self.is_causal:
                A_dot = A_dot.masked_fill(mask_tmp.unsqueeze(1).unsqueeze(2), float('-inf'))

            A_dot = F.softmax(A_dot / torch.sqrt(torch.tensor(self.d_head)), dim=-1)

            A_dot = A_dot @ value[:, :, idx, :, :]

            attention = (F.sigmoid(self.beta) * A_mem) + ((1 - F.sigmoid(self.beta)) * A_dot)

            # Update history matrix
            if self.update == 'linear':
                memory = memory + (sigma_k.transpose(-2, -1) @ value[:, :, idx, :, :])
            else:
                delta = (sigma_k @ memory) / ((sigma_k @ z) + 1e-6)
                memory = memory + (sigma_k.transpose(-2, -1) @ (value[:, :, idx, :, :] - delta))

            z = z + sigma_k.sum(dim=-2, keepdim=True)

            output.append(attention)

        attention = torch.concat(output, dim=2).view(batch_size, self.seq_len, self.emb_dim)
        return self.o(attention)


class PositionWiseFeedForward(nn.Module):
    def __init__(self, emb_dim: int, ff_mult: int, dropout_rate: float, bias: Optional[bool] = False):
        super().__init__()

        self.w1 = nn.Linear(emb_dim, emb_dim * ff_mult, bias=bias)
        self.w2 = nn.Linear(emb_dim * ff_mult, emb_dim, bias=bias)
        self.w3 = nn.Linear(emb_dim, emb_dim * ff_mult, bias=bias)
        self.gelu = nn.GELU()
        self.drop = nn.Dropout(dropout_rate)

    def forward(self, x):
        x = self.gelu(self.w1(x)) * self.w3(x)
        x = self.w2(x)

        return self.drop(x)


class InfiniTransformerBlock(nn.Module):
    def __init__(self, seq_len: int, ff_mult: int, emb_dim: int, d_head: int, n_head: int, n_segments: int,
                 dropout_rate: float, eps: Optional[float] = 1e-5):
        super().__init__()

        self.attention = InfiniAttention(seq_len, emb_dim, d_head, n_head, n_segments, update='delta')
        self.attn_norm = RMSNorm(emb_dim, eps)
        self.ffn_norm = RMSNorm(emb_dim, eps)
        self.ffn = PositionWiseFeedForward(emb_dim, ff_mult, dropout_rate)

    def forward(self, x, vl=None):
        x = x + self.attn_norm(self.attention(x, vl))
        x = x + self.ffn_norm(self.ffn(x))

        return x


def compute_freq_cis(emb_dim: int, seq_len: int, thetha: Optional[float] = 10000.0):
    t_thetha = 1.0 / (thetha ** (torch.arange(0, emb_dim, 2)[:emb_dim // 2] / emb_dim))
    t = torch.arange(seq_len)

    freqs = torch.outer(t, t_thetha)
    freqs_cis = torch.polar(torch.ones_like(freqs), freqs)
    return freqs_cis


def RoPE(freq_cis: torch.Tensor, query: torch.Tensor, key: torch.Tensor):
    b, t, c = query.size()

    query = query
    key = key
    freq_cis = freq_cis.to(query)

    query_complex = torch.view_as_complex(query.float().reshape(b, t, c // 2, 2))
    key_complex = torch.view_as_complex(key.float().reshape(b, t, c // 2, 2))

    q_rot = torch.view_as_real(query_complex * freq_cis).flatten(2)
    k_rot = torch.view_as_real(key_complex * freq_cis).flatten(2)

    return q_rot.type_as(query), k_rot.type_as(key)


class RMSNorm(nn.Module):
    def __init__(self, emb_dim: int, eps: Optional[float] = 1e-5):
        super().__init__()

        self.eps = eps
        self.weight = nn.Parameter(torch.ones(emb_dim))

    def forward(self, x):
        x_sqr = x ** 2
        RMS = torch.rsqrt(x_sqr.mean(dim=-1, keepdim=True) + self.eps)
        new_x = x * RMS
        new_x = new_x * self.weight

        return new_x
