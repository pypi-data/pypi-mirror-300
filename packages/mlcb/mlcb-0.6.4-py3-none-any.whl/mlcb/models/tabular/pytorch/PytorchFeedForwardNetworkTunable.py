import torch.nn as nn
import numpy as np
import optuna
from typing import Dict, Union, Any

from ....base_classes.pytorch.PytorchTunable import PytorchTunable

class PytorchFeedForwardNetworkTunable(PytorchTunable):
    """
    A tunable PyTorch feedforward neural network model class with hyperparameter tuning via Optuna.

    The model architecture includes customizable layers, units, activation functions, batch normalization, and dropout.

    Methods
    -------
    build_model(input_shape: tuple, hyperparameters: Dict[str, Any]) -> nn.Module
        Builds the feedforward neural network model based on the provided input shape and hyperparameters.
    
    _suggest_hyperparameters(trial: optuna.Trial) -> Dict[str, Union[int, float, str]]
        Suggests a set of hyperparameters for tuning using Optuna.
    
    _get_activation_function(activation_name: str) -> nn.Module
        Retrieves the corresponding PyTorch activation function based on the provided name.
    """

    def build_model(self, input_shape: tuple, hyperparameters: Dict[str, Any]) -> nn.Module:
        """
        Builds the feedforward neural network model based on the provided input shape and hyperparameters.

        Parameters
        ----------
        input_shape : tuple
            The shape of the input data, typically (num_features,).
        hyperparameters : Dict[str, Any]
            A dictionary of model hyperparameters.
            Expected keys:
                - 'n_layers': The number of layers in the feedforward network.
                - 'units': The number of units (neurons) per layer.
                - 'activation': The activation function to use (e.g., 'relu', 'tanh', etc.).
                - 'use_batch_normalization': Whether to apply batch normalization after each layer.
                - 'dropout_rate': The dropout rate for regularization.

        Returns
        -------
        nn.Module
            A PyTorch feedforward neural network model.
        """
        n_layers: int = hyperparameters.get('n_layers', 3)
        units: int = hyperparameters.get('units', 128)
        activation: nn.Module = self._get_activation_function(hyperparameters.get('activation', 'relu'))
        use_batch_normalization: bool = hyperparameters.get('use_batch_normalization', True)
        dropout_rate: float = hyperparameters.get('dropout_rate', 0.3)

        layers = []
        input_units = input_shape[0]
        output_shape = len(np.unique(self.test_labels))

        for _ in range(n_layers):
            layers.append(nn.Linear(input_units, units))
            if use_batch_normalization:
                layers.append(nn.BatchNorm1d(units))
            layers.append(activation)
            if dropout_rate > 0:
                layers.append(nn.Dropout(dropout_rate))
            input_units = units

        layers.append(nn.Linear(units, output_shape))

        return nn.Sequential(*layers)

    def _suggest_hyperparameters(self, trial: optuna.Trial) -> Dict[str, Union[int, float, str]]:
        """
        Suggests a set of hyperparameters for tuning using Optuna.

        Parameters
        ----------
        trial : optuna.Trial
            The Optuna trial object for hyperparameter optimization.

        Returns
        -------
        Dict[str, Union[int, float, str]]
            A dictionary containing suggested hyperparameters, including:
            - 'n_layers': The number of hidden layers.
            - 'units': The number of units (neurons) per hidden layer.
            - 'activation': The activation function (e.g., 'relu', 'tanh').
            - 'use_batch_normalization': Whether to apply batch normalization.
            - 'dropout_rate': The dropout rate for regularization.
            - 'optimizer': The optimizer to use (e.g., 'adam', 'rmsprop').
            - 'learning_rate': The learning rate for the optimizer.
            - 'batch_size': The batch size for training.
        """
        return {
            'n_layers': trial.suggest_int('n_layers', 1, 5, step=1),
            'units': trial.suggest_int('units', 64, 1024, step=64),
            'activation': trial.suggest_categorical('activation', ['relu', 'tanh', 'sigmoid', 'leaky_relu', 'gelu']),
            'use_batch_normalization': trial.suggest_categorical('use_batch_normalization', [True, False]),
            'dropout_rate': trial.suggest_float('dropout_rate', 0.1, 0.5, step=0.1),
            'optimizer': trial.suggest_categorical('optimizer', ['adam', 'rmsprop', 'sgd', 'adamw']),
            'learning_rate': trial.suggest_float('learning_rate', 1e-4, 1e-2, log=True),
            'batch_size': trial.suggest_int('batch_size', 32, 128, step=32),
        }

    def _get_activation_function(self, activation_name: str) -> nn.Module:
        """
        Retrieves the corresponding PyTorch activation function.

        Parameters
        ----------
        activation_name : str
            The name of the activation function (e.g., 'relu', 'tanh', etc.).

        Returns
        -------
        nn.Module
            The corresponding activation function module.

        Raises
        ------
        ValueError
            If an unsupported activation function name is provided.
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
