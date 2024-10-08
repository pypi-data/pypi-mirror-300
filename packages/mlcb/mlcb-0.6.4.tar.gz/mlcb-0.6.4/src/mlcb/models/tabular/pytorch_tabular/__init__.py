
"""
Package overview
----------------

This module contains tunable PyTorch Tabular neural network architectures for tabular data-based classification tasks,
with hyperparameter optimization support via Optuna.

Each model implements a different architecture suited for tabular datasets, allowing users to experiment 
with various configurations and hyperparameters. The networks offer flexibility in terms of activation 
functions, layer dimensions, and regularization, while supporting Optuna for hyperparameter tuning.

1. **PyTorchTabularAutoIntNetworkTunable**
   - Implements the AutoInt architecture with attention-based interactions for tabular data.

2. **PyTorchTabularCategoryEmbeddingNetworkTunable**
   - Uses category embeddings to handle categorical variables effectively in tabular data.

3. **PyTorchTabularDANetNetworkTunable**
   - Based on the DANet architecture, which focuses on hierarchical feature extraction and abstraction.

4. **PyTorchTabularGANDALFNetworkTunable**
   - Implements the GANDALF architecture, focusing on generalized attention and feature learning for tabular data.

Key Features:

All models support hyperparameter tuning via Optuna, allowing users to experiment with various configurations such as:
- Number of layers
- Attention blocks (for attention-based models)
- Dropout rate
- Activation functions
- Embedding dimensions (for categorical data)
- Optimizers (Adam, RMSprop, SGD)
- Learning rate and batch size
"""

from .PyTorchTabularAutoIntNetworkTunable import PyTorchTabularAutoIntNetworkTunable
from .PyTorchTabularCategoryEmbeddingNetworkTunable import PyTorchTabularCategoryEmbeddingNetworkTunable
from .PyTorchTabularDANetNetworkTunable import PyTorchTabularDANetNetworkTunable
from .PyTorchTabularGANDALFNetworkTunable import PyTorchTabularGANDALFNetworkTunable
