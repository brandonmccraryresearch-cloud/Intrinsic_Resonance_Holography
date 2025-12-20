"""
Holographic Encoder for RG Flow States

THEORETICAL FOUNDATION: IRH v21.1 §1.2-1.3
Inspired by AlphaGeometry's graph encoding

Encodes holographic states (RG trajectories in coupling space) into
learned representations suitable for transformer processing.

Key Components:
- Node embedding: Encode (λ̃, γ̃, μ̃, k) tuples
- Edge embedding: Encode beta function triplets
- Graph encoding: Process full RG trajectory as graph
- Positional encoding: Encode RG "time" (flow scale)
"""

from typing import Dict, List, Optional, Tuple
import numpy as np

try:
    from ..engines.holographic_state import CouplingState, HolographicState
    from .attention_modules import GraphAttention, PositionalEncoding
except (ImportError, ValueError):
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    from engines.holographic_state import CouplingState, HolographicState
    from attention_modules import GraphAttention, PositionalEncoding


class NodeEmbedding:
    """
    Embedding layer for coupling state nodes.
    
    Transforms (λ̃, γ̃, μ̃, k) tuples into fixed-dimensional embeddings.
    Uses learned projection + nonlinearity.
    """
    
    def __init__(self, input_dim: int = 4, embed_dim: int = 128):
        """
        Initialize node embedding.
        
        Args:
            input_dim: Input dimension (4 for λ̃, γ̃, μ̃, k)
            embed_dim: Output embedding dimension
        """
        self.input_dim = input_dim
        self.embed_dim = embed_dim
        
        # Initialize projection matrix
        scale = 1.0 / np.sqrt(input_dim)
        self.W = np.random.randn(input_dim, embed_dim) * scale
        self.b = np.zeros(embed_dim)
    
    def forward(self, node_features: np.ndarray) -> np.ndarray:
        """
        Embed node features.
        
        Args:
            node_features: Node features (num_nodes, input_dim)
            
        Returns:
            Node embeddings (num_nodes, embed_dim)
        """
        # Linear projection
        embeddings = np.dot(node_features, self.W) + self.b
        
        # ReLU activation
        embeddings = np.maximum(0, embeddings)
        
        return embeddings
    
    def __call__(self, node_features: np.ndarray) -> np.ndarray:
        """Make the module callable."""
        return self.forward(node_features)


class EdgeEmbedding:
    """
    Embedding layer for beta function edges.
    
    Transforms (β_λ, β_γ, β_μ) triplets into fixed-dimensional embeddings.
    """
    
    def __init__(self, input_dim: int = 3, embed_dim: int = 64):
        """
        Initialize edge embedding.
        
        Args:
            input_dim: Input dimension (3 for β_λ, β_γ, β_μ)
            embed_dim: Output embedding dimension
        """
        self.input_dim = input_dim
        self.embed_dim = embed_dim
        
        # Initialize projection matrix
        scale = 1.0 / np.sqrt(input_dim)
        self.W = np.random.randn(input_dim, embed_dim) * scale
        self.b = np.zeros(embed_dim)
    
    def forward(self, edge_features: np.ndarray) -> np.ndarray:
        """
        Embed edge features.
        
        Args:
            edge_features: Edge features (num_edges, input_dim)
            
        Returns:
            Edge embeddings (num_edges, embed_dim)
        """
        # Linear projection
        embeddings = np.dot(edge_features, self.W) + self.b
        
        # ReLU activation
        embeddings = np.maximum(0, embeddings)
        
        return embeddings
    
    def __call__(self, edge_features: np.ndarray) -> np.ndarray:
        """Make the module callable."""
        return self.forward(edge_features)


