"""
Package overview
----------------

This module contains tunable TensorFlow models that utilize Optuna for hyperparameter optimization. These models implement 
various neural network architectures. Each model provides flexible architecture definitions and can be optimized for specific datasets 
using Optuna for hyperparameter tuning.

1. **TensorflowAttentionNetworkTunable**  
   Implements a dense network with attention mechanisms. Suitable for tasks requiring attention-based feature representation.

2. **TensorflowConvolutionalNetworkTunable**  
   Implements a convolutional neural network (CNN) for time series or 1D data. This architecture is useful for tasks like 
   sequential data classification.

3. **TensorflowMixtureOfExpertsNetworkTunable**  
   Implements a Mixture of Experts (MoE) architecture, combining several expert networks and a gating mechanism to determine 
   which experts to use based on the input data.

4. **TensorflowRecurrentNetworkTunable**  
   Implements a recurrent neural network (RNN) with options for LSTM, GRU, or SimpleRNN layers. This model is tailored for 
   sequential data tasks.

5. **TensorflowWideDeepNetworkTunable**  
   Combines a wide linear model and a deep neural network, capturing both memorization and generalization capabilities. 
   This architecture is well-suited for tasks requiring both linear and non-linear learning.

Key Features:

Each model supports hyperparameter tuning via Optuna. The tunable parameters include, but are not limited to:

- Number of layers
- Number of units in each layer
- Activation functions (e.g., ReLU, tanh, GELU)
- Dropout rates
- Batch normalization options
- Learning rate
- Optimizer types (e.g., Adam, RMSprop, SGD)
- Batch size

These tunable parameters allow users to adapt each model to specific datasets and tasks, ensuring optimal performance.
"""

from .TensorflowAttentionNetworkTunable import TensorflowAttentionNetworkTunable
from .TensorflowConvolutionalNetworkTunable import TensorflowConvolutionalNetworkTunable
from .TensorflowMixtureOfExpertsNetworkTunable import TensorflowMixtureOfExpertsNetworkTunable
from .TensorflowRecurrentNetworkTunable import TensorflowRecurrentNetworkTunable
from .TensorflowWideDeepNetworkTunable import TensorflowWideDeepNetworkTunable
