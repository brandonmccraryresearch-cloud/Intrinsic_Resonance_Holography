"""
Resonance Decoder for RG Flow Predictions

THEORETICAL FOUNDATION: IRH v21.1 §1.2-1.3
Inspired by AlphaGeometry's decoder architecture

Decodes learned holographic representations into predictions:
- Final coupling constants (λ̃, γ̃, μ̃) at target scale
- Fixed point detection
- RG trajectory forecasting
- Action functional values

Architecture:
- Multi-layer decoder with self-attention
- Cross-attention between encoded state and target queries
- Feed-forward prediction heads
"""

from typing import Dict, List, Optional, Tuple
import numpy as np

try:
    from .attention_modules import MultiHeadAttention
except (ImportError, ValueError):
    import sys
    import os
    sys.path.append(os.path.dirname(__file__))
    from attention_modules import MultiHeadAttention


class FeedForward:
    """
    Feed-forward network for transformer decoder.
    
    Standard two-layer MLP with ReLU activation.
    """
    
    def __init__(
        self,
        embed_dim: int = 128,
        ff_dim: int = 512,
        dropout_rate: float = 0.1
    ):
        """
        Initialize feed-forward network.
        
        Args:
            embed_dim: Input/output embedding dimension
            ff_dim: Hidden dimension
            dropout_rate: Dropout probability
        """
        self.embed_dim = embed_dim
        self.ff_dim = ff_dim
        self.dropout_rate = dropout_rate
        
        # Initialize weights
        scale1 = 1.0 / np.sqrt(embed_dim)
        scale2 = 1.0 / np.sqrt(ff_dim)
        
        self.W1 = np.random.randn(embed_dim, ff_dim) * scale1
        self.b1 = np.zeros(ff_dim)
        
        self.W2 = np.random.randn(ff_dim, embed_dim) * scale2
        self.b2 = np.zeros(embed_dim)
    
    def forward(self, x: np.ndarray) -> np.ndarray:
        """
        Forward pass of feed-forward network.
        
        Args:
            x: Input tensor (..., embed_dim)
            
        Returns:
            Output tensor (..., embed_dim)
        """
        # First layer with ReLU
        h = np.dot(x, self.W1) + self.b1
        h = np.maximum(0, h)
        
        # Second layer
        output = np.dot(h, self.W2) + self.b2
        
        return output
    
    def __call__(self, x: np.ndarray) -> np.ndarray:
        """Make the module callable."""
        return self.forward(x)


class DecoderLayer:
    """
    Single transformer decoder layer.
    
    Architecture:
    1. Self-attention with residual + layer norm
    2. Cross-attention with residual + layer norm
    3. Feed-forward with residual + layer norm
    """
    
    def __init__(
        self,
        embed_dim: int = 128,
        num_heads: int = 8,
        ff_dim: int = 512,
        dropout_rate: float = 0.1
    ):
        """
        Initialize decoder layer.
        
        Args:
            embed_dim: Embedding dimension
            num_heads: Number of attention heads
            ff_dim: Feed-forward hidden dimension
            dropout_rate: Dropout probability
        """
        self.embed_dim = embed_dim
        self.num_heads = num_heads
        self.ff_dim = ff_dim
        self.dropout_rate = dropout_rate
        
        # Initialize sublayers
        self.self_attention = MultiHeadAttention(
            embed_dim=embed_dim,
            num_heads=num_heads,
            dropout_rate=dropout_rate
        )
        
        self.cross_attention = MultiHeadAttention(
            embed_dim=embed_dim,
            num_heads=num_heads,
            dropout_rate=dropout_rate
        )
        
        self.feed_forward = FeedForward(
            embed_dim=embed_dim,
            ff_dim=ff_dim,
            dropout_rate=dropout_rate
        )
    
    def forward(
        self,
        query: np.ndarray,
        memory: np.ndarray,
        query_mask: Optional[np.ndarray] = None,
        memory_mask: Optional[np.ndarray] = None
    ) -> np.ndarray:
        """
        Forward pass of decoder layer.
        
        Args:
            query: Query tensor (batch, seq_len_q, embed_dim)
            memory: Memory tensor from encoder (batch, seq_len_m, embed_dim)
            query_mask: Self-attention mask
            memory_mask: Cross-attention mask
            
        Returns:
            Output tensor (batch, seq_len_q, embed_dim)
        """
        # Self-attention block
        attn_output = self.self_attention(query, mask=query_mask)
        query = query + attn_output  # Residual
        query = self._layer_norm(query)
        
        # Cross-attention block
        cross_output = self.cross_attention(
            query=query,
            key=memory,
            value=memory,
            mask=memory_mask
        )
        query = query + cross_output  # Residual
        query = self._layer_norm(query)
        
        # Feed-forward block
        ff_output = self.feed_forward(query)
        query = query + ff_output  # Residual
        query = self._layer_norm(query)
        
        return query
    
    def _layer_norm(self, x: np.ndarray, eps: float = 1e-6) -> np.ndarray:
        """Apply layer normalization."""
        mean = np.mean(x, axis=-1, keepdims=True)
        std = np.std(x, axis=-1, keepdims=True)
        return (x - mean) / (std + eps)
    
    def __call__(self, *args, **kwargs) -> np.ndarray:
        """Make the layer callable."""
        return self.forward(*args, **kwargs)


