import torch
import torch.nn as nn
import optuna
from torch_geometric.nn import SGConv, global_mean_pool
from typing import Dict, Union, Any
import numpy as np

from ....base_classes.pytorch.PytorchGeometricTunable import PyTorchGeometricTunable

class SgNetworkTunable(PyTorchGeometricTunable):
    """
    A tunable neural network class using SGConv (Simplifying Graph Convolutional Networks) layers 
    with hyperparameter tuning via Optuna.

    This class builds a graph neural network model with SGConv layers for graph-based learning tasks, 
    supporting hyperparameter optimization through Optuna. Key tunable parameters include the number 
    of hidden channels, dropout rate, the number of propagation steps (K), and activation functions.
    
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
        Builds the PyTorch Geometric model based on SGConv layers and linear transformations.

        The model consists of two SGConv layers, each followed by an activation function and dropout. 
        A global mean pooling layer is applied after the SGConv layers to aggregate node embeddings, 
        followed by a linear layer for final classification.

        Parameters
        ----------
        hyperparameters : Dict[str, Any]
            Dictionary containing model hyperparameters. Expected keys:
            - 'hidden_channels' : int
                Number of hidden channels in SGConv layers.
            - 'dropout_rate' : float
                Dropout rate for regularization.
            - 'K' : int
                Number of propagation steps in SGConv.
            - 'activation' : str
                Activation function to use ('relu', 'leaky_relu', 'gelu').

        Returns
        -------
        nn.Module
            A PyTorch neural network model based on SGConv layers.
        """
        hidden_channels: int = hyperparameters.get('hidden_channels', 128)
        dropout_rate: float = hyperparameters.get('dropout_rate', 0.3)
        K: int = hyperparameters.get('K', 2)
        activation_func: str = hyperparameters.get('activation', 'relu')
        output_dim: int = len(np.unique(self.test_labels))
        input_shape: int = self.num_node_features

        activations = {
            'relu': nn.ReLU(),
            'leaky_relu': nn.LeakyReLU(),
            'gelu': nn.GELU()
        }
        activation = activations[activation_func]

        conv1 = SGConv(input_shape, hidden_channels, K=K)
        conv2 = SGConv(hidden_channels, hidden_channels, K=K)
        dropout = nn.Dropout(p=dropout_rate)
        lin = nn.Linear(hidden_channels, output_dim)

        class SGModel(nn.Module):
            """
            Inner class representing the actual model architecture that uses SGConv layers.

            This model applies two SGConv layers, each followed by activation and dropout, and 
            then aggregates node embeddings using global mean pooling. The final output is 
            produced through a linear transformation.
            """

            def __init__(self, conv1: SGConv, conv2: SGConv, dropout: nn.Dropout, lin: nn.Linear, activation: nn.Module):
                """
                Initializes the SGModel.

                Parameters
                ----------
                conv1 : SGConv
                    First SGConv layer.
                conv2 : SGConv
                    Second SGConv layer.
                dropout : nn.Dropout
                    Dropout layer for regularization.
                lin : nn.Linear
                    Output linear transformation layer.
                activation : nn.Module
                    Activation function for the layers.
                """
                super(SGModel, self).__init__()
                self.conv1 = conv1
                self.conv2 = conv2
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
                x = self.conv1(x, edge_index)
                x = self.activation(x)
                x = self.dropout(x)
                x = self.conv2(x, edge_index)
                x = self.activation(x)
                x = self.dropout(x)
                x = global_mean_pool(x, batch)
                return self.lin(x)

        return SGModel(conv1, conv2, dropout, lin, activation)

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
            - 'hidden_channels' : int
                Number of hidden channels in SGConv layers.
            - 'dropout_rate' : float
                Dropout rate for regularization.
            - 'K' : int
                Number of propagation steps in SGConv.
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
            'hidden_channels': trial.suggest_int('hidden_channels', 16, 256),
            'dropout_rate': trial.suggest_float('dropout_rate', 0.0, 0.5),
            'K': trial.suggest_int('K', 1, 5),
            'activation': trial.suggest_categorical('activation', ['relu', 'leaky_relu', 'gelu']),
            'optimizer': trial.suggest_categorical('optimizer', ['adam', 'rmsprop', 'sgd']),
            'learning_rate': trial.suggest_float('learning_rate', 1e-5, 1e-2, log=True),
            'batch_size': trial.suggest_int('batch_size', 16, 128),
        }
