"""
Custom Attention Modules for Holographic Data

THEORETICAL FOUNDATION: Inspired by AlphaGeometry attention mechanisms
Adapted for IRH holographic state graph structures

This module provides attention mechanisms specialized for processing
graph-structured holographic state data, including:
- Self-attention for node features
- Cross-attention between RG steps
- Graph attention networks for coupling space
"""

from typing import Optional, Tuple
import numpy as np

try:
    import jax
    import jax.numpy as jnp
    JAX_AVAILABLE = True
except ImportError:
    JAX_AVAILABLE = False


class MultiHeadAttention:
    """
    Multi-head attention for holographic states.
    
    Adapted from AlphaGeometry's transformer attention but specialized
    for graph-structured data representing RG flow trajectories.
    
    Attributes:
        num_heads: Number of attention heads
        head_dim: Dimension of each attention head
        embed_dim: Total embedding dimension
        dropout_rate: Dropout probability
    """
    
    def __init__(
        self,
        embed_dim: int = 128,
        num_heads: int = 8,
        dropout_rate: float = 0.1,
        use_jax: bool = False
    ):
        """
        Initialize multi-head attention.
        
        Args:
            embed_dim: Embedding dimension (must be divisible by num_heads)
            num_heads: Number of attention heads
            dropout_rate: Dropout probability
            use_jax: Use JAX for acceleration if available
        """
        if embed_dim % num_heads != 0:
            raise ValueError(
                f"embed_dim ({embed_dim}) must be divisible by num_heads ({num_heads})"
            )
        
        self.embed_dim = embed_dim
        self.num_heads = num_heads
        self.head_dim = embed_dim // num_heads
        self.dropout_rate = dropout_rate
        self.use_jax = use_jax and JAX_AVAILABLE
        
        # Initialize weights (in real implementation, these would be learned)
        # Here we use placeholder initialization
        self.W_q = None  # Query projection
        self.W_k = None  # Key projection
        self.W_v = None  # Value projection
        self.W_o = None  # Output projection
        
        self._initialize_weights()
    
    def _initialize_weights(self) -> None:
        """Initialize attention weight matrices."""
        scale = 1.0 / np.sqrt(self.embed_dim)
        
        self.W_q = np.random.randn(self.embed_dim, self.embed_dim) * scale
        self.W_k = np.random.randn(self.embed_dim, self.embed_dim) * scale
        self.W_v = np.random.randn(self.embed_dim, self.embed_dim) * scale
        self.W_o = np.random.randn(self.embed_dim, self.embed_dim) * scale
    
    def _split_heads(self, x: np.ndarray) -> np.ndarray:
        """
        Split embedding dimension into multiple heads.
        
        Args:
            x: Input tensor of shape (batch, seq_len, embed_dim)
            
        Returns:
            Tensor of shape (batch, num_heads, seq_len, head_dim)
        """
        batch_size, seq_len, _ = x.shape
        x = x.reshape(batch_size, seq_len, self.num_heads, self.head_dim)
        return np.transpose(x, (0, 2, 1, 3))
    
    def _merge_heads(self, x: np.ndarray) -> np.ndarray:
        """
        Merge multiple heads back into single embedding.
        
        Args:
            x: Input tensor of shape (batch, num_heads, seq_len, head_dim)
            
        Returns:
            Tensor of shape (batch, seq_len, embed_dim)
        """
        batch_size, _, seq_len, _ = x.shape
        x = np.transpose(x, (0, 2, 1, 3))
        return x.reshape(batch_size, seq_len, self.embed_dim)
    
    def forward(
        self,
        query: np.ndarray,
        key: Optional[np.ndarray] = None,
        value: Optional[np.ndarray] = None,
        mask: Optional[np.ndarray] = None
    ) -> np.ndarray:
        """
        Forward pass of multi-head attention.
        
        Args:
            query: Query tensor (batch, seq_len_q, embed_dim)
            key: Key tensor (batch, seq_len_k, embed_dim), defaults to query
            value: Value tensor (batch, seq_len_v, embed_dim), defaults to key
            mask: Attention mask (batch, seq_len_q, seq_len_k)
            
        Returns:
            Output tensor (batch, seq_len_q, embed_dim)
        """
        if key is None:
            key = query
        if value is None:
            value = key
        
        batch_size, seq_len_q, _ = query.shape
        seq_len_k = key.shape[1]
        
        # Project to Q, K, V
        Q = np.dot(query, self.W_q)  # (batch, seq_len_q, embed_dim)
        K = np.dot(key, self.W_k)    # (batch, seq_len_k, embed_dim)
        V = np.dot(value, self.W_v)  # (batch, seq_len_k, embed_dim)
        
        # Split into multiple heads
        Q = self._split_heads(Q)  # (batch, num_heads, seq_len_q, head_dim)
        K = self._split_heads(K)  # (batch, num_heads, seq_len_k, head_dim)
        V = self._split_heads(V)  # (batch, num_heads, seq_len_k, head_dim)
        
        # Scaled dot-product attention
        scores = np.matmul(Q, np.transpose(K, (0, 1, 3, 2)))  # (batch, num_heads, seq_len_q, seq_len_k)
        scores = scores / np.sqrt(self.head_dim)
        
        # Apply mask if provided
        if mask is not None:
            # Broadcast mask to match scores shape
            mask = mask[:, np.newaxis, :, :]  # (batch, 1, seq_len_q, seq_len_k)
            scores = np.where(mask, scores, -1e9)
        
        # Softmax over key dimension
        attention_weights = self._softmax(scores, axis=-1)
        
        # Apply attention to values
        context = np.matmul(attention_weights, V)  # (batch, num_heads, seq_len_q, head_dim)
        
        # Merge heads
        context = self._merge_heads(context)  # (batch, seq_len_q, embed_dim)
        
        # Final projection
        output = np.dot(context, self.W_o)
        
        return output
    
    def _softmax(self, x: np.ndarray, axis: int = -1) -> np.ndarray:
        """Numerically stable softmax."""
        x_max = np.max(x, axis=axis, keepdims=True)
        exp_x = np.exp(x - x_max)
        return exp_x / np.sum(exp_x, axis=axis, keepdims=True)
    
    def __call__(self, *args, **kwargs) -> np.ndarray:
        """Make the module callable."""
        return self.forward(*args, **kwargs)


