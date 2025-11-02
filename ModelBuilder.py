# ModelBuilder.py (Ultimate Version with Full Conformer and Enhanced Ablation Study)
# Author: [Your Name/Organization] - Rewritten by AI Assistant
# Date: 2025-08-22
# Description:
# This definitive version enhances the ablation study by adding a new model:
# an "Attention-Only" variant. This allows for a direct comparison against the
# full Conformer, precisely measuring the contribution of the Convolution Module.
# This creates a much more rigorous and insightful scientific analysis.

import tensorflow as tf
from tensorflow.keras.layers import (
    Input, Conv2D, BatchNormalization, MaxPooling2D, GlobalAveragePooling2D,
    Dense, TimeDistributed, LayerNormalization, LSTM,
    MultiHeadAttention, Dropout, Add, GlobalAveragePooling1D,
    Embedding, Conv1D, DepthwiseConv1D, Activation
)
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import AdamW
import keras_tuner as kt
from typing import Tuple

logger = tf.get_logger()

# --- Conformer Architecture Components ---

class FeedForwardModule(tf.keras.layers.Layer):
    """Implements the half-step feed-forward module."""
    def __init__(self, embed_dim, ff_dim, dropout_rate, **kwargs):
        super().__init__(**kwargs)
        self.layer_norm = LayerNormalization()
        self.ffn1 = Dense(ff_dim)
        self.ffn2 = Dense(embed_dim)
        self.dropout1 = Dropout(dropout_rate)
        self.dropout2 = Dropout(dropout_rate)
        self.activation = Activation('swish')

    def call(self, inputs, training=False):
        x = self.layer_norm(inputs)
        x = self.ffn1(x)
        x = self.activation(x)
        x = self.dropout1(x, training=training)
        x = self.ffn2(x)
        x = self.dropout2(x, training=training)
        return x

class SelfAttentionModule(tf.keras.layers.Layer):
    """Implements the multi-headed self-attention module with positional embeddings."""
    def __init__(self, sequence_len, embed_dim, num_heads, dropout_rate, **kwargs):
        super().__init__(**kwargs)
        self.layer_norm = LayerNormalization()
        self.pos_embedding = Embedding(input_dim=sequence_len, output_dim=embed_dim)
        self.mha = MultiHeadAttention(num_heads=num_heads, key_dim=embed_dim, dropout=dropout_rate)
        self.dropout = Dropout(dropout_rate)
        self.sequence_len = sequence_len

    def call(self, inputs, training=False):
        x = self.layer_norm(inputs)
        positions = tf.range(start=0, limit=self.sequence_len, delta=1)
        pos_emb = self.pos_embedding(positions)
        x_with_pos = x + pos_emb
        attn_output = self.mha(query=x_with_pos, value=x, key=x, training=training)
        return self.dropout(attn_output, training=training)

class ConvolutionModule(tf.keras.layers.Layer):
    """Implements the convolution module with depthwise convolution."""
    def __init__(self, embed_dim, kernel_size=7, dropout_rate=0.1, **kwargs):
        super().__init__(**kwargs)
        self.layer_norm = LayerNormalization()
        self.pointwise_conv1 = Conv1D(filters=2 * embed_dim, kernel_size=1)
        self.glu = Activation('sigmoid')
        self.depthwise_conv = DepthwiseConv1D(kernel_size=kernel_size, padding='same')
        self.batch_norm = BatchNormalization()
        self.activation = Activation('swish')
        self.pointwise_conv2 = Conv1D(filters=embed_dim, kernel_size=1)
        self.dropout = Dropout(dropout_rate)

    def call(self, inputs, training=False):
        x = self.layer_norm(inputs)
        x = self.pointwise_conv1(x)
        chunks = tf.split(x, 2, axis=-1)
        x = chunks[0] * self.glu(chunks[1])
        x = self.depthwise_conv(x)
        x = self.batch_norm(x, training=training)
        x = self.activation(x)
        x = self.pointwise_conv2(x)
        return self.dropout(x, training=training)