class HolographicEncoder:
    """
    Complete encoder for holographic states.
    
    Adapted from AlphaGeometry's graph encoding approach.
    Processes RG trajectory graphs into learned representations.
    
    Architecture:
    1. Node embedding (coupling states)
    2. Edge embedding (beta functions)
    3. Graph attention layers
    4. Positional encoding (RG scale)
    5. Output projection
    
    Attributes:
        node_dim: Node feature dimension
        edge_dim: Edge feature dimension
        embed_dim: Hidden embedding dimension
        num_layers: Number of graph attention layers
        num_heads: Number of attention heads per layer
    """
    
    def __init__(
        self,
        node_dim: int = 4,
        edge_dim: int = 3,
        embed_dim: int = 128,
        num_layers: int = 3,
        num_heads: int = 4,
        dropout_rate: float = 0.1
    ):
        """
        Initialize holographic encoder.
        
        Args:
            node_dim: Dimension of node features (λ̃, γ̃, μ̃, k)
            edge_dim: Dimension of edge features (β_λ, β_γ, β_μ)
            embed_dim: Hidden embedding dimension
            num_layers: Number of graph attention layers
            num_heads: Number of attention heads
            dropout_rate: Dropout probability
        """
        self.node_dim = node_dim
        self.edge_dim = edge_dim
        self.embed_dim = embed_dim
        self.num_layers = num_layers
        self.num_heads = num_heads
        self.dropout_rate = dropout_rate
        
        # Initialize submodules
        self.node_embedding = NodeEmbedding(
            input_dim=node_dim,
            embed_dim=embed_dim
        )
        
        self.edge_embedding = EdgeEmbedding(
            input_dim=edge_dim,
            embed_dim=embed_dim // 2  # Edge embeddings are smaller
        )
        
        self.graph_layers = [
            GraphAttention(
                node_dim=embed_dim,
                edge_dim=embed_dim // 2,
                num_heads=num_heads,
                dropout_rate=dropout_rate
            )
            for _ in range(num_layers)
        ]
        
        self.positional_encoding = PositionalEncoding(
            embed_dim=embed_dim,
            max_len=1000
        )
        
        # Output projection
        self.output_projection = self._create_output_projection()
    
    def _create_output_projection(self) -> np.ndarray:
        """Create output projection matrix."""
        scale = 1.0 / np.sqrt(self.embed_dim)
        return np.random.randn(self.embed_dim, self.embed_dim) * scale
    
    def encode_holographic_state(
        self,
        state: HolographicState
    ) -> Tuple[np.ndarray, Dict]:
        """
        Encode a holographic state into learned representation.
        
        Args:
            state: Holographic state to encode
            
        Returns:
            (encoding, metadata)
            - encoding: Encoded representation (seq_len, embed_dim)
            - metadata: Additional information (attention weights, etc.)
        """
        # Convert state to graph representation
        graph = state.to_graph_representation()
        
        return self.encode_graph(
            node_features=graph['node_features'],
            edge_features=graph['edge_features'],
            adjacency=graph['adjacency']
        )
    
    def encode_graph(
        self,
        node_features: np.ndarray,
        edge_features: np.ndarray,
        adjacency: np.ndarray
    ) -> Tuple[np.ndarray, Dict]:
        """
        Encode graph representation.
        
        Args:
            node_features: Node features (num_nodes, node_dim)
            edge_features: Edge features (num_edges, edge_dim)
            adjacency: Adjacency matrix (num_edges, 2)
            
        Returns:
            (encoding, metadata)
            - encoding: Encoded representation (num_nodes, embed_dim)
            - metadata: Additional information
        """
        num_nodes = node_features.shape[0]
        
        # Step 1: Embed nodes and edges
        node_embeddings = self.node_embedding(node_features)
        
        if edge_features.shape[0] > 0:
            edge_embeddings = self.edge_embedding(edge_features)
        else:
            # Handle single-node case
            edge_embeddings = np.zeros((0, self.embed_dim // 2))
        
        # Step 2: Apply graph attention layers
        h = node_embeddings
        attention_weights = []
        
        for layer in self.graph_layers:
            if edge_embeddings.shape[0] > 0:
                h_new = layer(h, edge_embeddings, adjacency)
                
                # Residual connection
                h = h + h_new
                
                # Layer normalization
                h = self._layer_norm(h)
            else:
                # Skip graph attention for single node
                pass
        
        # Step 3: Add positional encoding
        # Reshape to (batch=1, seq_len, embed_dim) for positional encoding
        h = h[np.newaxis, :, :]
        h = self.positional_encoding(h)
        h = h[0, :, :]  # Remove batch dimension
        
        # Step 4: Output projection
        output = np.dot(h, self.output_projection)
        
        # Compile metadata
        metadata = {
            'num_nodes': num_nodes,
            'num_edges': edge_features.shape[0],
            'attention_weights': attention_weights,
            'input_shapes': {
                'nodes': node_features.shape,
                'edges': edge_features.shape,
                'adjacency': adjacency.shape
            }
        }
        
        return output, metadata
    
    def _layer_norm(self, x: np.ndarray, eps: float = 1e-6) -> np.ndarray:
        """
        Apply layer normalization.
        
        Args:
            x: Input tensor (..., embed_dim)
            eps: Small constant for numerical stability
            
        Returns:
            Normalized tensor
        """
        mean = np.mean(x, axis=-1, keepdims=True)
        std = np.std(x, axis=-1, keepdims=True)
        return (x - mean) / (std + eps)
    
    def encode_batch(
        self,
        states: List[HolographicState]
    ) -> Tuple[List[np.ndarray], List[Dict]]:
        """
        Encode a batch of holographic states.
        
        Args:
            states: List of holographic states
            
        Returns:
            (encodings, metadatas)
            - encodings: List of encoded representations
            - metadatas: List of metadata dicts
        """
        encodings = []
        metadatas = []
        
        for state in states:
            encoding, metadata = self.encode_holographic_state(state)
            encodings.append(encoding)
            metadatas.append(metadata)
        
        return encodings, metadatas
    
    def __call__(
        self,
        state_or_graph,
        **kwargs
    ) -> Tuple[np.ndarray, Dict]:
        """
        Make the encoder callable.
        
        Args:
            state_or_graph: Either HolographicState or graph dict
            **kwargs: Additional arguments
            
        Returns:
            (encoding, metadata)
        """
        if isinstance(state_or_graph, HolographicState):
            return self.encode_holographic_state(state_or_graph)
        elif isinstance(state_or_graph, dict):
            # Extract the graph components
            return self.encode_graph(
                node_features=state_or_graph['node_features'],
                edge_features=state_or_graph['edge_features'],
                adjacency=state_or_graph['adjacency']
            )
        else:
            raise TypeError(
                f"Expected HolographicState or dict, got {type(state_or_graph)}"
            )


# Example usage and validation
if __name__ == "__main__":
    print("Testing HolographicEncoder...")
    
    # Create a sample holographic state
    from engines.holographic_state import CouplingState, HolographicState
    
    initial = CouplingState(
        lambda_tilde=10.0,
        gamma_tilde=10.0,
        mu_tilde=10.0,
        k=1.0
    )
    
    state = HolographicState(initial)
    
    # Add some RG flow steps
    for i in range(5):
        new_state = CouplingState(
            lambda_tilde=10.0 - 0.5 * (i + 1),
            gamma_tilde=10.0 - 0.5 * (i + 1),
            mu_tilde=10.0 - 0.5 * (i + 1),
            k=1.0 - 0.1 * (i + 1)
        )
        beta_funcs = (-0.5, -0.5, -0.5)
        state.add_rg_step(new_state, beta_functions=beta_funcs)
    
    # Test 1: Basic encoding
    print("\n1. Testing basic encoding...")
    encoder = HolographicEncoder(
        node_dim=4,
        edge_dim=3,
        embed_dim=128,
        num_layers=3,
        num_heads=4
    )
    
    encoding, metadata = encoder(state)
    print(f"  ✓ Encoding shape: {encoding.shape}")
    print(f"  ✓ Num nodes: {metadata['num_nodes']}")
    print(f"  ✓ Num edges: {metadata['num_edges']}")
    
    # Test 2: Single node case
    print("\n2. Testing single node encoding...")
    single_state = HolographicState(initial)
    encoding_single, metadata_single = encoder(single_state)
    print(f"  ✓ Single node encoding shape: {encoding_single.shape}")
    assert encoding_single.shape[0] == 1
    
    # Test 3: Batch encoding
    print("\n3. Testing batch encoding...")
    states = [state, single_state]
    encodings, metadatas = encoder.encode_batch(states)
    print(f"  ✓ Batch size: {len(encodings)}")
    print(f"  ✓ Encoding 0 shape: {encodings[0].shape}")
    print(f"  ✓ Encoding 1 shape: {encodings[1].shape}")
    
    # Test 4: Direct graph encoding
    print("\n4. Testing direct graph encoding...")
    graph = state.to_graph_representation()
    encoding_graph, metadata_graph = encoder(graph)
    print(f"  ✓ Graph encoding shape: {encoding_graph.shape}")
    
    # Verify consistency
    assert np.allclose(encoding, encoding_graph, atol=1e-6)
    print("  ✓ State and graph encoding consistent")
    
    # Test 5: Node and edge embedding dimensions
    print("\n5. Testing embedding dimensions...")
    node_emb = encoder.node_embedding(graph['node_features'])
    print(f"  ✓ Node embedding shape: {node_emb.shape}")
    assert node_emb.shape == (6, 128)
    
    if graph['edge_features'].shape[0] > 0:
        edge_emb = encoder.edge_embedding(graph['edge_features'])
        print(f"  ✓ Edge embedding shape: {edge_emb.shape}")
        assert edge_emb.shape == (5, 64)
    
    print("\n✅ All HolographicEncoder tests passed!")
