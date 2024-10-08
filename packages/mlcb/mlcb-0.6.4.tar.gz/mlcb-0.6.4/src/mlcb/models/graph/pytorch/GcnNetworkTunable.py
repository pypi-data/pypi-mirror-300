import torch
import torch.nn as nn
import optuna
from torch_geometric.nn import GCNConv, global_mean_pool
from typing import Dict, Union, Any
import numpy as np

from ....base_classes.pytorch.PytorchGeometricTunable import PyTorchGeometricTunable

class GcnNetworkTunable(PyTorchGeometricTunable):
    """
    A tunable neural network class that uses GCNConv (Graph Convolutional Network) layers for 
    graph-based learning, with hyperparameter tuning facilitated by Optuna.
    
    The architecture consists of stacked GCNConv layers followed by a global pooling layer and 
    a final linear layer for classification. Various hyperparameters such as the number of layers, 
    hidden channels, dropout rate, and activation function can be tuned during optimization.

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
        Builds the PyTorch Geometric model based on GCNConv layers for message passing and a 
        final linear transformation for classification.
        
        This model architecture allows for a configurable number of GCNConv layers, 
        hidden dimensions, dropout, and activation functions. The output from the GCNConv layers 
        is globally pooled before being passed to the final linear layer for classification.

        Parameters
        ----------
        hyperparameters : Dict[str, Any]
            A dictionary containing hyperparameters to configure the model. Expected keys:
            - 'n_layers' : int
                Number of GCNConv layers.
            - 'hidden_channels' : int
                Number of hidden channels in each GCNConv layer.
            - 'dropout_rate' : float
                Dropout rate applied between layers for regularization.
            - 'activation' : str
                Activation function to use ('relu', 'leaky_relu', 'gelu').

        Returns
        -------
        nn.Module
            A PyTorch neural network model with GCNConv layers.
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
            [GCNConv(input_shape, hidden_channels)] +
            [GCNConv(hidden_channels, hidden_channels) for _ in range(n_layers - 1)]
        )
        dropout = nn.Dropout(p=dropout_rate)
        lin = nn.Linear(hidden_channels, output_dim)

        class GCNModel(nn.Module):
            """
            Inner class representing the actual model architecture that uses GCNConv layers 
            for graph convolution and a final linear transformation for classification.
            """
            
            def __init__(self, convs: nn.ModuleList, dropout: nn.Dropout, lin: nn.Linear, activation: nn.Module):
                """
                Initializes the GCNModel with the provided layers and activation function.

                Parameters
                ----------
                convs : nn.ModuleList
                    List of GCNConv layers for message passing.
                dropout : nn.Dropout
                    Dropout layer for regularization between layers.
                lin : nn.Linear
                    Final linear layer for classification.
                activation : nn.Module
                    Activation function to apply between layers.
                """
                super(GCNModel, self).__init__()
                self.convs = convs
                self.dropout = dropout
                self.lin = lin
                self.activation = activation

            def forward(self, data: Any) -> torch.Tensor:
                """
                Forward pass of the GCNModel.

                Parameters
                ----------
                data : Any
                    Input data containing node features, edge indices, and batch information 
                    in the format required by PyTorch Geometric.

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

        return GCNModel(convs, dropout, lin, activation)

    def _suggest_hyperparameters(self, trial: optuna.Trial) -> Dict[str, Union[int, float, str]]:
        """
        Suggests a set of hyperparameters for the Optuna trial.

        This method allows Optuna to suggest values for various hyperparameters such as the 
        number of layers, number of hidden channels, dropout rate, learning rate, etc., 
        for the model.

        Parameters
        ----------
        trial : optuna.Trial
            The Optuna trial instance used for hyperparameter optimization.

        Returns
        -------
        Dict[str, Union[int, float, str]]
            A dictionary of suggested hyperparameters for the model, including:
            - 'n_layers' : int
                Number of GCNConv layers.
            - 'hidden_channels' : int
                Number of hidden channels in each layer.
            - 'dropout_rate' : float
                Dropout rate for regularization.
            - 'weight_decay' : float
                Weight decay (L2 regularization).
            - 'activation' : str
                Activation function ('relu', 'leaky_relu', 'gelu').
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
            'weight_decay': trial.suggest_float('weight_decay', 1e-6, 1e-2, log=True),
            'activation': trial.suggest_categorical('activation', ['relu', 'leaky_relu', 'gelu']),
            'optimizer': trial.suggest_categorical('optimizer', ['adam', 'rmsprop', 'sgd']),
            'learning_rate': trial.suggest_float('learning_rate', 1e-5, 1e-2, log=True),
            'batch_size': trial.suggest_int('batch_size', 16, 128),
        }
