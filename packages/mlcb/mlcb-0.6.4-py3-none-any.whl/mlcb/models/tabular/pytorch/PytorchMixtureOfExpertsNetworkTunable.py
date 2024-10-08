import torch
import torch.nn as nn
import numpy as np
import optuna
from typing import Dict, Union, Any

from ....base_classes.pytorch.PytorchTunable import PytorchTunable


class PytorchMoETunable(PytorchTunable):
    """
    A tunable PyTorch model class implementing a Mixture of Experts (MoE) architecture with 
    hyperparameter tuning via Optuna. The model uses a gating network to combine the outputs of 
    multiple expert networks and adaptively select the best combination for the task.

    Methods
    -------
    build_model(input_shape: tuple, hyperparameters: Dict[str, Any]) -> nn.Module
        Builds the Mixture of Experts (MoE) model based on the provided input shape and hyperparameters.

    _suggest_hyperparameters(trial: optuna.Trial) -> Dict[str, Union[int, float, str]]
        Suggests a set of hyperparameters for the Optuna trial.

    _get_activation_function(activation_name: str) -> nn.Module
        Retrieves the corresponding PyTorch activation function based on the given name.
    """

    def build_model(self, input_shape: tuple, hyperparameters: Dict[str, Any]) -> nn.Module:
        """
        Builds the Mixture of Experts (MoE) model based on the provided input shape and hyperparameters.

        Parameters
        ----------
        input_shape : tuple
            Shape of the input data.
        hyperparameters : Dict[str, Any]
            Dictionary containing model hyperparameters.
            Expected keys: 
                - 'n_experts' (int): Number of expert networks.
                - 'units' (int): Number of units in each expert.
                - 'activation' (str): Activation function to use in each expert.
                - 'dropout_rate' (float): Dropout rate for regularization.

        Returns
        -------
        nn.Module
            A PyTorch Mixture of Experts (MoE) model.
        """
        n_experts: int = hyperparameters.get('n_experts', 3)
        units: int = hyperparameters.get('units', 128)
        activation: nn.Module = self._get_activation_function(
            hyperparameters.get('activation', 'relu'))
        dropout_rate: float = hyperparameters.get('dropout_rate', 0.3)
        input_units: int = input_shape[0]
        output_shape: int = len(np.unique(self.test_labels))

        gating_network = nn.Sequential(
            nn.Linear(input_units, n_experts),
            nn.Softmax(dim=1)
        )

        experts = []
        for _ in range(n_experts):
            expert_layers = [
                nn.Linear(input_units, units),
                activation
            ]
            if dropout_rate > 0:
                expert_layers.append(nn.Dropout(dropout_rate))
            experts.append(nn.Sequential(*expert_layers))

        experts_module_list = nn.ModuleList(experts)

        output_layer = nn.Linear(units, output_shape)

        class MoEModel(nn.Module):
            """
            Inner class representing the Mixture of Experts (MoE) model.
            """

            def __init__(self, gating_network: nn.Sequential, experts: nn.ModuleList, output_layer: nn.Linear):
                """
                Initializes the MoEModel.

                Parameters
                ----------
                gating_network : nn.Sequential
                    Gating network to assign weights to each expert.
                experts : nn.ModuleList
                    List of expert networks.
                output_layer : nn.Linear
                    Output layer for classification.
                """
                super(MoEModel, self).__init__()
                self.gating_network = gating_network
                self.experts = experts
                self.output_layer = output_layer

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
                    The output of the model after the expert combination and classification.
                """
                gate = self.gating_network(x)
                experts_out = torch.stack([expert(x)
                                          for expert in self.experts], dim=1)
                output = torch.einsum('bi,bij->bj', gate, experts_out)
                return self.output_layer(output)

        return MoEModel(gating_network, experts_module_list, output_layer)

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
            A dictionary of suggested hyperparameters for tuning, including:
            - 'n_experts': Number of expert networks.
            - 'units': Number of units in each expert.
            - 'activation': Activation function (e.g., 'relu', 'tanh', etc.).
            - 'dropout_rate': Dropout rate for regularization.
            - 'optimizer': Optimizer to use for training (e.g., 'adam', 'rmsprop').
            - 'learning_rate': Learning rate for the optimizer.
            - 'batch_size': Batch size for training.
        """
        return {
            'n_experts': trial.suggest_int('n_experts', 2, 10, step=1),
            'units': trial.suggest_int('units', 64, 512, step=64),
            'activation': trial.suggest_categorical('activation', ['relu', 'tanh', 'sigmoid', 'leaky_relu', 'gelu']),
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
            Name of the activation function (e.g., 'relu', 'tanh', 'sigmoid').

        Returns
        -------
        nn.Module
            The corresponding activation function.

        Raises
        ------
        ValueError
            If the activation function is not supported.
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
            raise ValueError(
                f"Unsupported activation function: {activation_name}")
