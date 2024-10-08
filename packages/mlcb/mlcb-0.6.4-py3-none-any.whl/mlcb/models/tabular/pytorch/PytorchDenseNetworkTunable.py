import numpy as np
import torch.nn as nn
import optuna
from typing import Dict, Union, Any

from ....base_classes.pytorch.PytorchTunable import PytorchTunable

class PytorchDenseNetTunable(PytorchTunable):
    """
    A tunable PyTorch DenseNet-like model class with hyperparameter tuning via Optuna.

    The model architecture includes customizable layers, growth rate, and optional batch normalization and dropout.
    It is designed for flexibility, allowing the user to specify various aspects of the network's structure.

    Methods
    -------
    build_model(input_shape: tuple, hyperparameters: Dict[str, Any]) -> nn.Module
        Builds the dense neural network model with specified hyperparameters.

    _suggest_hyperparameters(trial: optuna.Trial) -> Dict[str, Union[int, float, str]]
        Suggests a set of hyperparameters for Optuna-based tuning.

    _get_activation_function(activation_name: str) -> nn.Module
        Retrieves the corresponding PyTorch activation function based on the provided name.
    """

    def build_model(self, input_shape: tuple, hyperparameters: Dict[str, Any]) -> nn.Module:
        """
        Builds the dense neural network model based on the provided input shape and hyperparameters.

        Parameters
        ----------
        input_shape : tuple
            The shape of the input data, typically the feature dimension.
        hyperparameters : Dict[str, Any]
            A dictionary of model hyperparameters.
            Expected keys:
                - 'n_layers': Number of layers in the network.
                - 'growth_rate': Number of neurons added to each subsequent layer.
                - 'activation': Activation function to use (e.g., 'relu', 'tanh', etc.).
                - 'use_batch_normalization': Whether to use batch normalization after each layer.
                - 'dropout_rate': Dropout rate for regularization.

        Returns
        -------
        nn.Module
            A PyTorch dense neural network model built based on the specified hyperparameters.
        """
        n_layers: int = hyperparameters.get('n_layers', 3)
        growth_rate: int = hyperparameters.get('growth_rate', 32)
        activation: nn.Module = self._get_activation_function(hyperparameters.get('activation', 'relu'))
        use_batch_normalization: bool = hyperparameters.get('use_batch_normalization', True)
        dropout_rate: float = hyperparameters.get('dropout_rate', 0.3)

        layers = []
        input_units = input_shape[0]
        output_shape = len(np.unique(self.test_labels))

        for _ in range(n_layers):
            layer = nn.Linear(input_units, growth_rate)
            layers.append(layer)

            if use_batch_normalization:
                layers.append(nn.BatchNorm1d(growth_rate))

            layers.append(activation)

            if dropout_rate > 0:
                layers.append(nn.Dropout(dropout_rate))

            input_units = growth_rate

        layers.append(nn.Linear(input_units, output_shape))

        return nn.Sequential(*layers)

    def _suggest_hyperparameters(self, trial: optuna.Trial) -> Dict[str, Union[int, float, str]]:
        """
        Suggests a set of hyperparameters for the Optuna trial.

        Parameters
        ----------
        trial : optuna.Trial
            The Optuna trial instance used for hyperparameter optimization.

        Returns
        -------
        Dict[str, Union[int, float, str]]
            A dictionary of suggested hyperparameters.
            Suggested keys:
                - 'n_layers': Number of layers in the network.
                - 'growth_rate': Number of neurons added per layer.
                - 'activation': Activation function (e.g., 'relu', 'tanh', etc.).
                - 'use_batch_normalization': Whether to use batch normalization.
                - 'dropout_rate': Dropout rate for regularization.
                - 'optimizer': Optimizer to use during training (e.g., 'adam', 'rmsprop').
                - 'learning_rate': Learning rate for the optimizer.
                - 'batch_size': Batch size for training.
        """
        return {
            'n_layers': trial.suggest_int('n_layers', 1, 5, step=1),
            'growth_rate': trial.suggest_int('growth_rate', 16, 128, step=16),
            'activation': trial.suggest_categorical('activation', ['relu', 'tanh', 'sigmoid', 'leaky_relu', 'gelu']),
            'use_batch_normalization': trial.suggest_categorical('use_batch_normalization', [True, False]),
            'dropout_rate': trial.suggest_float('dropout_rate', 0.1, 0.5, step=0.1),
            'optimizer': trial.suggest_categorical('optimizer', ['adam', 'rmsprop', 'sgd', 'adamw']),
            'learning_rate': trial.suggest_float('learning_rate', 1e-4, 1e-2, log=True),
            'batch_size': trial.suggest_int('batch_size', 32, 128, step=32),
        }

    def _get_activation_function(self, activation_name: str) -> nn.Module:
        """
        Retrieves the corresponding PyTorch activation function based on the provided name.

        Parameters
        ----------
        activation_name : str
            The name of the activation function (e.g., 'relu', 'tanh', etc.).

        Returns
        -------
        nn.Module
            The PyTorch activation function corresponding to the given name.

        Raises
        ------
        ValueError
            If the provided activation function name is not supported.
        """
        activations = {
            'relu': nn.ReLU(),
            'tanh': nn.Tanh(),
            'sigmoid': nn.Sigmoid(),
            'leaky_relu': nn.LeakyReLU(),
            'gelu': nn.GELU(),
        }
        if activation_name in activations:
            return activations[activation_name]
        else:
            raise ValueError(f"Unsupported activation function: {activation_name}")