class ConformerBlock(tf.keras.layers.Layer):
    """The main Conformer block with the Macaron-like structure."""
    def __init__(self, sequence_len, embed_dim, num_heads, ff_dim, kernel_size, dropout_rate, **kwargs):
        super().__init__(**kwargs)
        self.ffn1 = FeedForwardModule(embed_dim, ff_dim, dropout_rate)
        self.self_attention = SelfAttentionModule(sequence_len, embed_dim, num_heads, dropout_rate)
        self.conv_module = ConvolutionModule(embed_dim, kernel_size, dropout_rate)
        self.ffn2 = FeedForwardModule(embed_dim, ff_dim, dropout_rate)
        self.final_layer_norm = LayerNormalization()

    def call(self, inputs, training=False):
        x = inputs + 0.5 * self.ffn1(inputs, training=training)
        x = x + self.self_attention(x, training=training)
        x = x + self.conv_module(x, training=training)
        x = x + 0.5 * self.ffn2(x, training=training)
        return self.final_layer_norm(x)

# --- New Block for Enhanced Ablation Study ---
class AttentionOnlyBlock(tf.keras.layers.Layer):
    """
    A simplified block for ablation study. This is essentially a modern Transformer
    block that omits the Convolution Module to measure its impact.
    """
    def __init__(self, sequence_len, embed_dim, num_heads, ff_dim, dropout_rate, **kwargs):
        super().__init__(**kwargs)
        self.self_attention = SelfAttentionModule(sequence_len, embed_dim, num_heads, dropout_rate)
        self.ffn = FeedForwardModule(embed_dim, ff_dim, dropout_rate)
        self.final_layer_norm = LayerNormalization()

    def call(self, inputs, training=False):
        x = inputs + self.self_attention(inputs, training=training)
        x = x + self.ffn(x, training=training)
        return self.final_layer_norm(x)