class ResonanceDecoder:
    """
    Complete decoder for resonance predictions.
    
    Adapted from AlphaGeometry's decoder architecture.
    Predicts final states from encoded RG trajectories.
    
    Prediction Heads:
    1. Coupling prediction: (λ̃, γ̃, μ̃) at target scale
    2. Fixed point classification: Is this a fixed point?
    3. Trajectory prediction: Next N steps of RG flow
    4. Action prediction: cGFT action functional value
    
    Attributes:
        embed_dim: Embedding dimension
        num_layers: Number of decoder layers
        num_heads: Number of attention heads
        output_dim: Dimension of output predictions
    """
    
    def __init__(
        self,
        embed_dim: int = 128,
        num_layers: int = 3,
        num_heads: int = 8,
        ff_dim: int = 512,
        dropout_rate: float = 0.1,
        output_dim: int = 3  # (λ̃, γ̃, μ̃)
    ):
        """
        Initialize resonance decoder.
        
        Args:
            embed_dim: Embedding dimension
            num_layers: Number of decoder layers
            num_heads: Number of attention heads
            ff_dim: Feed-forward hidden dimension
            dropout_rate: Dropout probability
            output_dim: Output prediction dimension
        """
        self.embed_dim = embed_dim
        self.num_layers = num_layers
        self.num_heads = num_heads
        self.ff_dim = ff_dim
        self.dropout_rate = dropout_rate
        self.output_dim = output_dim
        
        # Initialize decoder layers
        self.layers = [
            DecoderLayer(
                embed_dim=embed_dim,
                num_heads=num_heads,
                ff_dim=ff_dim,
                dropout_rate=dropout_rate
            )
            for _ in range(num_layers)
        ]
        
        # Initialize prediction heads
        self._initialize_heads()
    
    def _initialize_heads(self) -> None:
        """Initialize prediction head weights."""
        scale = 1.0 / np.sqrt(self.embed_dim)
        
        # Coupling prediction head
        self.coupling_head = {
            'W': np.random.randn(self.embed_dim, self.output_dim) * scale,
            'b': np.zeros(self.output_dim)
        }
        
        # Fixed point classification head (binary)
        self.fixed_point_head = {
            'W': np.random.randn(self.embed_dim, 1) * scale,
            'b': np.zeros(1)
        }
        
        # Action prediction head (scalar)
        self.action_head = {
            'W': np.random.randn(self.embed_dim, 1) * scale,
            'b': np.zeros(1)
        }
    
    def forward(
        self,
        encoded_state: np.ndarray,
        target_queries: Optional[np.ndarray] = None
    ) -> Dict[str, np.ndarray]:
        """
        Forward pass of decoder.
        
        Args:
            encoded_state: Encoded RG trajectory (seq_len, embed_dim)
            target_queries: Optional target query embeddings
            
        Returns:
            Dictionary of predictions:
            - 'couplings': Predicted (λ̃, γ̃, μ̃) 
            - 'is_fixed_point': Fixed point probability
            - 'action': Predicted action value
        """
        # Add batch dimension if needed
        if encoded_state.ndim == 2:
            encoded_state = encoded_state[np.newaxis, :, :]
        
        batch_size, seq_len, _ = encoded_state.shape
        
        # Initialize queries if not provided
        if target_queries is None:
            # Use learnable queries (in real implementation)
            # Here we use the final encoded state as query
            target_queries = encoded_state[:, -1:, :]
        
        # Pass through decoder layers
        hidden = target_queries
        for layer in self.layers:
            hidden = layer(
                query=hidden,
                memory=encoded_state
            )
        
        # Apply prediction heads
        # Take the final query output
        final_hidden = hidden[:, -1, :]  # (batch, embed_dim)
        
        predictions = {
            'couplings': self._predict_couplings(final_hidden),
            'is_fixed_point': self._predict_fixed_point(final_hidden),
            'action': self._predict_action(final_hidden)
        }
        
        # Remove batch dimension for single inputs
        if batch_size == 1:
            for key in predictions:
                predictions[key] = predictions[key][0]
        
        return predictions
    
    def _predict_couplings(self, hidden: np.ndarray) -> np.ndarray:
        """
        Predict coupling constants.
        
        Args:
            hidden: Hidden state (batch, embed_dim)
            
        Returns:
            Predicted couplings (batch, output_dim)
        """
        couplings = np.dot(hidden, self.coupling_head['W']) + self.coupling_head['b']
        return couplings
    
    def _predict_fixed_point(self, hidden: np.ndarray) -> np.ndarray:
        """
        Predict fixed point probability.
        
        Args:
            hidden: Hidden state (batch, embed_dim)
            
        Returns:
            Fixed point probability (batch, 1)
        """
        logit = np.dot(hidden, self.fixed_point_head['W']) + self.fixed_point_head['b']
        # Apply sigmoid
        prob = 1.0 / (1.0 + np.exp(-logit))
        return prob
    
    def _predict_action(self, hidden: np.ndarray) -> np.ndarray:
        """
        Predict action functional value.
        
        Args:
            hidden: Hidden state (batch, embed_dim)
            
        Returns:
            Predicted action (batch, 1)
        """
        action = np.dot(hidden, self.action_head['W']) + self.action_head['b']
        return action
    
    def predict_trajectory(
        self,
        encoded_state: np.ndarray,
        num_steps: int = 10
    ) -> np.ndarray:
        """
        Predict future RG trajectory.
        
        Args:
            encoded_state: Encoded current state (seq_len, embed_dim)
            num_steps: Number of future steps to predict
            
        Returns:
            Predicted trajectory (num_steps, output_dim)
        """
        trajectory = []
        
        # Autoregressive prediction
        current_encoding = encoded_state
        
        for _ in range(num_steps):
            # Predict next step
            predictions = self.forward(current_encoding)
            next_coupling = predictions['couplings']
            
            trajectory.append(next_coupling)
            
            # Update encoding (simplified - in real implementation,
            # would re-encode with new state)
            # Here we just append
            # current_encoding = ... (would need encoder)
        
        return np.array(trajectory)
    
    def __call__(self, *args, **kwargs) -> Dict[str, np.ndarray]:
        """Make the decoder callable."""
        return self.forward(*args, **kwargs)


