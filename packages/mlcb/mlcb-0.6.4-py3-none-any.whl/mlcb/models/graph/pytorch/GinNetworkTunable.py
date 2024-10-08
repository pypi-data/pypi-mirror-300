import torch
import torch.nn as nn
import optuna
from torch_geometric.nn import GINConv, global_mean_pool
from typing import Dict, Union, Any
import numpy as np

from ....base_classes.pytorch.PytorchGeometricTunable import PyTorchGeometricTunable

class GinNetworkTunable(PyTorchGeometricTunable):
    """
    A tunable neural network class using GINConv (Graph Isomorphism Network) layers 
    with hyperparameter tuning via Optuna.

    This class builds a GINConv-based neural network for node classification tasks on graph-structured data,
    leveraging Optuna for automated hyperparameter tuning.

    Attributes
    ----------
    train_data : torch_geometric.data.Dataset
        The training dataset in PyTorch Geometric format.
    test_data : torch_geometric.data.Dataset
        The testing dataset in PyTorch Geometric format.
    num_node_features : int
        Number of features for each node in the graph.
    max_epochs : int
        Maximum number of epochs for training.
    device : torch.device
        The device (CPU or GPU) used for training the model.
    """

    def build_model(self, hyperparameters: Dict[str, Any]) -> nn.Module:
        """
        Builds the PyTorch Geometric model based on GINConv layers and linear transformations.

        The model consists of multiple GINConv layers stacked together, followed by global mean pooling
        and a final linear layer for classification.

        Parameters
        ----------
        hyperparameters : Dict[str, Any]
            Dictionary containing model hyperparameters. Expected keys:
            - 'n_layers' : int
                Number of GINConv layers.
            - 'hidden_channels' : int
                Number of hidden channels for each layer.
            - 'dropout_rate' : float
                Dropout rate for regularization.
            - 'activation' : str
                Activation function to use ('relu', 'leaky_relu', 'gelu').

        Returns
        -------
        nn.Module
            A PyTorch neural network model based on GINConv layers.
        """
        n_layers: int = hyperparameters.get('n_layers', 3)
        hidden_channels: int = hyperparameters.get('hidden_channels', 128)
        dropout_rate: float = hyperparameters.get('dropout_rate', 0.3)
        output_dim: int = len(np.unique(self.test_labels))
        input_shape: int = self.num_node_features
        activation_func: str = hyperparameters.get('activation', 'relu')

        activations = {
            'relu': nn.ReLU(),
            'leaky_relu': nn.LeakyReLU(),
            'gelu': nn.GELU()
        }
        activation = activations[activation_func]

        convs = nn.ModuleList(
            [GINConv(nn.Linear(input_shape, hidden_channels))] +
            [GINConv(nn.Linear(hidden_channels, hidden_channels)) for _ in range(n_layers - 1)]
        )
        dropout = nn.Dropout(p=dropout_rate)
        lin = nn.Linear(hidden_channels, output_dim)

        class GINModel(nn.Module):
            """
            Inner class representing the actual model architecture that uses GINConv layers.

            The model applies a series of GINConv layers, followed by dropout, global mean pooling,
            and a final linear transformation to produce the output predictions.
            """

            def __init__(self, convs: nn.ModuleList, dropout: nn.Dropout, lin: nn.Linear, activation: nn.Module):
                """
                Initializes the GINModel.

                Parameters
                ----------
                convs : nn.ModuleList
                    List of GINConv layers for message passing in the graph.
                dropout : nn.Dropout
                    Dropout layer for regularization.
                lin : nn.Linear
                    Output linear layer for classification.
                activation : nn.Module
                    Activation function for the GINConv layers.
                """
                super(GINModel, self).__init__()
                self.convs = convs
                self.dropout = dropout
                self.lin = lin
                self.activation = activation

            def forward(self, data: Any) -> torch.Tensor:
                """
                Forward pass of the model.

                Parameters
                ----------
                data : Any
                    Input data containing node features, edge indices, and batch information.

                Returns
                -------
                torch.Tensor
                    The output predictions from the model.
                """
                x, edge_index, batch = data.x, data.edge_index, data.batch
                for conv in self.convs:
                    x = conv(x, edge_index)
                    x = self.activation(x)
                    x = self.dropout(x)
                x = global_mean_pool(x, batch)
                return self.lin(x)

        return GINModel(convs, dropout, lin, activation)

    def _suggest_hyperparameters(self, trial: optuna.Trial) -> Dict[str, Union[int, float, str]]:
        """
        Suggests a set of hyperparameters for the Optuna trial.

        This method defines the range of hyperparameters that Optuna will explore during the tuning process.

        Parameters
        ----------
        trial : optuna.Trial
            The Optuna trial instance for hyperparameter optimization.

        Returns
        -------
        Dict[str, Union[int, float, str]]
            A dictionary of suggested hyperparameters, including:
            - 'n_layers' : int
                Number of GINConv layers.
            - 'hidden_channels' : int
                Number of hidden channels for each layer.
            - 'dropout_rate' : float
                Dropout rate for regularization.
            - 'activation' : str
                Activation function to use ('relu', 'leaky_relu', 'gelu').
            - 'optimizer' : str
                Optimizer for training ('adam', 'rmsprop', 'sgd').
            - 'learning_rate' : float
                Learning rate for the optimizer.
            - 'batch_size' : int
                Batch size for training.
        """
        return {
            'n_layers': trial.suggest_int('n_layers', 2, 5),
            'hidden_channels': trial.suggest_int('hidden_channels', 16, 256),
            'dropout_rate': trial.suggest_float('dropout_rate', 0.0, 0.5),
            'activation': trial.suggest_categorical('activation', ['relu', 'leaky_relu', 'gelu']),
            'optimizer': trial.suggest_categorical('optimizer', ['adam', 'rmsprop', 'sgd']),
            'learning_rate': trial.suggest_float('learning_rate', 1e-5, 1e-2, log=True),
            'batch_size': trial.suggest_int('batch_size', 16, 128),
        }