class GraphAttention:
    """
    Graph attention for coupling space trajectories.
    
    Specialized attention mechanism for graph-structured holographic states,
    where nodes represent RG steps and edges represent flow dynamics.
    
    Based on Graph Attention Networks (GAT) adapted for IRH.
    """
    
    def __init__(
        self,
        node_dim: int = 64,
        edge_dim: int = 32,
        num_heads: int = 4,
        dropout_rate: float = 0.1
    ):
        """
        Initialize graph attention.
        
        Args:
            node_dim: Dimension of node features
            edge_dim: Dimension of edge features
            num_heads: Number of attention heads
            dropout_rate: Dropout probability
        """
        self.node_dim = node_dim
        self.edge_dim = edge_dim
        self.num_heads = num_heads
        self.dropout_rate = dropout_rate
        
        # Initialize weight matrices
        self.W_node = None
        self.W_edge = None
        self.a = None  # Attention coefficients
        
        self._initialize_weights()
    
    def _initialize_weights(self) -> None:
        """Initialize graph attention weights."""
        scale = 1.0 / np.sqrt(self.node_dim)
        
        self.W_node = np.random.randn(self.node_dim, self.node_dim) * scale
        self.W_edge = np.random.randn(self.edge_dim, self.node_dim) * scale
        # Attention vector size: 2 * node_dim (src + dst) + node_dim (edge transformed)
        self.a = np.random.randn(self.num_heads, 3 * self.node_dim) * scale
    
    def forward(
        self,
        node_features: np.ndarray,
        edge_features: np.ndarray,
        adjacency: np.ndarray
    ) -> np.ndarray:
        """
        Forward pass of graph attention.
        
        Args:
            node_features: Node features (num_nodes, node_dim)
            edge_features: Edge features (num_edges, edge_dim)
            adjacency: Adjacency matrix (num_edges, 2) - edge indices
            
        Returns:
            Updated node features (num_nodes, node_dim)
        """
        num_nodes = node_features.shape[0]
        num_edges = edge_features.shape[0]
        
        # Transform node features
        h = np.dot(node_features, self.W_node)  # (num_nodes, node_dim)
        
        # Transform edge features
        e = np.dot(edge_features, self.W_edge)  # (num_edges, node_dim)
        
        # Compute attention coefficients for each edge
        attention_logits = np.zeros((num_edges, self.num_heads))
        
        for i in range(num_edges):
            src_idx, dst_idx = adjacency[i]
            
            # Concatenate source node, destination node, and edge features
            concat_features = np.concatenate([
                h[src_idx],
                h[dst_idx],
                e[i]
            ])
            
            # Compute attention logit for each head
            for head in range(self.num_heads):
                attention_logits[i, head] = np.dot(self.a[head], concat_features)
        
        # Apply leaky ReLU
        attention_logits = np.maximum(0.01 * attention_logits, attention_logits)
        
        # Softmax per destination node
        attention_weights = self._softmax_per_node(
            attention_logits, adjacency[:, 1], num_nodes
        )
        
        # Aggregate neighbor features
        h_new = np.zeros_like(h)
        
        for i in range(num_edges):
            src_idx, dst_idx = adjacency[i]
            
            for head in range(self.num_heads):
                h_new[dst_idx] += attention_weights[i, head] * h[src_idx]
        
        # Average across heads
        h_new = h_new / self.num_heads
        
        return h_new
    
    def _softmax_per_node(
        self,
        logits: np.ndarray,
        dst_indices: np.ndarray,
        num_nodes: int
    ) -> np.ndarray:
        """
        Apply softmax separately for each destination node.
        
        Args:
            logits: Attention logits (num_edges, num_heads)
            dst_indices: Destination node indices (num_edges,)
            num_nodes: Total number of nodes
            
        Returns:
            Attention weights (num_edges, num_heads)
        """
        weights = np.zeros_like(logits)
        
        for node in range(num_nodes):
            # Find all edges pointing to this node
            mask = dst_indices == node
            
            if np.any(mask):
                # Apply softmax to logits for these edges
                node_logits = logits[mask]
                node_logits_max = np.max(node_logits, axis=0, keepdims=True)
                exp_logits = np.exp(node_logits - node_logits_max)
                node_weights = exp_logits / np.sum(exp_logits, axis=0, keepdims=True)
                
                weights[mask] = node_weights
        
        return weights
    
    def __call__(self, *args, **kwargs) -> np.ndarray:
        """Make the module callable."""
        return self.forward(*args, **kwargs)


