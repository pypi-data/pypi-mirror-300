"""
Package overview
----------------

This module contains tunable PyTorch network implementations with integrated hyperparameter optimization using Optuna. 
Each network can be customized and optimized for a classification, leveraging different neural network architectures.

- **PytorchDenseNetworkTunable**: 
    A tunable densely connected neural network with customizable growth rates and layer configurations for tasks requiring high model capacity.
    
- **PytorchFeedForwardNetworkTunable**: 
    A tunable feedforward neural network that allows customization of the number of layers and units.
    
- **PytorchMixtureOfExpertsNetworkTunable**: 
    A tunable Mixture of Experts (MoE) architecture, ideal for complex tasks that require dynamic expert selection for different inputs.
    
- **PytorchResNetNetworkTunable**: 
    A tunable Residual Network (ResNet) architecture designed to tackle deep learning tasks by using skip connections to improve training stability.
    
- **PytorchSelfNormalizingNetworkTunable**: 
    A tunable Self-Normalizing Neural Network (SNN) architecture that utilizes SELU activations and AlphaDropout to maintain self-normalization during training, improving model robustness.
    
- **PytorchTangentKernelNetworkTunable**: 
    A tunable tangent kernel-like network with fixed first-layer weights that mimics tangent kernel properties for specific applications requiring such architectures.
    
- **PytorchWideAndDeepNetworkTunable**: 
    A tunable wide and deep architecture combining linear and deep components to capture both shallow and deep feature interactions.

Key Features:

- **Hyperparameter Tuning**: 
    All models are integrated with Optuna for hyperparameter tuning, enabling automatic optimization of key parameters such as layer depth, number of units, learning rates, dropout rates, and activation functions.
    
- **Customization**: 
    Each model supports extensive customization, allowing users to adjust architectural elements to suit specific datasets and task requirements.

All models are implemented using PyTorch and support seamless integration with Optuna for hyperparameter optimization.
"""

from .PytorchDenseNetworkTunable import PytorchDenseNetTunable
from .PytorchFeedForwardNetworkTunable import PytorchFeedForwardNetworkTunable
from .PytorchMixtureOfExpertsNetworkTunable import PytorchMoETunable
from .PytorchResNetNetworkTunable import PytorchResNetNetworkTunable
from .PytorchSelfNormalizingNetworkTunable import PytorchSelfNormalizingNetworkTunable
from .PytorchTangentKernelNetworkTunable import PytorchTangentKernelNetworkTunable
from .PytorchWideDeepNetworkTunable import PytorchWideAndDeepNetworkTunable
