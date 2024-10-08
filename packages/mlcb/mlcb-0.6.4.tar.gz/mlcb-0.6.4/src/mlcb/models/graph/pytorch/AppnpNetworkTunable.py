import torch
import torch.nn as nn
import optuna
from torch_geometric.nn import APPNP, global_mean_pool
from typing import Dict, Union, Any
import numpy as np

from ....base_classes.pytorch.PytorchGeometricTunable import PyTorchGeometricTunable


class AppnpNetworkTunable(PyTorchGeometricTunable):
    """
    A tunable neural network class utilizing the APPNP (Approximate Personalized Propagation of Neural Predictions)
    layer for graph-based learning. This class supports hyperparameter tuning via Optuna and inherits from 
    `PyTorchGeometricTunable`.

    The model consists of:
    - Linear layers for node feature transformation.
    - APPNP layer for message passing across nodes in the graph.
    - Global mean pooling for aggregating node embeddings.
    - Dropout layers for regularization.

    Attributes
    ----------
    num_node_features : int
        Number of node features in the graph.
    train_data : torch_geometric.data.Dataset
        Training dataset.
    test_data : torch_geometric.data.Dataset
        Testing dataset.
    """

    def build_model(self, hyperparameters: Dict[str, Any]) -> nn.Module:
        """
        Builds the PyTorch Geometric model using the APPNP layer and linear transformations.

        The model architecture includes:
        - A linear layer for transforming node features to hidden channels.
        - An APPNP layer for propagating node information across the graph.
        - Global mean pooling for aggregating node embeddings across the graph.
        - A final linear layer for classification.

        Parameters
        ----------
        hyperparameters : Dict[str, Any]
            A dictionary containing the model hyperparameters. 
            Expected keys:
            - 'hidden_channels': int
                Number of hidden channels in the first linear layer.
            - 'dropout_rate': float
                Dropout rate for regularization.
            - 'alpha': float
                APPNP alpha hyperparameter (controls the teleport probability in propagation).
            - 'K': int
                Number of propagation steps in the APPNP layer.

        Returns
        -------
        nn.Module
            A PyTorch neural network model based on the APPNP layer.
        """
        hidden_channels: int = hyperparameters.get('hidden_channels', 128)
        dropout_rate: float = hyperparameters.get('dropout_rate', 0.3)
        output_dim: int = len(np.unique(self.test_labels))
        alpha: float = hyperparameters.get('alpha', 0.1)
        K: int = hyperparameters.get('K', 10)
        input_shape: int = self.num_node_features

        lin1 = nn.Linear(input_shape, hidden_channels)
        lin2 = nn.Linear(hidden_channels, output_dim)
        appnp = APPNP(K=K, alpha=alpha)
        dropout = nn.Dropout(p=dropout_rate)

        class APPNPModel(nn.Module):
            """
            Inner class representing the actual neural network architecture that uses APPNP.

            Parameters
            ----------
            lin1 : nn.Linear
                First linear layer for transforming input features to hidden channels.
            lin2 : nn.Linear
                Output linear layer for final classification.
            appnp : APPNP
                The APPNP layer for propagating node information across the graph.
            dropout : nn.Dropout
                Dropout layer for regularization during training.
            """

            def __init__(self, lin1: nn.Linear, lin2: nn.Linear, appnp: APPNP, dropout: nn.Dropout):
                super(APPNPModel, self).__init__()
                self.lin1 = lin1
                self.lin2 = lin2
                self.appnp = appnp
                self.dropout = dropout

            def forward(self, data: Any) -> torch.Tensor:
                """
                Defines the forward pass of the model.

                Parameters
                ----------
                data : Any
                    The input data containing node features (`x`), edge indices (`edge_index`), 
                    and batch information (`batch`).

                Returns
                -------
                torch.Tensor
                    The output predictions from the model.
                """
                x, edge_index, batch = data.x, data.edge_index, data.batch
                x = self.lin1(x).relu()
                x = self.dropout(x)
                x = self.appnp(x, edge_index)
                x = global_mean_pool(x, batch)
                return self.lin2(x)

        return APPNPModel(lin1, lin2, appnp, dropout)

    def _suggest_hyperparameters(self, trial: optuna.Trial) -> Dict[str, Union[int, float, str]]:
        """
        Suggests a set of hyperparameters for tuning the APPNP model using Optuna.

        Parameters
        ----------
        trial : optuna.Trial
            The Optuna trial object for suggesting hyperparameters.

        Returns
        -------
        Dict[str, Union[int, float, str]]
            A dictionary of hyperparameters suggested by Optuna, including:
            - 'hidden_channels': int
                Number of hidden units in the first linear layer.
            - 'dropout_rate': float
                Dropout rate for regularization.
            - 'optimizer': str
                Optimizer to use ('adam', 'rmsprop', or 'sgd').
            - 'learning_rate': float
                Learning rate for the optimizer.
            - 'batch_size': int
                Batch size for training.
            - 'K': int
                Number of propagation steps in the APPNP layer.
            - 'alpha': float
                Teleport probability for propagation in APPNP.
        """
        return {
            'hidden_channels': trial.suggest_int('hidden_channels', 16, 256),
            'dropout_rate': trial.suggest_float('dropout_rate', 0.0, 0.5),
            'optimizer': trial.suggest_categorical('optimizer', ['adam', 'rmsprop', 'sgd']),
            'learning_rate': trial.suggest_float('learning_rate', 1e-5, 1e-2, log=True),
            'batch_size': trial.suggest_int('batch_size', 16, 128),
            'K': trial.suggest_int('K', 5, 30),
            'alpha': trial.suggest_float('alpha', 0.05, 0.3),
        }
