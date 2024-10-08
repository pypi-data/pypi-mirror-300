import torch
import torch.nn as nn
import optuna
from torch_geometric.nn import LEConv, global_mean_pool, global_max_pool, global_add_pool
from typing import Dict, Union, Any
import numpy as np

from ....base_classes.pytorch.PytorchGeometricTunable import PyTorchGeometricTunable

class LeNetworkTunable(PyTorchGeometricTunable):
    """
    A tunable neural network class using LEConv (Laplacian Eigenmaps) layers 
    with hyperparameter tuning via Optuna.

    This class builds a graph neural network using LEConv layers and supports automated hyperparameter 
    tuning with Optuna. It also includes options for activation functions, dropout, and various 
    pooling strategies.
    
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
        Builds the PyTorch Geometric model based on LEConv layers and linear transformations.

        The model consists of multiple LEConv layers followed by dropout and a linear layer. 
        Global pooling is applied at the end, with different pooling methods available such as 
        global mean pooling, max pooling, or add pooling.

        Parameters
        ----------
        hyperparameters : Dict[str, Any]
            Dictionary containing model hyperparameters. Expected keys:
            - 'n_layers' : int
                Number of LEConv layers.
            - 'hidden_channels' : int
                Number of hidden channels for each layer.
            - 'dropout_rate' : float
                Dropout rate for regularization.
            - 'activation' : str
                Activation function to use ('relu', 'leaky_relu', 'gelu').
            - 'pooling' : str
                Pooling function to apply ('mean', 'max', 'add').

        Returns
        -------
        nn.Module
            A PyTorch neural network model based on LEConv layers.
        """
        n_layers: int = hyperparameters.get('n_layers', 3)
        hidden_channels: int = hyperparameters.get('hidden_channels', 128)
        dropout_rate: float = hyperparameters.get('dropout_rate', 0.3)
        activation_func: str = hyperparameters.get('activation', 'relu')
        pooling_type: str = hyperparameters.get('pooling', 'mean')
        output_dim: int = len(np.unique(self.test_labels))
        input_shape: int = self.num_node_features

        activations = {
            'relu': nn.ReLU(),
            'leaky_relu': nn.LeakyReLU(),
            'gelu': nn.GELU()
        }
        activation = activations[activation_func]

        pooling_funcs = {
            'mean': global_mean_pool,
            'max': global_max_pool,
            'add': global_add_pool
        }
        pooling = pooling_funcs[pooling_type]

        convs = nn.ModuleList(
            [LEConv(input_shape, hidden_channels)] +
            [LEConv(hidden_channels, hidden_channels) for _ in range(n_layers - 1)]
        )
        dropout = nn.Dropout(p=dropout_rate)
        lin = nn.Linear(hidden_channels, output_dim)

        class LEModel(nn.Module):
            """
            Inner class representing the actual model architecture that uses LEConv layers.

            The model applies a series of LEConv layers followed by activation, dropout, and pooling.
            A final linear transformation layer produces the output predictions.
            """

            def __init__(self, convs: nn.ModuleList, dropout: nn.Dropout, lin: nn.Linear, activation: nn.Module, pooling: Any):
                """
                Initializes the LEModel.

                Parameters
                ----------
                convs : nn.ModuleList
                    List of LEConv layers for message passing in the graph.
                dropout : nn.Dropout
                    Dropout layer for regularization.
                lin : nn.Linear
                    Output linear layer for classification.
                activation : nn.Module
                    Activation function for the LEConv layers.
                pooling : Any
                    Pooling function to use (global_mean_pool, global_max_pool, global_add_pool).
                """
                super(LEModel, self).__init__()
                self.convs = convs
                self.dropout = dropout
                self.lin = lin
                self.activation = activation
                self.pooling = pooling

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
                x = self.pooling(x, batch)
                return self.lin(x)

        return LEModel(convs, dropout, lin, activation, pooling)

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
                Number of LEConv layers.
            - 'hidden_channels' : int
                Number of hidden channels for each layer.
            - 'dropout_rate' : float
                Dropout rate for regularization.
            - 'activation' : str
                Activation function to use ('relu', 'leaky_relu', 'gelu').
            - 'pooling' : str
                Pooling function to apply ('mean', 'max', 'add').
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
            'pooling': trial.suggest_categorical('pooling', ['mean', 'max', 'add']),
            'optimizer': trial.suggest_categorical('optimizer', ['adam', 'rmsprop', 'sgd']),
            'learning_rate': trial.suggest_float('learning_rate', 1e-5, 1e-2, log=True),
            'batch_size': trial.suggest_int('batch_size', 16, 128),
        }
