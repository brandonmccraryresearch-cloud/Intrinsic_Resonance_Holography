"""
Models module for IRH transformer architecture.

This module provides the neural network models for ML surrogates,
adapted from AlphaGeometry's transformer architecture.

Key Components:
- IRHTransformer: Complete end-to-end model
- HolographicEncoder: Encodes RG trajectories  
- ResonanceDecoder: Decodes predictions
- Attention modules: Multi-head and graph attention
"""

from .irh_transformer import IRHTransformer
from .holographic_encoder import HolographicEncoder, NodeEmbedding, EdgeEmbedding
from .resonance_decoder import ResonanceDecoder, DecoderLayer, FeedForward
from .attention_modules import (
    MultiHeadAttention,
    GraphAttention,
    PositionalEncoding
)

__all__ = [
    'IRHTransformer',
    'HolographicEncoder',
    'NodeEmbedding',
    'EdgeEmbedding',
    'ResonanceDecoder',
    'DecoderLayer',
    'FeedForward',
    'MultiHeadAttention',
    'GraphAttention',
    'PositionalEncoding',
]
