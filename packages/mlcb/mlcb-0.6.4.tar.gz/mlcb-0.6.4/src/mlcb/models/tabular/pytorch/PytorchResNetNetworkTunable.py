import torch
import torch.nn as nn
import numpy as np
import optuna
from typing import Dict, Union, Any

from ....base_classes.pytorch.PytorchTunable import PytorchTunable

class ResidualBlock(nn.Module):
    """
    Defines a residual block that performs two linear transformations, with optional batch normalization 
    and dropout, followed by a skip connection.
    
    Methods
    -------
    forward(x: torch.Tensor) -> torch.Tensor
        Defines the forward pass through the residual block.
    """

    def __init__(self, input_units: int, units: int, use_batch_normalization: bool, dropout_rate: float):
        """
        Initializes the ResidualBlock.

        Parameters
        ----------
        input_units : int
            Number of input features.
        units : int
            Number of units for the hidden layers.
        use_batch_normalization : bool
            Whether to use batch normalization in the block.
        dropout_rate : float
            Dropout rate (0 to disable dropout).
        """
        super(ResidualBlock, self).__init__()
        self.use_batch_normalization = use_batch_normalization
        self.dropout_rate = dropout_rate
        
        self.fc1 = nn.Linear(input_units, units)
        nn.init.kaiming_normal_(self.fc1.weight, mode='fan_in', nonlinearity='relu')
        
        if use_batch_normalization:
            self.bn1 = nn.BatchNorm1d(units)
        
        self.relu = nn.ReLU()
        
        if dropout_rate > 0:
            self.dropout = nn.Dropout(dropout_rate)
        
        self.fc2 = nn.Linear(units, units)
        nn.init.kaiming_normal_(self.fc2.weight, mode='fan_in', nonlinearity='relu')
        
        if use_batch_normalization:
            self.bn2 = nn.BatchNorm1d(units)
        
        self.transform_input = nn.Linear(input_units, units) if input_units != units else None

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Forward pass through the residual block.

        Parameters
        ----------
        x : torch.Tensor
            Input tensor.

        Returns
        -------
        torch.Tensor
            Output tensor after applying the residual block transformations.
        """
        identity = x
        
        if self.transform_input is not None:
            identity = self.transform_input(identity)

        out = self.fc1(x)
        
        if self.use_batch_normalization:
            out = self.bn1(out)
        
        out = self.relu(out)
        
        if self.dropout_rate > 0:
            out = self.dropout(out)
        
        out = self.fc2(out)
        
        if self.use_batch_normalization:
            out = self.bn2(out)
        
        out += identity
        out = self.relu(out)
        
        return out

class PytorchResNetNetworkTunable(PytorchTunable):
    """
    A tunable PyTorch model class implementing a ResNet-like architecture with residual blocks,
    with hyperparameter tuning via Optuna.

    Methods
    -------
    build_model(input_shape: tuple, hyperparameters: Dict[str, Any]) -> nn.Module
        Builds the ResNet-like model based on the provided input shape and hyperparameters.
    
    _suggest_hyperparameters(trial: optuna.Trial) -> Dict[str, Union[int, float, str]]
        Suggests a set of hyperparameters for the Optuna trial.
    """

    def build_model(self, input_shape: tuple, hyperparameters: Dict[str, Any]) -> nn.Module:
        """
        Builds the ResNet-like model based on the provided input shape and hyperparameters.

        Parameters
        ----------
        input_shape : tuple
            Shape of the input data.
        hyperparameters : Dict[str, Any]
            Dictionary containing model hyperparameters.
            Expected keys:
                - 'units': Number of units for each residual block.
                - 'n_residual_blocks': Number of residual blocks.
                - 'use_batch_normalization': Whether to use batch normalization.
                - 'dropout_rate': Dropout rate for regularization.

        Returns
        -------
        nn.Module
            A PyTorch ResNet-like model with residual blocks.
        """
        units: int = hyperparameters.get('units', 128)
        n_residual_blocks: int = hyperparameters.get('n_residual_blocks', 3)
        use_batch_normalization: bool = hyperparameters.get('use_batch_normalization', True)
        dropout_rate: float = hyperparameters.get('dropout_rate', 0.3)

        layers = []
        input_units = input_shape[0]
        output_shape = len(np.unique(self.test_labels))

        for _ in range(n_residual_blocks):
            residual_block = ResidualBlock(input_units, units, use_batch_normalization, dropout_rate)
            layers.append(residual_block)
            input_units = units

        layers.append(nn.Linear(units, output_shape))

        return nn.Sequential(*layers)

    def _suggest_hyperparameters(self, trial: optuna.Trial) -> Dict[str, Union[int, float, str]]:
        """
        Suggests a set of hyperparameters for the Optuna trial.

        Parameters
        ----------
        trial : optuna.Trial
            The Optuna trial instance for hyperparameter optimization.

        Returns
        -------
        Dict[str, Union[int, float, str]]
            A dictionary of suggested hyperparameters for tuning.
            Suggested keys include:
            - 'n_residual_blocks': Number of residual blocks in the network.
            - 'units': Number of units in each residual block.
            - 'use_batch_normalization': Whether to apply batch normalization.
            - 'dropout_rate': Dropout rate for regularization.
            - 'optimizer': Optimizer to use for training (e.g., 'adam', 'rmsprop').
            - 'learning_rate': Learning rate for the optimizer.
            - 'batch_size': Batch size for training.
        """
        return {
            'n_residual_blocks': trial.suggest_int('n_residual_blocks', 1, 10, step=1),
            'units': trial.suggest_int('units', 64, 512, step=64),
            'use_batch_normalization': trial.suggest_categorical('use_batch_normalization', [True, False]),
            'dropout_rate': trial.suggest_float('dropout_rate', 0.1, 0.5, step=0.1),
            'optimizer': trial.suggest_categorical('optimizer', ['adam', 'rmsprop', 'sgd', 'adamw']),
            'learning_rate': trial.suggest_float('learning_rate', 1e-4, 1e-2, log=True),
            'batch_size': trial.suggest_int('batch_size', 32, 128, step=32),
        }
