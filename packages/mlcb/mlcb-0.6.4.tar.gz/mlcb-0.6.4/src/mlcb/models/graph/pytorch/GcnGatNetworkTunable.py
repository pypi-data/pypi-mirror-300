import torch
import torch.nn as nn
import optuna
from torch_geometric.nn import GCNConv, GATConv, global_mean_pool
from typing import Dict, Union, Any
import numpy as np

from ....base_classes.pytorch.PytorchGeometricTunable import PyTorchGeometricTunable

class GcnGatNetworkTunable(PyTorchGeometricTunable):
    """
    A tunable hybrid neural network class that alternates between GCNConv (Graph Convolutional Network) 
    and GATConv (Graph Attention Network) layers. This architecture is designed for graph-based learning, 
    leveraging both convolutional and attention-based message-passing techniques.

    Hyperparameter tuning is handled via Optuna, enabling flexible experimentation with different 
    model configurations such as the number of layers, hidden channels, dropout, and more.
    
    Attributes
    ----------
    train_data : torch_geometric.data.Dataset
        Training dataset.
    test_data : torch_geometric.data.Dataset
        Testing dataset.
    num_node_features : int
        Number of features for each node in the graph.
    max_epochs : int
        Maximum number of epochs for training.
    """

    def build_model(self, hyperparameters: Dict[str, Any]) -> nn.Module:
        """
        Builds the PyTorch Geometric hybrid model that alternates between GCNConv and GATConv layers.

        The architecture consists of alternating GCNConv and GATConv layers, with an optional activation function,
        followed by dropout layers for regularization. The model concludes with a global mean pooling layer 
        and a final linear layer for classification.

        Parameters
        ----------
        hyperparameters : Dict[str, Any]
            A dictionary of hyperparameters. Expected keys:
            - 'n_layers' : int
                Number of layers (alternating GCNConv and GATConv).
            - 'hidden_channels' : int
                Number of hidden channels in the GCNConv and GATConv layers.
            - 'dropout_rate' : float
                Dropout rate for regularization.
            - 'heads' : int
                Number of attention heads in the GATConv layers.
            - 'activation' : str
                Activation function to use ('relu', 'leaky_relu', 'gelu').

        Returns
        -------
        nn.Module
            A PyTorch neural network model based on a hybrid GCN/GAT architecture.
        """
        n_layers: int = hyperparameters.get('n_layers', 6)
        hidden_channels: int = hyperparameters.get('hidden_channels', 128)
        dropout_rate: float = hyperparameters.get('dropout_rate', 0.3)
        heads: int = hyperparameters.get('heads', 8)
        activation_func: str = hyperparameters.get('activation', 'relu')
        output_dim: int = len(np.unique(self.test_labels))
        input_shape: int = self.num_node_features

        activations = {
            'relu': nn.ReLU(),
            'leaky_relu': nn.LeakyReLU(),
            'gelu': nn.GELU()
        }
        activation = activations[activation_func]

        convs = nn.ModuleList([GCNConv(input_shape, hidden_channels)])
        for i in range(n_layers // 2):
            convs.append(GATConv(hidden_channels, hidden_channels, heads=heads))
            convs.append(GCNConv(hidden_channels * heads, hidden_channels))

        dropout = nn.Dropout(p=dropout_rate)
        lin = nn.Linear(hidden_channels, output_dim)

        class GCN_GAT_Hybrid_Model(nn.Module):
            """
            Inner class representing the hybrid model architecture alternating between GCNConv and GATConv layers.
            
            Attributes
            ----------
            convs : nn.ModuleList
                List of GCNConv and GATConv layers for message passing.
            dropout : nn.Dropout
                Dropout layer for regularization during training.
            lin : nn.Linear
                Output linear layer for final classification.
            activation : nn.Module
                Activation function for the layers.
            """

            def __init__(self, convs: nn.ModuleList, dropout: nn.Dropout, lin: nn.Linear, activation: nn.Module):
                """
                Initializes the GCN_GAT_Hybrid_Model with the provided layers.

                Parameters
                ----------
                convs : nn.ModuleList
                    List of GCNConv and GATConv layers.
                dropout : nn.Dropout
                    Dropout layer for regularization.
                lin : nn.Linear
                    Output linear transformation layer.
                activation : nn.Module
                    Activation function for the layers.
                """
                super(GCN_GAT_Hybrid_Model, self).__init__()
                self.convs = convs
                self.dropout = dropout
                self.lin = lin
                self.activation = activation

            def forward(self, data: Any) -> torch.Tensor:
                """
                Defines the forward pass of the hybrid model.

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

        return GCN_GAT_Hybrid_Model(convs, dropout, lin, activation)

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
            A dictionary of suggested hyperparameters for the model. These include:
            - 'n_layers' : int
                Number of alternating GCNConv and GATConv layers.
            - 'hidden_channels' : int
                Number of hidden channels for the GCNConv and GATConv layers.
            - 'dropout_rate' : float
                Dropout rate for regularization.
            - 'heads' : int
                Number of attention heads in the GATConv layers.
            - 'activation' : str
                Activation function ('relu', 'leaky_relu', 'gelu').
            - 'optimizer' : str
                Optimizer to use during training ('adam', 'rmsprop', or 'sgd').
            - 'learning_rate' : float
                Learning rate for the optimizer.
            - 'batch_size' : int
                Batch size to use during training.
        """
        return {
            'n_layers': trial.suggest_int('n_layers', 4, 8),
            'hidden_channels': trial.suggest_int('hidden_channels', 32, 256),
            'dropout_rate': trial.suggest_float('dropout_rate', 0.0, 0.5),
            'heads': trial.suggest_int('heads', 2, 16),
            'activation': trial.suggest_categorical('activation', ['relu', 'leaky_relu', 'gelu']),
            'optimizer': trial.suggest_categorical('optimizer', ['adam', 'rmsprop', 'sgd']),
            'learning_rate': trial.suggest_float('learning_rate', 1e-5, 1e-2, log=True),
            'batch_size': trial.suggest_int('batch_size', 16, 128),
        }
