import torch
import torch.nn as nn
import numpy as np
import optuna
from typing import Dict, Union, Any

from ....base_classes.pytorch.PytorchTunable import PytorchTunable


class PytorchWideAndDeepNetworkTunable(PytorchTunable):
    """
    A tunable PyTorch model class implementing a Wide and Deep architecture.
    The model combines a wide (linear) component with a deep (multi-layered) component,
    and uses Optuna for hyperparameter tuning.

    Methods
    -------
    build_model(input_shape: tuple, hyperparameters: Dict[str, Any]) -> nn.Module
        Builds the wide and deep neural network based on the provided input shape and hyperparameters.

    _suggest_hyperparameters(trial: optuna.Trial) -> Dict[str, Union[int, float, str]]
        Suggests a set of hyperparameters for the Optuna trial.
    """

    def build_model(self, input_shape: tuple, hyperparameters: Dict[str, Any]) -> nn.Module:
        """
        Builds the wide and deep neural network based on the provided input shape and hyperparameters.

        Parameters
        ----------
        input_shape : tuple
            Shape of the input data (typically (num_features,)).
        hyperparameters : Dict[str, Any]
            Dictionary containing model hyperparameters. Expected keys:
            - 'wide_units': Number of units in the wide part of the network.
            - 'deep_units': Number of units in each hidden layer of the deep part.
            - 'deep_n_layers': Number of hidden layers in the deep part.
            - 'dropout_rate': Dropout rate for the deep part.

        Returns
        -------
        nn.Module
            A PyTorch wide and deep neural network model.
        """
        wide_units: int = hyperparameters.get('wide_units', 64)
        wide = nn.Linear(input_shape[0], wide_units)

        deep_units: int = hyperparameters.get('deep_units', 128)
        deep_n_layers: int = hyperparameters.get('deep_n_layers', 3)
        layers = []
        input_units = input_shape[0]

        for _ in range(deep_n_layers):
            layers.append(nn.Linear(input_units, deep_units))
            layers.append(nn.ReLU())
            layers.append(nn.Dropout(hyperparameters.get('dropout_rate', 0.3)))
            input_units = deep_units

        deep = nn.Sequential(*layers)

        combined_units = wide_units + deep_units
        combined = nn.Linear(combined_units, len(np.unique(self.test_labels)))

        class WideAndDeepModel(nn.Module):
            """
            Inner class representing the Wide and Deep model architecture.
            The model combines both wide (linear) and deep (multi-layered) components.
            """

            def __init__(self):
                """
                Initializes the Wide and Deep model.
                """
                super(WideAndDeepModel, self).__init__()
                self.wide = wide
                self.deep = deep
                self.combined = combined

            def forward(self, x: torch.Tensor) -> torch.Tensor:
                """
                Forward pass of the model.

                Parameters
                ----------
                x : torch.Tensor
                    Input data.

                Returns
                -------
                torch.Tensor
                    The output predictions from the combined wide and deep model.
                """
                wide_output = self.wide(x)
                deep_output = self.deep(x)
                combined_output = torch.cat([wide_output, deep_output], dim=1)
                return self.combined(combined_output)

        return WideAndDeepModel()

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
            A dictionary of suggested hyperparameters, including:
            - 'wide_units': Number of units in the wide part.
            - 'deep_units': Number of units in the deep part.
            - 'deep_n_layers': Number of hidden layers in the deep part.
            - 'dropout_rate': Dropout rate for regularization.
            - 'optimizer': Optimizer for training (e.g., 'adam', 'rmsprop').
            - 'learning_rate': Learning rate for the optimizer.
            - 'batch_size': Batch size for training.
        """
        return {
            'wide_units': trial.suggest_int('wide_units', 32, 128, step=32),
            'deep_units': trial.suggest_int('deep_units', 64, 512, step=64),
            'deep_n_layers': trial.suggest_int('deep_n_layers', 1, 5, step=1),
            'dropout_rate': trial.suggest_float('dropout_rate', 0.1, 0.5, step=0.1),
            'optimizer': trial.suggest_categorical('optimizer', ['adam', 'rmsprop', 'sgd', 'adamw']),
            'learning_rate': trial.suggest_float('learning_rate', 1e-4, 1e-2, log=True),
            'batch_size': trial.suggest_int('batch_size', 32, 128, step=32),
        }
