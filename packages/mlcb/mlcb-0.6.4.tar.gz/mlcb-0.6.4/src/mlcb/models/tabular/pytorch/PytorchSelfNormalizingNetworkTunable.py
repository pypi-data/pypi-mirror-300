import torch.nn as nn
import numpy as np
import optuna
from typing import Dict, Union, Any

from ....base_classes.pytorch.PytorchTunable import PytorchTunable

class PytorchSelfNormalizingNetworkTunable(PytorchTunable):
    """
    A tunable PyTorch model class implementing a Self-Normalizing Neural Network (SNN) architecture
    with SELU activation functions and AlphaDropout, using Optuna for hyperparameter tuning.

    Methods
    -------
    build_model(input_shape: tuple, hyperparameters: Dict[str, Any]) -> nn.Module
        Builds the self-normalizing neural network model based on the provided input shape and hyperparameters.
    
    _suggest_hyperparameters(trial: optuna.Trial) -> Dict[str, Union[int, float, str]]
        Suggests a set of hyperparameters for the Optuna trial.
    """

    def build_model(self, input_shape: tuple, hyperparameters: Dict[str, Any]) -> nn.Module:
        """
        Builds the self-normalizing neural network model based on the provided input shape and hyperparameters.

        Parameters
        ----------
        input_shape : tuple
            Shape of the input data, typically (num_features,).
        hyperparameters : Dict[str, Any]
            Dictionary containing model hyperparameters. Expected keys:
            - 'n_layers': The number of hidden layers in the model.
            - 'units': The number of units (neurons) in each hidden layer.
            - 'dropout_rate': The dropout rate for AlphaDropout regularization.

        Returns
        -------
        nn.Module
            A PyTorch self-normalizing neural network model.
        """
        n_layers: int = hyperparameters.get('n_layers', 3)
        units: int = hyperparameters.get('units', 128)
        dropout_rate: float = hyperparameters.get('dropout_rate', 0.3)

        layers = []
        input_units = input_shape[0]
        output_shape = len(np.unique(self.test_labels))

        for _ in range(n_layers):
            layer = nn.Linear(input_units, units)
            nn.init.normal_(layer.weight, mean=0, std=np.sqrt(1 / input_units))
            layers.append(layer)
            layers.append(nn.SELU())
            if dropout_rate > 0:
                layers.append(nn.AlphaDropout(dropout_rate))
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
            A dictionary of suggested hyperparameters for tuning. Includes:
            - 'n_layers': Number of hidden layers in the network.
            - 'units': Number of units (neurons) per hidden layer.
            - 'dropout_rate': Dropout rate for AlphaDropout regularization.
            - 'optimizer': The optimizer to use (e.g., 'adam', 'rmsprop').
            - 'learning_rate': The learning rate for the optimizer.
            - 'batch_size': Batch size for training.
        """
        return {
            'n_layers': trial.suggest_int('n_layers', 1, 10, step=1),
            'units': trial.suggest_int('units', 64, 512, step=64),
            'dropout_rate': trial.suggest_float('dropout_rate', 0.1, 0.5, step=0.1),
            'optimizer': trial.suggest_categorical('optimizer', ['adam', 'rmsprop', 'sgd', 'adamw']),
            'learning_rate': trial.suggest_float('learning_rate', 1e-4, 1e-2, log=True),
            'batch_size': trial.suggest_int('batch_size', 32, 128, step=32)
        }
