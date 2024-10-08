import torch
import torch.nn as nn
import optuna
from torch_geometric.nn import GATConv, global_mean_pool
from typing import Dict, Union, Any
import numpy as np

from ....base_classes.pytorch.PytorchGeometricTunable import PyTorchGeometricTunable

class GatNetworkTunable(PyTorchGeometricTunable):
    """
    A tunable neural network class utilizing the GAT (Graph Attention Network) layer with 
    hyperparameter tuning via Optuna. This class is designed for graph-based learning, leveraging 
    attention mechanisms across graph nodes using the GATConv layer in PyTorch Geometric.
    
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
        Builds the PyTorch Geometric model based on GATConv layers and linear transformations.
        
        The model consists of:
        - Multiple GATConv layers for node-level attention-based message passing.
        - Dropout for regularization between layers.
        - Global mean pooling for aggregating node embeddings across the graph.
        - A final linear layer for output classification.

        Parameters
        ----------
        hyperparameters : Dict[str, Any]
            Dictionary containing model hyperparameters.
            Expected keys:
            - 'n_layers' : int
                Number of GATConv layers.
            - 'hidden_channels' : int
                Number of hidden channels in the GATConv layers.
            - 'dropout_rate' : float
                Dropout rate for regularization.
            - 'heads' : int
                Number of attention heads in each GATConv layer.

        Returns
        -------
        nn.Module
            A PyTorch neural network model based on GATConv layers.
        """
        n_layers: int = hyperparameters.get('n_layers', 3)
        hidden_channels: int = hyperparameters.get('hidden_channels', 128)
        dropout_rate: float = hyperparameters.get('dropout_rate', 0.3)
        heads: int = hyperparameters.get('heads', 8)
        output_dim: int = len(np.unique(self.test_labels))
        input_shape: int = self.num_node_features
        
        convs = nn.ModuleList(
            [GATConv(input_shape, hidden_channels, heads=heads)] +
            [GATConv(hidden_channels * heads, hidden_channels, heads=heads) for _ in range(n_layers - 1)]
        )
        
        dropout = nn.Dropout(p=dropout_rate)
        lin = nn.Linear(hidden_channels * heads, output_dim)

        class GATModel(nn.Module):
            """
            Inner class representing the actual model architecture that uses GATConv layers.
            
            Attributes
            ----------
            convs : nn.ModuleList
                List of GATConv layers for message passing.
            dropout : nn.Dropout
                Dropout layer for regularization during training.
            lin : nn.Linear
                Output linear layer for final classification.
            """

            def __init__(self, convs: nn.ModuleList, dropout: nn.Dropout, lin: nn.Linear):
                """
                Initializes the GATModel with the given layers.

                Parameters
                ----------
                convs : nn.ModuleList
                    List of GATConv layers.
                dropout : nn.Dropout
                    Dropout layer for regularization.
                lin : nn.Linear
                    Output linear transformation layer.
                """
                super(GATModel, self).__init__()
                self.convs = convs
                self.dropout = dropout
                self.lin = lin

            def forward(self, data: Any) -> torch.Tensor:
                """
                Defines the forward pass of the model.

                Parameters
                ----------
                data : Any
                    Input data containing node features (`x`), edge indices (`edge_index`), and batch information (`batch`).

                Returns
                -------
                torch.Tensor
                    The output predictions from the model.
                """
                x, edge_index, batch = data.x, data.edge_index, data.batch
                
                for conv in self.convs:
                    x = conv(x, edge_index)
                    x = x.relu()
                    x = self.dropout(x)
                
                x = global_mean_pool(x, batch)
                
                return self.lin(x)

        return GATModel(convs, dropout, lin)

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
                Number of GATConv layers in the model.
            - 'hidden_channels' : int
                Number of hidden channels in the GATConv layers.
            - 'dropout_rate' : float
                Dropout rate for regularization.
            - 'heads' : int
                Number of attention heads in each GATConv layer.
            - 'optimizer' : str
                Optimizer to use during training (choices are 'adam', 'rmsprop', or 'sgd').
            - 'learning_rate' : float
                Learning rate for the optimizer.
            - 'batch_size' : int
                Batch size to use during training.
        """
        return {
            'n_layers': trial.suggest_int('n_layers', 2, 5),
            'hidden_channels': trial.suggest_int('hidden_channels', 16, 256),
            'dropout_rate': trial.suggest_float('dropout_rate', 0.0, 0.5),
            'heads': trial.suggest_int('heads', 1, 16),
            'optimizer': trial.suggest_categorical('optimizer', ['adam', 'rmsprop', 'sgd']),
            'learning_rate': trial.suggest_float('learning_rate', 1e-5, 1e-2, log=True),
            'batch_size': trial.suggest_int('batch_size', 16, 128),
        }