# Example usage and validation
if __name__ == "__main__":
    print("Testing ResonanceDecoder...")
    
    # Test 1: Basic decoding
    print("\n1. Testing basic decoding...")
    decoder = ResonanceDecoder(
        embed_dim=128,
        num_layers=3,
        num_heads=8,
        output_dim=3
    )
    
    # Create dummy encoded state
    seq_len = 10
    encoded_state = np.random.randn(seq_len, 128)
    
    predictions = decoder(encoded_state)
    
    print(f"  ✓ Coupling predictions shape: {predictions['couplings'].shape}")
    print(f"  ✓ Fixed point probability: {predictions['is_fixed_point']}")
    print(f"  ✓ Action prediction: {predictions['action']}")
    
    assert predictions['couplings'].shape == (3,)
    assert 0 <= predictions['is_fixed_point'] <= 1
    
    # Test 2: Batch decoding
    print("\n2. Testing batch decoding...")
    batch_size = 4
    encoded_batch = np.random.randn(batch_size, seq_len, 128)
    
    predictions_batch = decoder(encoded_batch)
    
    print(f"  ✓ Batch coupling predictions: {predictions_batch['couplings'].shape}")
    print(f"  ✓ Batch fixed point probs: {predictions_batch['is_fixed_point'].shape}")
    print(f"  ✓ Batch action predictions: {predictions_batch['action'].shape}")
    
    assert predictions_batch['couplings'].shape == (batch_size, 3)
    assert predictions_batch['is_fixed_point'].shape == (batch_size, 1)
    assert predictions_batch['action'].shape == (batch_size, 1)
    
    # Test 3: Trajectory prediction
    print("\n3. Testing trajectory prediction...")
    trajectory = decoder.predict_trajectory(encoded_state, num_steps=5)
    
    print(f"  ✓ Trajectory shape: {trajectory.shape}")
    assert trajectory.shape == (5, 3)
    
    # Test 4: DecoderLayer standalone
    print("\n4. Testing DecoderLayer...")
    layer = DecoderLayer(embed_dim=128, num_heads=8)
    
    query = np.random.randn(2, 5, 128)
    memory = np.random.randn(2, 10, 128)
    
    output = layer(query, memory)
    
    print(f"  ✓ Layer output shape: {output.shape}")
    assert output.shape == (2, 5, 128)
    
    # Test 5: FeedForward standalone
    print("\n5. Testing FeedForward...")
    ff = FeedForward(embed_dim=128, ff_dim=512)
    
    x = np.random.randn(2, 10, 128)
    output = ff(x)
    
    print(f"  ✓ FeedForward output shape: {output.shape}")
    assert output.shape == (2, 10, 128)
    
    print("\n✅ All ResonanceDecoder tests passed!")