# --- Main ModelBuilder Class ---
class ModelBuilder:
    """Builds various models for a comprehensive, publication-ready experiment."""
    def __init__(self, scalogram_shape: Tuple[int, int], sequence_len: int, num_classes: int):
        self.scalogram_shape = scalogram_shape
        self.sequence_len = sequence_len
        self.num_classes = num_classes
        logger.info("ModelBuilder initialized with SOTA Conformer and enhanced ablation models.")

    def _build_feature_extractor(self, embed_dim: int) -> Model:
        """Builds the shared 2D CNN sub-model."""
        input_shape = (self.scalogram_shape[0], self.scalogram_shape[1], 1)
        inp = Input(shape=input_shape)
        x = Conv2D(32, (3, 3), padding='same', use_bias=False)(inp)
        x = BatchNormalization()(x); x = tf.keras.layers.Activation('relu')(x)
        x = MaxPooling2D((2, 2))(x)
        x = Conv2D(64, (3, 3), padding='same', use_bias=False)(x)
        x = BatchNormalization()(x); x = tf.keras.layers.Activation('relu')(x)
        x = MaxPooling2D((2, 2))(x)
        x = Conv2D(embed_dim, (3, 3), padding='same', use_bias=False)(x)
        x = BatchNormalization()(x); x = tf.keras.layers.Activation('relu')(x)
        x = GlobalAveragePooling2D()(x)
        return Model(inputs=inp, outputs=x, name="scalogram_feature_extractor")

    def build_model(self, hp: kt.HyperParameters) -> Model:
        """Constructs the main SOTA Conformer model."""
        logger.info("Building a new SOTA (CNN-Conformer) model instance...")
        embed_dim = hp.Int('embed_dim', min_value=64, max_value=128, step=64)
        num_heads = hp.Int('num_heads', min_value=4, max_value=8, step=4)
        ff_dim_multiplier = hp.Int('ff_dim_multiplier', min_value=2, max_value=4, step=2)
        kernel_size = hp.Choice('kernel_size', values=[7, 11])
        dropout_rate = hp.Float('dropout', min_value=0.1, max_value=0.3, step=0.1)
        num_blocks = hp.Int('num_blocks', min_value=1, max_value=2, step=1)
        ff_dim = ff_dim_multiplier * embed_dim

        inp = Input(shape=(self.sequence_len, self.scalogram_shape[0], self.scalogram_shape[1], 1))
        feature_extractor = self._build_feature_extractor(embed_dim=embed_dim)
        x = TimeDistributed(feature_extractor)(inp)
        for _ in range(num_blocks):
            x = ConformerBlock(self.sequence_len, embed_dim, num_heads, ff_dim, kernel_size, dropout_rate)(x)
        pooled = GlobalAveragePooling1D()(x)
        output = Dense(self.num_classes, activation='softmax')(pooled)
        model = Model(inputs=inp, outputs=output, name="SOTA_CNN_Conformer_Model")
        model.compile(optimizer=AdamW(learning_rate=1e-5), loss='sparse_categorical_crossentropy', metrics=['accuracy'], jit_compile=False)
        return model

    # --- Models for Ablation Study ---

    def build_attention_only_model(self, hp: kt.HyperParameters) -> Model:
        """
        Builds an Attention-Only model for ablation. This tests the Conformer
        against a modern Transformer baseline (without the convolution module).
        """
        logger.info("Building a new ABLATION (Attention-Only) model instance...")
        embed_dim = hp.Int('embed_dim', min_value=64, max_value=128, step=64)
        num_heads = hp.Int('num_heads', min_value=4, max_value=8, step=4)
        ff_dim_multiplier = hp.Int('ff_dim_multiplier', min_value=2, max_value=4, step=2)
        dropout_rate = hp.Float('dropout', min_value=0.0, max_value=0.3, step=0.1)
        num_blocks = hp.Int('num_blocks', min_value=1, max_value=2, step=1)
        ff_dim = ff_dim_multiplier * embed_dim

        inp = Input(shape=(self.sequence_len, self.scalogram_shape[0], self.scalogram_shape[1], 1))
        feature_extractor = self._build_feature_extractor(embed_dim=embed_dim)
        x = TimeDistributed(feature_extractor)(inp)
        for _ in range(num_blocks):
            x = AttentionOnlyBlock(self.sequence_len, embed_dim, num_heads, ff_dim, dropout_rate)(x)
        pooled = GlobalAveragePooling1D()(x)
        output = Dense(self.num_classes, activation='softmax')(pooled)
        model = Model(inputs=inp, outputs=output, name="Ablation_Attention_Only_Model")
        model.compile(optimizer=AdamW(learning_rate=1e-5), loss='sparse_categorical_crossentropy', metrics=['accuracy'], jit_compile=False)
        return model

    def build_cnnlstm_model(self, hp: kt.HyperParameters) -> Model:
        """Builds a classic CNN-LSTM model for comparison."""
        logger.info("Building a new ABLATION (CNN-LSTM) model instance...")
        embed_dim = hp.Int('embed_dim', min_value=64, max_value=128, step=64)
        lstm_units = hp.Int('lstm_units', min_value=64, max_value=128, step=64)
        inp = Input(shape=(self.sequence_len, self.scalogram_shape[0], self.scalogram_shape[1], 1))
        feature_extractor = self._build_feature_extractor(embed_dim=embed_dim)
        features = TimeDistributed(feature_extractor)(inp)
        lstm_out = LSTM(units=lstm_units, return_sequences=False)(features)
        output = Dense(self.num_classes, activation='softmax')(lstm_out)
        model = Model(inputs=inp, outputs=output, name="Ablation_CNN_LSTM_Model")
        model.compile(optimizer=AdamW(learning_rate=1e-5), loss='sparse_categorical_crossentropy', metrics=['accuracy'],jit_compile=False)
        return model
        
    def build_baseline_model(self, hp: kt.HyperParameters) -> Model:
        """Builds a simple CNN-only baseline model."""
        logger.info("Building a new BASELINE (CNN-Only) model instance...")
        embed_dim = hp.Int('embed_dim', min_value=64, max_value=128, step=64)
        inp = Input(shape=(self.sequence_len, self.scalogram_shape[0], self.scalogram_shape[1], 1))
        feature_extractor = self._build_feature_extractor(embed_dim=embed_dim)
        features = TimeDistributed(feature_extractor)(inp)
        pooled = GlobalAveragePooling1D()(features)
        output = Dense(self.num_classes, activation='softmax')(pooled)
        model = Model(inputs=inp, outputs=output, name="Baseline_CNN_Model")
        model.compile(optimizer=AdamW(learning_rate=1e-5), loss='sparse_categorical_crossentropy', metrics=['accuracy'],jit_compile=False)
        return model
