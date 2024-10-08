import torch.nn as nn
import numpy as np
import optuna
from typing import Dict, Union, Any

from ....base_classes.pytorch.PytorchTunable import PytorchTunable


class PytorchTangentKernelNetworkTunable(PytorchTunable):
    """
    A tunable PyTorch model class resembling a Tangent Kernel Network, where the first layer has fixed weights.
    This model uses Optuna for hyperparameter tuning.

    Methods
    -------
    build_model(input_shape: tuple, hyperparameters: Dict[str, Any]) -> nn.Module
        Builds the tangent kernel-like network based on the provided input shape and hyperparameters.

    _suggest_hyperparameters(trial: optuna.Trial) -> Dict[str, Union[int, float, str]]
        Suggests a set of hyperparameters for the Optuna trial.
    """

    def build_model(self, input_shape: tuple, hyperparameters: Dict[str, Any]) -> nn.Module:
        """
        Builds the tangent kernel-like network based on the provided input shape and hyperparameters.

        Parameters
        ----------
        input_shape : tuple
            Shape of the input data (usually (num_features,)).
        hyperparameters : Dict[str, Any]
            Dictionary containing model hyperparameters. Expected keys:
            - 'n_layers': The number of layers in the model.
            - 'units': The number of units (neurons) per layer.

        Returns
        -------
        nn.Module
            A PyTorch neural network model with a tangent kernel structure, where the first layer has fixed weights.
        """
        n_layers: int = hyperparameters.get('n_layers', 5)
        units: int = hyperparameters.get('units', 1024)

        layers = []
        input_units = input_shape[0]
        output_shape = len(np.unique(self.test_labels))

        first_layer = nn.Linear(input_units, units, bias=False)
        nn.init.normal_(first_layer.weight, mean=0,
                        std=np.sqrt(2.0 / input_units))
        layers.append(first_layer)

        for param in first_layer.parameters():
            param.requires_grad = False

        for _ in range(n_layers - 1):
            hidden_layer = nn.Linear(units, units)
            nn.init.normal_(hidden_layer.weight, mean=0,
                            std=np.sqrt(2.0 / units))
            layers.append(hidden_layer)
            layers.append(nn.ReLU())

        output_layer = nn.Linear(units, output_shape)
        nn.init.normal_(output_layer.weight, mean=0, std=np.sqrt(2.0 / units))
        layers.append(output_layer)

        layers.append(nn.Softmax(dim=1))

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
            A dictionary of suggested hyperparameters, including:
            - 'n_layers': Number of layers in the network.
            - 'units': Number of units (neurons) per layer.
            - 'optimizer': Optimizer to use (e.g., 'adam', 'rmsprop').
            - 'learning_rate': Learning rate for the optimizer.
            - 'batch_size': Batch size for training.
        """
        return {
            'n_layers': trial.suggest_int('n_layers', 3, 10),
            'units': trial.suggest_int('units', 512, 4096, step=512),
            'optimizer': trial.suggest_categorical('optimizer', ['adam', 'rmsprop', 'sgd', 'adamw']),
            'learning_rate': trial.suggest_float('learning_rate', 1e-4, 1e-2, log=True),
            'batch_size': trial.suggest_int('batch_size', 32, 256, step=32),
        }