class PositionalEncoding:
    """
    Positional encoding for RG scale sequences.
    
    Adapted from standard transformer positional encoding,
    specialized for encoding RG flow "time" (scale k).
    """
    
    def __init__(self, embed_dim: int = 128, max_len: int = 1000):
        """
        Initialize positional encoding.
        
        Args:
            embed_dim: Embedding dimension
            max_len: Maximum sequence length
        """
        self.embed_dim = embed_dim
        self.max_len = max_len
        
        # Create positional encoding matrix
        self.pe = self._create_positional_encoding()
    
    def _create_positional_encoding(self) -> np.ndarray:
        """
        Create sinusoidal positional encoding.
        
        Returns:
            Positional encoding matrix (max_len, embed_dim)
        """
        position = np.arange(self.max_len)[:, np.newaxis]
        div_term = np.exp(
            np.arange(0, self.embed_dim, 2) * 
            -(np.log(10000.0) / self.embed_dim)
        )
        
        pe = np.zeros((self.max_len, self.embed_dim))
        pe[:, 0::2] = np.sin(position * div_term)
        pe[:, 1::2] = np.cos(position * div_term)
        
        return pe
    
    def forward(self, x: np.ndarray) -> np.ndarray:
        """
        Add positional encoding to input.
        
        Args:
            x: Input tensor (batch, seq_len, embed_dim)
            
        Returns:
            Input with positional encoding added
        """
        seq_len = x.shape[1]
        
        if seq_len > self.max_len:
            raise ValueError(
                f"Sequence length ({seq_len}) exceeds max_len ({self.max_len})"
            )
        
        # Add positional encoding (broadcasting over batch dimension)
        return x + self.pe[np.newaxis, :seq_len, :]
    
    def __call__(self, x: np.ndarray) -> np.ndarray:
        """Make the module callable."""
        return self.forward(x)


# Example usage and validation
if __name__ == "__main__":
    print("Testing Attention Modules...")
    
    # Test 1: MultiHeadAttention
    print("\n1. Testing MultiHeadAttention...")
    mha = MultiHeadAttention(embed_dim=128, num_heads=8)
    
    batch_size, seq_len = 2, 10
    query = np.random.randn(batch_size, seq_len, 128)
    
    output = mha(query)
    assert output.shape == (batch_size, seq_len, 128)
    print(f"  ✓ Output shape: {output.shape}")
    
    # Test 2: GraphAttention
    print("\n2. Testing GraphAttention...")
    gat = GraphAttention(node_dim=64, edge_dim=32, num_heads=4)
    
    num_nodes, num_edges = 10, 15
    node_features = np.random.randn(num_nodes, 64)
    edge_features = np.random.randn(num_edges, 32)
    adjacency = np.random.randint(0, num_nodes, size=(num_edges, 2))
    
    output = gat(node_features, edge_features, adjacency)
    assert output.shape == (num_nodes, 64)
    print(f"  ✓ Output shape: {output.shape}")
    
    # Test 3: PositionalEncoding
    print("\n3. Testing PositionalEncoding...")
    pe = PositionalEncoding(embed_dim=128, max_len=1000)
    
    x = np.random.randn(2, 50, 128)
    output = pe(x)
    assert output.shape == (2, 50, 128)
    print(f"  ✓ Output shape: {output.shape}")
    
    # Test 4: Cross-attention (different Q, K, V)
    print("\n4. Testing Cross-Attention...")
    query = np.random.randn(2, 5, 128)
    key_value = np.random.randn(2, 10, 128)
    
    output = mha(query, key=key_value, value=key_value)
    assert output.shape == (2, 5, 128)
    print(f"  ✓ Cross-attention output shape: {output.shape}")
    
    print("\n✅ All attention module tests passed!")
