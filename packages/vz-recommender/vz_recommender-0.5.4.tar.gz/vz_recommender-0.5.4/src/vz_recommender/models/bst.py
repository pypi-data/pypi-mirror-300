from typing import *
import torch
import abc
from torch import nn
from torch.nn import TransformerEncoder, TransformerEncoderLayer
from transformers import AutoModel, DistilBertModel


import sys, os
sys.path.insert(0, os.path.abspath("../models/"))


from .context import ContextHead, ContextTransformerAndWide
from .transformer import TransformerAEP, ParallelTransformerBlock, ParallelTransformerAEP, \
    ParallelTransformerAEP2S, ParallelTransformerIHQ
from .moe import MoE
from transformers import DistilBertConfig, DistilBertModel
from .utils import MeanMaxPooling
from .mmoe import MMoE
from .moe import ExpertLayer, MoEFFLayer, MoEFFLayerTopK


class BST(nn.Module):
    """
    Args:
        deep_dims: size of the dictionary of embeddings.
        seq_dim: size of the dictionary of embeddings.
        seq_embed_dim: the number of expected features in the encoder/decoder inputs.
        deep_embed_dims: the size of each embedding vector, can be either int or list of int.
        seq_hidden_size: the dimension of the feedforward network model.
        num_wide: the number of wide input features (default=0).
        num_shared: the number of embedding shared with sequence transformer (default=1).
    """
    def __init__(self, deep_dims, page_dim, seq_dim, page_embed_dim, item_embed_dim, seq_embed_dim, wad_embed_dim, deep_embed_dims, seq_hidden_size,
                 num_wide=0, num_shared=0, context_head_kwargs=None, sequence_transformer_kwargs=None,
                 page_embedding_weight=None, item_embedding_weight=None, shared_embeddings_weight=None):
        super().__init__()
        context_head_kwargs = context_head_kwargs if context_head_kwargs else {}
        sequence_transformer_kwargs = sequence_transformer_kwargs if sequence_transformer_kwargs else {}
        if page_embedding_weight is None:
            print("not use pretrained page embedding")
            self.page_embedding = nn.Embedding(page_dim, page_embed_dim)
        else:
            print("use pretrained page embedding")
            self.page_embedding = nn.Embedding.from_pretrained(page_embedding_weight, freeze=True)

        if item_embedding_weight is None:
            print("not use pretrained item embedding")
            self.item_embedding = nn.Embedding(seq_dim, item_embed_dim)
        else:
            print("use pretrained item embedding")
            self.item_embedding = nn.Embedding.from_pretrained(item_embedding_weight, freeze=True)

        self.context_head = ContextHead(
            deep_dims=deep_dims,
            num_wide=num_wide,
            num_shared=num_shared,
            item_embedding=self.item_embedding,
            wad_embed_dim=wad_embed_dim,
            shared_embeddings_weight=shared_embeddings_weight,
            deep_embed_dims=deep_embed_dims
        )
        self.sequence_transformer = TransformerAEP(
            page_embedding=self.page_embedding,
            item_embedding=self.item_embedding,
            seq_embed_dim=seq_embed_dim,
            seq_hidden_size=seq_hidden_size,
            **sequence_transformer_kwargs,
        )
        self.dense1 = torch.nn.Linear(
            in_features=seq_embed_dim+2*wad_embed_dim,
            out_features=(seq_embed_dim+2*wad_embed_dim)//2
        )
        self.act1 = self.act2 = nn.LeakyReLU(0.2)
        self.dense2 = torch.nn.Linear((seq_embed_dim+2*wad_embed_dim)//2, seq_embed_dim)

    @abc.abstractmethod
    def forward(self, **kwargs):
        pass


class AudienceTTIHQ(nn.Module):
    def __init__(self, user_deep_dims, user_deep_embed_dims, user_num_wide, user_wad_embed_dim,
                 offer_deep_dims, offer_deep_embed_dims, offer_num_wide, offer_wad_embed_dim,
                 svc_dim, svc_embed_dim, new_svc_dim, new_svc_embed_dim,
                 svc_desc_dly_dim, svc_desc_dly_embed_dim, ihq_dim,
                 page_dim, item_dim, seq_embed_dim, user_moe_kwargs,
                 sequence_transformer_kwargs, ihq_transformer_kwargs):
        super().__init__()
        # user layers
        self.user_context_head = ContextHead(
            deep_dims=user_deep_dims,
            num_wide=user_num_wide,
            deep_embed_dims=user_deep_embed_dims,
            wad_embed_dim=user_wad_embed_dim,
        )

        self.svc_embedding = nn.Embedding(svc_dim, svc_embed_dim)
        self.new_svc_embedding = nn.Embedding(new_svc_dim, new_svc_embed_dim)
        self.svc_desc_dly_embedding = nn.Embedding(svc_desc_dly_dim, svc_desc_dly_embed_dim)
        self.mm_pooling = MeanMaxPooling()

        self.ihq_embedding = nn.Embedding(ihq_dim, seq_embed_dim)
        self.ihq_transformer = ParallelTransformerIHQ(
            ihq_embedding=self.ihq_embedding,
            dim=seq_embed_dim,
            dim_head=seq_embed_dim,
            heads=ihq_transformer_kwargs.get("ihq_num_heads"),
            num_layers=ihq_transformer_kwargs.get("ihq_num_layers"),
        )

        self.page_embedding = nn.Embedding(page_dim, seq_embed_dim)
        self.item_embedding = nn.Embedding(item_dim, seq_embed_dim)
        self.sequence_transformer = ParallelTransformerAEP2S(
            page_embedding=self.page_embedding,
            item_embedding=self.item_embedding,
            dim=seq_embed_dim,
            dim_head=seq_embed_dim,
            heads=sequence_transformer_kwargs.get("seq_num_heads"),
            num_layers=sequence_transformer_kwargs.get("seq_num_layers"),
        )

        if user_num_wide:
            user_ctx_out_dims = user_wad_embed_dim
        else:
            user_ctx_out_dims = user_wad_embed_dim // 2
        self.user_att_pooling = ParallelTransformerBlock(
            dim=seq_embed_dim, dim_head=seq_embed_dim, heads=1
        )
        self.user_moe = MoEFFLayerTopK(
            dim=seq_embed_dim,
            num_experts=user_moe_kwargs.get("num_experts"),
            expert_capacity=user_moe_kwargs.get("expert_capacity"),
            hidden_size=seq_embed_dim,
            expert_class=ExpertLayer,
            num_K=user_moe_kwargs.get("num_K"),
        )
        self.user_dense_0 = torch.nn.Linear(
            # ihq_out + aep_seq_out + user_ctx_out + svc_out + new_svc_out + svc_desc_dly_out
            in_features=seq_embed_dim + user_ctx_out_dims + seq_embed_dim +
                        svc_embed_dim * 2 + new_svc_embed_dim * 2 + svc_desc_dly_embed_dim * 2,
            out_features=seq_embed_dim * 4
        )
        self.user_dense_1 = torch.nn.Linear(
            in_features=seq_embed_dim * 4,
            out_features=seq_embed_dim
        )
        self.user_act = nn.LeakyReLU(0.2)
        self.user_dropout = nn.Dropout(p=0.1)

        # offer layers
        self.offer_context_head = ContextHead(
            deep_dims=offer_deep_dims,
            num_wide=offer_num_wide,
            deep_embed_dims=offer_deep_embed_dims,
            wad_embed_dim=offer_wad_embed_dim,
        )

        if offer_num_wide:
            offer_ctx_out_dims = offer_wad_embed_dim
        else:
            offer_ctx_out_dims = offer_wad_embed_dim // 2
        self.offer_dense_0 = torch.nn.Linear(
            in_features=offer_ctx_out_dims,
            out_features=offer_ctx_out_dims + offer_ctx_out_dims // 2
        )
        self.offer_dense_1 = torch.nn.Linear(
            in_features=offer_ctx_out_dims + offer_ctx_out_dims // 2,
            out_features=seq_embed_dim
        )
        self.offer_act = nn.LeakyReLU(0.2)
        self.offer_dropout = nn.Dropout(p=0.1)

        self.out_act = nn.Sigmoid()

    def forward(self, user_deep_in, offer_deep_in, svc_in, new_svc_in, svc_desc_dly_in, 
                page_in, item_in, vl_in, user_wide_in, offer_wide_in, ihq_in, ihq_vl_in):
        """
        Args:
            deep_in: list, a list of Tensor of shape [batch_size, deep_dims].
            seq_in: Tensor, shape [batch_size, seq_len].
            vl_in: Tensor, shape [batch_size].
            wide_in: list, a list of Tensor of shape [batch_size, num_wide].
            shared_in: list, a list of Tensor of shape [batch_size, num_shared] (default=None).
            nlp_in: tensor, Tensor of shape [batch_size, sentence_length] (default=None).
            att_mask: tensor, Tensor of shape [batch_size, sentence_length] (default=None).
        Return:
            out: Tensor, shape [batch_size, seq_dim].
            user_out: Tensor, shape [batch_size, seq_embed_dim].
        """
        svc_out = self.svc_embedding(svc_in.long())
        svc_out = self.mm_pooling(svc_out)
        new_svc_out = self.new_svc_embedding(new_svc_in.long())
        new_svc_out = self.mm_pooling(new_svc_out)
        svc_desc_dly_out = self.svc_desc_dly_embedding(svc_desc_dly_in.long())
        svc_desc_dly_out = self.mm_pooling(svc_desc_dly_out)

        aep_seq_out = self.sequence_transformer(page_in=page_in, item_in=item_in, vl_in=vl_in)

        ihq_out = self.ihq_transformer(ihq_in=ihq_in, ihq_vl_in=ihq_vl_in)

        user_ctx_out = self.user_context_head(deep_in=user_deep_in, wide_in=user_wide_in)
        user_out = torch.stack([ihq_out, aep_seq_out, user_ctx_out, svc_out, new_svc_out, svc_desc_dly_out], dim=1)
        user_out = self.user_att_pooling(user_out)
        user_out, user_aux_loss = self.user_moe(user_out)
        user_out = torch.concat(user_out.unbind(1), dim=1)
        user_out = self.user_dense_0(user_out)
        user_out = self.user_act(user_out)
        user_out = self.user_dropout(user_out)
        user_out = self.user_dense_1(user_out)
        user_out = self.user_act(user_out)

        offer_ctx_out = self.offer_context_head(deep_in=offer_deep_in, wide_in=offer_wide_in)
        offer_out = offer_ctx_out
        offer_out = self.offer_dense_0(offer_out)
        offer_out = self.offer_act(offer_out)
        offer_out = self.offer_dropout(offer_out)
        offer_out = self.offer_dense_1(offer_out)
        offer_out = self.offer_act(offer_out)

        out = torch.mul(user_out, offer_out)
        out = torch.sum(out, dim=1)
        out = self.out_act(out)

        return out, user_out, offer_out, user_aux_loss


class BSTAudienceTaWTT(nn.Module):
    def __init__(self, user_deep_dims, user_deep_embed_dims, user_num_wide, user_wad_embed_dim,
                 offer_deep_dims, offer_deep_embed_dims, offer_num_wide, offer_wad_embed_dim,
                 svc_dim, svc_embed_dim, new_svc_dim, new_svc_embed_dim,
                 svc_desc_dly_dim, svc_desc_dly_embed_dim,
                 page_dim, item_dim, seq_embed_dim,
                 nlp_encoder_path, nlp_dim, sequence_transformer_kwargs=None):
        super().__init__()
        # user layers
        self.user_context_head = ContextTransformerAndWide(
            deep_dims=user_deep_dims,
            num_wide=user_num_wide,
            deep_embed_dims=user_deep_embed_dims,
            wad_embed_dim=user_wad_embed_dim,
        )

        self.svc_embedding = nn.Embedding(svc_dim, svc_embed_dim)
        self.new_svc_embedding = nn.Embedding(new_svc_dim, new_svc_embed_dim)
        self.svc_desc_dly_embedding = nn.Embedding(svc_desc_dly_dim, svc_desc_dly_embed_dim)
        self.mm_pooling = MeanMaxPooling()

        self.page_embedding = nn.Embedding(page_dim, seq_embed_dim)
        self.item_embedding = nn.Embedding(item_dim, seq_embed_dim)
        self.sequence_transformer = ParallelTransformerAEP2S(
            page_embedding=self.page_embedding,
            item_embedding=self.item_embedding,
            dim=seq_embed_dim,
            dim_head=seq_embed_dim,
            heads=sequence_transformer_kwargs.get("seq_num_heads"),
            num_layers=sequence_transformer_kwargs.get("seq_num_layers"),
        )

        self.nlp_encoder = AutoModel.from_pretrained(nlp_encoder_path)
        self.nlp_dense_0 = torch.nn.Linear(
            in_features=nlp_dim,
            out_features=seq_embed_dim
        )
        self.nlp_act = nn.LeakyReLU(0.2)

        if user_num_wide:
            user_ctx_out_dims = user_wad_embed_dim
        else:
            user_ctx_out_dims = user_wad_embed_dim // 2
        self.user_att_pooling = ParallelTransformerBlock(
            dim=seq_embed_dim, dim_head=seq_embed_dim, heads=1
        )
        self.user_dense_0 = torch.nn.Linear(
            # nlp_out + aep_seq_out + user_ctx_out + svc_out + new_svc_out + svc_desc_dly_out
            in_features=seq_embed_dim + seq_embed_dim + user_ctx_out_dims +
                        svc_embed_dim * 2 + new_svc_embed_dim * 2 + svc_desc_dly_embed_dim * 2,
            out_features=seq_embed_dim * 4
        )
        self.user_dense_1 = torch.nn.Linear(
            in_features=seq_embed_dim * 4,
            out_features=seq_embed_dim
        )
        self.user_act = nn.LeakyReLU(0.2)
        self.user_dropout = nn.Dropout(p=0.1)

        # offer layers
        self.offer_context_head = ContextTransformerAndWide(
            deep_dims=offer_deep_dims,
            num_wide=offer_num_wide,
            deep_embed_dims=offer_deep_embed_dims,
            wad_embed_dim=offer_wad_embed_dim,
        )

        if offer_num_wide:
            offer_ctx_out_dims = offer_wad_embed_dim
        else:
            offer_ctx_out_dims = offer_wad_embed_dim // 2
        self.offer_dense_0 = torch.nn.Linear(
            in_features=offer_ctx_out_dims,
            out_features=offer_ctx_out_dims + offer_ctx_out_dims // 2
        )
        self.offer_dense_1 = torch.nn.Linear(
            in_features=offer_ctx_out_dims + offer_ctx_out_dims // 2,
            out_features=seq_embed_dim
        )
        self.offer_act = nn.LeakyReLU(0.2)
        self.offer_dropout = nn.Dropout(p=0.1)

        self.out_act = nn.Sigmoid()

    def forward(self, user_deep_in, offer_deep_in, svc_in, new_svc_in, svc_desc_dly_in,
                page_in, item_in, vl_in, user_wide_in, offer_wide_in, nlp_in):
        """
        Args:
            deep_in: list, a list of Tensor of shape [batch_size, deep_dims].
            seq_in: Tensor, shape [batch_size, seq_len].
            vl_in: Tensor, shape [batch_size].
            wide_in: list, a list of Tensor of shape [batch_size, num_wide].
            shared_in: list, a list of Tensor of shape [batch_size, num_shared] (default=None).
            nlp_in: tensor, Tensor of shape [batch_size, sentence_length] (default=None).
            att_mask: tensor, Tensor of shape [batch_size, sentence_length] (default=None).
        Return:
            out: Tensor, shape [batch_size, seq_dim].
            user_out: Tensor, shape [batch_size, seq_embed_dim].
        """
        svc_out = self.svc_embedding(svc_in.long())
        svc_out = self.mm_pooling(svc_out)
        new_svc_out = self.new_svc_embedding(new_svc_in.long())
        new_svc_out = self.mm_pooling(new_svc_out)
        svc_desc_dly_out = self.svc_desc_dly_embedding(svc_desc_dly_in.long())
        svc_desc_dly_out = self.mm_pooling(svc_desc_dly_out)

        aep_seq_out = self.sequence_transformer(page_in=page_in, item_in=item_in, vl_in=vl_in)

        nlp_out = self.nlp_encoder(**nlp_in).pooler_output.to(dtype=torch.float32)
        nlp_out = self.nlp_dense_0(nlp_out)
        nlp_out = self.nlp_act(nlp_out)

        user_ctx_out = self.user_context_head(deep_in=user_deep_in, wide_in=user_wide_in)
        user_out = torch.stack([nlp_out, aep_seq_out, user_ctx_out, svc_out, new_svc_out, svc_desc_dly_out], dim=1)
        user_out = self.user_att_pooling(user_out)
        user_out = torch.concat(user_out.unbind(1), dim=1)
        user_out = self.user_dense_0(user_out)
        user_out = self.user_act(user_out)
        user_out = self.user_dropout(user_out)
        user_out = self.user_dense_1(user_out)
        user_out = self.user_act(user_out)

        offer_ctx_out = self.offer_context_head(deep_in=offer_deep_in, wide_in=offer_wide_in)
        offer_out = offer_ctx_out
        offer_out = self.offer_dense_0(offer_out)
        offer_out = self.offer_act(offer_out)
        offer_out = self.offer_dropout(offer_out)
        offer_out = self.offer_dense_1(offer_out)
        offer_out = self.offer_act(offer_out)

        out = torch.mul(user_out, offer_out)
        out = torch.sum(out, dim=1)
        out = self.out_act(out)

        return out, user_out, offer_out


class BSTAudienceTwoTowerPplan(nn.Module):
    def __init__(self, user_deep_dims, user_deep_embed_dims, user_num_wide, user_num_shared, user_wad_embed_dim,
                 offer_deep_dims, offer_deep_embed_dims, offer_num_wide, offer_num_shared, offer_wad_embed_dim,
                 svc_dim, svc_embed_dim, page_dim, page_embed_dim, item_dim, item_embed_dim, seq_embed_dim,
                 seq_hidden_size,
                 nlp_encoder_path, nlp_dim=0, sequence_transformer_kwargs=None):
        super().__init__()
        # user layers
        self.user_context_head = ContextHead(
            deep_dims=user_deep_dims,
            num_wide=user_num_wide,
            deep_embed_dims=user_deep_embed_dims,
            wad_embed_dim=user_wad_embed_dim,
            num_shared=user_num_shared,
        )

        self.svc_embedding = nn.Embedding(svc_dim, svc_embed_dim)
        self.svc_pooling = MeanMaxPooling()

        self.page_embedding = nn.Embedding(page_dim, page_embed_dim)
        self.item_embedding = nn.Embedding(item_dim, item_embed_dim)
        self.sequence_transformer = TransformerAEP(
            page_embedding=self.page_embedding,
            item_embedding=self.item_embedding,
            seq_embed_dim=seq_embed_dim,
            seq_hidden_size=seq_hidden_size,
            **sequence_transformer_kwargs,
        )

        self.nlp_encoder = DistilBertModel.from_pretrained(nlp_encoder_path)
        self.search_nlp_dense_0 = torch.nn.Linear(
            in_features=nlp_dim,
            out_features=seq_embed_dim * 2
        )
        self.search_nlp_dense_1 = torch.nn.Linear(
            in_features=seq_embed_dim * 2,
            out_features=seq_embed_dim // 2
        )
        self.nlp_act = nn.LeakyReLU(0.2)

        if user_num_wide:
            user_ctx_out_dims = user_wad_embed_dim
        else:
            user_ctx_out_dims = user_wad_embed_dim // 2
        self.user_dense_0 = torch.nn.Linear(
            # nlp_out + aep_seq_out + svc_out + user_ctx_out
            in_features=seq_embed_dim // 2 + seq_embed_dim + svc_embed_dim * 2 + user_ctx_out_dims,
            out_features=seq_embed_dim * 2
        )
        self.user_dense_1 = torch.nn.Linear(
            in_features=seq_embed_dim * 2,
            out_features=seq_embed_dim
        )
        self.user_act = nn.LeakyReLU(0.2)
        self.user_dropout = nn.Dropout(p=0.1)

        # offer layers
        self.offer_context_head = ContextHead(
            deep_dims=offer_deep_dims,
            num_wide=offer_num_wide,
            deep_embed_dims=offer_deep_embed_dims,
            wad_embed_dim=offer_wad_embed_dim,
            num_shared=offer_num_shared,
        )

        if offer_num_wide:
            offer_ctx_out_dims = offer_wad_embed_dim
        else:
            offer_ctx_out_dims = offer_wad_embed_dim // 2
        self.offer_dense_0 = torch.nn.Linear(
            in_features=offer_ctx_out_dims,
            out_features=offer_ctx_out_dims + offer_ctx_out_dims // 2
        )
        self.offer_dense_1 = torch.nn.Linear(
            in_features=offer_ctx_out_dims + offer_ctx_out_dims // 2,
            out_features=seq_embed_dim
        )
        self.offer_act = nn.LeakyReLU(0.2)
        self.offer_dropout = nn.Dropout(p=0.1)

        self.out_act = nn.Sigmoid()

    def forward(self, user_deep_in, offer_deep_in, svc_in, page_in, item_in, vl_in,
                user_wide_in=None, offer_wide_in=None, search_in=None):
        """
        Args:
            deep_in: list, a list of Tensor of shape [batch_size, deep_dims].
            seq_in: Tensor, shape [batch_size, seq_len].
            vl_in: Tensor, shape [batch_size].
            wide_in: list, a list of Tensor of shape [batch_size, num_wide].
            shared_in: list, a list of Tensor of shape [batch_size, num_shared] (default=None).
            search_ids: tensor, Tensor of shape [batch_size, sentence_length] (default=None).
            att_mask: tensor, Tensor of shape [batch_size, sentence_length] (default=None).
        Return:
            out: Tensor, shape [batch_size, seq_dim].
            user_out: Tensor, shape [batch_size, seq_embed_dim].
        """
        svc_out = self.svc_embedding(svc_in.long())
        svc_out = self.svc_pooling(svc_out)

        aep_seq_out = self.sequence_transformer(page_in=page_in, item_in=item_in, vl_in=vl_in)

        search_out = self.nlp_encoder(**search_in).last_hidden_state[:, 0, :].to(dtype=torch.float32)
        search_out = self.search_nlp_dense_0(search_out)
        search_out = self.nlp_act(search_out)
        search_out = self.search_nlp_dense_1(search_out)
        search_out = self.nlp_act(search_out)

        user_ctx_out = self.user_context_head(deep_in=user_deep_in, wide_in=user_wide_in)
        user_out = torch.cat([search_out, aep_seq_out, svc_out, user_ctx_out], dim=1)
        user_out = self.user_dense_0(user_out)
        user_out = self.user_act(user_out)
        user_out = self.user_dropout(user_out)
        user_out = self.user_dense_1(user_out)
        user_out = self.user_act(user_out)

        offer_ctx_out = self.offer_context_head(deep_in=offer_deep_in, wide_in=offer_wide_in)
        offer_out = offer_ctx_out
        offer_out = self.offer_dense_0(offer_out)
        offer_out = self.offer_act(offer_out)
        offer_out = self.offer_dropout(offer_out)
        offer_out = self.offer_dense_1(offer_out)
        offer_out = self.offer_act(offer_out)

        out = torch.mul(user_out, offer_out)
        out = torch.sum(out, dim=1)
        out = self.out_act(out)

        return out, user_out, offer_out
    
    
class BSTHome(nn.Module):
    def __init__(self, deep_dims, page_dim, seq_dim, page_embed_dim, item_embed_dim, seq_embed_dim, deep_embed_dims, wad_embed_dim, nlp_embed_dim, seq_hidden_size, nlp_encoder_path, freeze=False,
                 num_wide=0, num_shared=0, nlp_dim=0, context_head_kwargs=None, sequence_transformer_kwargs=None,
                 page_embedding_weight=None, item_embedding_weight=None, shared_embeddings_weight=None):
        super().__init__()
        self.nlp_encoder = DistilBertModel.from_pretrained(nlp_encoder_path)
        
        if freeze:
            for param in self.nlp_encoder.parameters():
                param.requires_grad = False
        
        context_head_kwargs = context_head_kwargs if context_head_kwargs else {}
        sequence_transformer_kwargs = sequence_transformer_kwargs if sequence_transformer_kwargs else {}
        
        if page_embedding_weight is None:
            print("not use pretrained embedding")
            self.page_embedding = nn.Embedding(page_dim, page_embed_dim)
        else:
            print("use pretrained item embedding")
            self.page_embedding = nn.Embedding.from_pretrained(page_embedding_weight, freeze=True)

        if item_embedding_weight is None:
            print("not use pretrained embedding")
            self.item_embedding = nn.Embedding(seq_dim, item_embed_dim)
        else:
            print("use pretrained item embedding")
            self.item_embedding = nn.Embedding.from_pretrained(item_embedding_weight, freeze=False)
            
        self.context_head = ContextHead(
            deep_dims=deep_dims,
            num_wide=num_wide,
            item_embedding=self.item_embedding,
            shared_embeddings_weight=shared_embeddings_weight,
            wad_embed_dim=wad_embed_dim,
            deep_embed_dims=deep_embed_dims
        )
        self.sequence_transformer = TransformerAEP(
            page_embedding=self.page_embedding,
            item_embedding=self.item_embedding,
            seq_embed_dim=page_embed_dim + item_embed_dim,
            seq_hidden_size=seq_hidden_size,
            **sequence_transformer_kwargs,
        )
        self.seq_dense = torch.nn.Linear(
            in_features=page_embed_dim + item_embed_dim,
            out_features=seq_embed_dim
        )
        self.nlp_dense = torch.nn.Linear(
            in_features=nlp_dim,
            out_features=nlp_embed_dim
        )
        self.dense1 = torch.nn.Linear(
            in_features=nlp_embed_dim + wad_embed_dim + seq_embed_dim,
            out_features=seq_embed_dim)
        self.act1 = self.act2 = nn.LeakyReLU(0.2)
        self.dense2 = torch.nn.Linear(seq_embed_dim, seq_embed_dim // 2)
        self.dense3 = torch.nn.Linear(seq_embed_dim // 2, 1)

    def forward(self, deep_in, page_in, item_in, vl_in, wide_in=None, shared_in=None, search_in=None):
        """
        Args:
            deep_in: list, a list of Tensor of shape [batch_size, deep_dims].
            seq_in: Tensor, shape [batch_size, seq_len].
            vl_in: Tensor, shape [batch_size].
            wide_in: list, a list of Tensor of shape [batch_size, num_wide].
            shared_in: list, a list of Tensor of shape [batch_size, num_shared] (default=None).
            search_ids: tensor, Tensor of shape [batch_size, sentence_length] (default=None).
            att_mask: tensor, Tensor of shape [batch_size, sentence_length] (default=None).

        Return:
            out: Tensor, shape [batch_size, seq_dim].
            user_out: Tensor, shape [batch_size, seq_embed_dim].
        """
        search_out = self.nlp_encoder(**search_in).last_hidden_state[:,0,:].to(dtype=torch.float32)
        search_out = self.nlp_dense(search_out)
        ctx_out = self.context_head(deep_in=deep_in, wide_in=wide_in, shared_in=shared_in)
        seq_out = self.sequence_transformer(page_in=page_in, item_in=item_in, vl_in=vl_in)
        seq_out = self.seq_dense(seq_out)
        outs = torch.cat([seq_out, ctx_out, search_out], dim=1)
        outs = self.dense1(outs)
        outs = self.act1(outs)
        outs = self.dense2(outs)
        outs = self.act2(outs)
        outs = self.dense3(outs)
        return outs
    
    
class BSTGridwall(nn.Module):
    def __init__(self, deep_dims, page_dim, seq_dim, page_embed_dim, item_embed_dim, seq_embed_dim, deep_embed_dims, wad_embed_dim, nlp_embed_dim, seq_hidden_size, nlp_encoder_path, 
                 num_wide=0, num_shared=0, nlp_dim=0, item_freeze=None, nlp_freeze=None, context_head_kwargs=None, sequence_transformer_kwargs=None,
                 page_embedding_weight=None, item_embedding_weight=None, shared_embeddings_weight=None):
        super().__init__()
        self.nlp_encoder = DistilBertModel.from_pretrained(nlp_encoder_path)
        context_head_kwargs = context_head_kwargs if context_head_kwargs else {}
        sequence_transformer_kwargs = sequence_transformer_kwargs if sequence_transformer_kwargs else {}
        
        if page_embedding_weight is None:
            print("not use pretrained embedding")
            self.page_embedding = nn.Embedding(page_dim, page_embed_dim)
        else:
            print("use pretrained item embedding")
            self.page_embedding = nn.Embedding.from_pretrained(page_embedding_weight, freeze=True)

        if item_embedding_weight is None:
            print("not use pretrained embedding")
            self.item_embedding = nn.Embedding(seq_dim, item_embed_dim)
        else:
            print("use pretrained item embedding")
            self.item_embedding = nn.Embedding.from_pretrained(item_embedding_weight, freeze=False)
            
        if item_freeze:
            self.item_embedding.weight.requires_grad = False
            
        if nlp_freeze:
            for param in self.nlp_encoder.parameters():
                param.requires_grad = False
            
        self.context_head = ContextHead(
            deep_dims=deep_dims,
            num_wide=num_wide,
            item_embedding=self.item_embedding,
            shared_embeddings_weight=shared_embeddings_weight,
            wad_embed_dim=wad_embed_dim,
            deep_embed_dims=deep_embed_dims
        )
        self.sequence_transformer = TransformerAEP(
            page_embedding=self.page_embedding,
            item_embedding=self.item_embedding,
            seq_embed_dim=page_embed_dim + item_embed_dim,
            seq_hidden_size=seq_hidden_size,
            **sequence_transformer_kwargs,
        )
        self.seq_dense = torch.nn.Linear(
            in_features=page_embed_dim + item_embed_dim,
            out_features=seq_embed_dim
        )
        self.nlp_dense = torch.nn.Linear(
            in_features=nlp_dim,
            out_features=nlp_embed_dim
        )
        self.dense1 = torch.nn.Linear(
            in_features=nlp_embed_dim + wad_embed_dim + seq_embed_dim,
            out_features=seq_embed_dim)
        self.act1 = self.act2 = nn.LeakyReLU(0.2)
        self.dense2 = torch.nn.Linear(seq_embed_dim, seq_embed_dim)
        self.dense3 = torch.nn.Linear(seq_embed_dim, seq_dim)

    def forward(self, deep_in, page_in, item_in, vl_in, wide_in=None, input_ids=None, attention_mask=None, shared_in=None):
        """
        Args:
            deep_in: list, a list of Tensor of shape [batch_size, deep_dims].
            seq_in: Tensor, shape [batch_size, seq_len].
            vl_in: Tensor, shape [batch_size].
            wide_in: list, a list of Tensor of shape [batch_size, num_wide].
            shared_in: list, a list of Tensor of shape [batch_size, num_shared] (default=None).
            search_ids: tensor, Tensor of shape [batch_size, sentence_length] (default=None).
            att_mask: tensor, Tensor of shape [batch_size, sentence_length] (default=None).

        Return:
            out: Tensor, shape [batch_size, seq_dim].
            user_out: Tensor, shape [batch_size, seq_embed_dim].
        """
        search_out = self.nlp_encoder(input_ids=input_ids, attention_mask=attention_mask).last_hidden_state[:,0,:].to(dtype=torch.float32)
        search_out = self.nlp_dense(search_out)
        ctx_out = self.context_head(deep_in=deep_in, wide_in=wide_in, shared_in=shared_in)
        seq_out = self.sequence_transformer(page_in=page_in, item_in=item_in, vl_in=vl_in)
        seq_out = self.seq_dense(seq_out)
        outs = torch.cat([seq_out, ctx_out, search_out], dim=1)
        outs = self.dense1(outs)
        outs = self.act1(outs)
        outs = self.dense2(outs)
        user_out = self.act2(outs)
        outs = self.dense3(user_out)
        return (outs, user_out)
