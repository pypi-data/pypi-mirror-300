import torch
import torch.nn as nn
import optuna
from torch_geometric.nn import GCNConv, SAGEConv, global_mean_pool, global_max_pool, global_add_pool
from typing import Dict, Union, Any
import numpy as np

from ....base_classes.pytorch.PytorchGeometricTunable import PyTorchGeometricTunable

class GcnSageNetworkTunable(PyTorchGeometricTunable):
    """
    A tunable hybrid neural network class that alternates between GCNConv (Graph Convolutional Network)
    and SAGEConv (GraphSAGE) layers with hyperparameter tuning via Optuna.
    
    This architecture combines both GCN and SAGE layers for message passing in the graph,
    providing flexibility in the choice of layer types and pooling mechanisms, making it
    suitable for node classification tasks on graph-structured data.
    
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
        Builds the PyTorch Geometric hybrid model alternating between GCNConv and SAGEConv layers.
        
        The model applies GCNConv and SAGEConv layers in alternating order, followed by a global
        pooling operation (mean, max, or add) to combine node embeddings. The final layer is a linear
        transformation for classification.

        Parameters
        ----------
        hyperparameters : Dict[str, Any]
            Dictionary containing the model hyperparameters. Expected keys:
            - 'n_layers' : int
                Number of GCN/SAGE layers (the model alternates between GCNConv and SAGEConv).
            - 'hidden_channels' : int
                Number of hidden channels for each layer.
            - 'dropout_rate' : float
                Dropout rate for regularization.
            - 'sage_aggregation' : str
                Aggregation method used by SAGEConv ('mean', 'max', 'lstm').
            - 'pooling' : str
                Pooling operation after convolution layers ('mean', 'max', 'add').

        Returns
        -------
        nn.Module
            A PyTorch neural network model based on a hybrid GCN/SAGE architecture.
        """
        n_layers: int = hyperparameters.get('n_layers', 6)
        hidden_channels: int = hyperparameters.get('hidden_channels', 128)
        dropout_rate: float = hyperparameters.get('dropout_rate', 0.3)
        output_dim: int = len(np.unique(self.test_labels))
        input_shape: int = self.num_node_features
        sage_aggregation: str = hyperparameters.get('sage_aggregation', 'mean')
        pooling_type: str = hyperparameters.get('pooling', 'mean')

        pooling_funcs = {
            'mean': global_mean_pool,
            'max': global_max_pool,
            'add': global_add_pool
        }
        pooling = pooling_funcs[pooling_type]

        convs = nn.ModuleList([GCNConv(input_shape, hidden_channels)])
        for i in range(n_layers // 2):
            convs.append(SAGEConv(hidden_channels, hidden_channels, aggr=sage_aggregation))
            convs.append(GCNConv(hidden_channels, hidden_channels))

        dropout = nn.Dropout(p=dropout_rate)
        lin = nn.Linear(hidden_channels, output_dim)

        class GCN_SAGE_Hybrid_Model(nn.Module):
            """
            Inner class representing the actual hybrid model architecture that uses both GCNConv and SAGEConv layers
            for message passing.
            """
            
            def __init__(self, convs: nn.ModuleList, dropout: nn.Dropout, lin: nn.Linear, pooling: Any):
                """
                Initializes the GCN_SAGE_Hybrid_Model with the specified layers, dropout, and pooling function.

                Parameters
                ----------
                convs : nn.ModuleList
                    List of GCNConv and SAGEConv layers for message passing.
                dropout : nn.Dropout
                    Dropout layer for regularization between layers.
                lin : nn.Linear
                    Final linear layer for classification.
                pooling : Any
                    Pooling function (global_mean_pool, global_max_pool, or global_add_pool).
                """
                super(GCN_SAGE_Hybrid_Model, self).__init__()
                self.convs = convs
                self.dropout = dropout
                self.lin = lin
                self.pooling = pooling

            def forward(self, data: Any) -> torch.Tensor:
                """
                Forward pass of the GCN_SAGE_Hybrid_Model.

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
                    x = x.relu()
                    x = self.dropout(x)
                x = self.pooling(x, batch)
                return self.lin(x)

        return GCN_SAGE_Hybrid_Model(convs, dropout, lin, pooling)

    def _suggest_hyperparameters(self, trial: optuna.Trial) -> Dict[str, Union[int, float, str]]:
        """
        Suggests a set of hyperparameters for the Optuna trial.

        This method suggests hyperparameters for the model, including the number of layers, hidden dimensions,
        dropout rate, SAGEConv aggregation method, pooling function, and optimization parameters such as
        learning rate and batch size.

        Parameters
        ----------
        trial : optuna.Trial
            The Optuna trial instance for hyperparameter optimization.

        Returns
        -------
        Dict[str, Union[int, float, str]]
            A dictionary of suggested hyperparameters for the model, including:
            - 'n_layers' : int
                Number of GCNConv and SAGEConv layers.
            - 'hidden_channels' : int
                Number of hidden channels for each layer.
            - 'dropout_rate' : float
                Dropout rate for regularization.
            - 'sage_aggregation' : str
                Aggregation function for SAGEConv ('mean', 'max', 'lstm').
            - 'pooling' : str
                Pooling operation ('mean', 'max', 'add').
            - 'optimizer' : str
                Optimizer for training ('adam', 'rmsprop', 'sgd').
            - 'learning_rate' : float
                Learning rate for the optimizer.
            - 'batch_size' : int
                Batch size for training.
        """
        return {
            'n_layers': trial.suggest_int('n_layers', 4, 8),
            'hidden_channels': trial.suggest_int('hidden_channels', 32, 256),
            'dropout_rate': trial.suggest_float('dropout_rate', 0.0, 0.5),
            'sage_aggregation': trial.suggest_categorical('sage_aggregation', ['mean', 'max', 'lstm']),
            'pooling': trial.suggest_categorical('pooling', ['mean', 'max', 'add']),
            'optimizer': trial.suggest_categorical('optimizer', ['adam', 'rmsprop', 'sgd']),
            'learning_rate': trial.suggest_float('learning_rate', 1e-5, 1e-2, log=True),
            'batch_size': trial.suggest_int('batch_size', 16, 128),
        }
