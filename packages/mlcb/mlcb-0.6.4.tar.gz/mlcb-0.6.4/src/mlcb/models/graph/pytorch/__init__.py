"""
Package overview
----------------

This module contains tunable PyTorch Geometric neural network architectures for graph-based learning tasks, 
with hyperparameter optimization support via Optuna.

Each model implements a different type of graph convolutional layer, allowing users to experiment 
with various architectures and hyperparameters. The networks offer flexibility in terms of activation 
functions, pooling layers, and dropout regularization, while supporting Optuna for hyperparameter tuning.

1. **TransformerNetworkTunable**
   - Uses TransformerConv layers for graph convolutions with attention mechanisms.

2. **TagNetworkTunable**
   - Implements a network based on TAGConv (Topology Adaptive Graph Convolutional Networks) layers.

3. **SgNetworkTunable**
   - Based on SGConv (Simplifying Graph Convolutional Networks) layers, simplifying the graph convolutional process.

4. **SageNetworkTunable**
   - Implements SAGEConv layers, utilizing the GraphSAGE architecture for graph node embeddings.

5. **LeNetworkTunable**
   - Uses LEConv (Laplacian Eigenmaps) layers for learning on graph structures.

6. **GinNetworkTunable**
   - Based on GINConv (Graph Isomorphism Network) layers, enhancing the neural network’s discriminative power.

7. **GcnSageNetworkTunable**
   - A hybrid network alternating between GCNConv and SAGEConv layers, combining Graph Convolutional Networks (GCN) with GraphSAGE.

8. **GcnNetworkTunable**
   - Implements GCNConv layers for standard Graph Convolutional Networks.

9. **GcnGatNetworkTunable**
   - A hybrid network alternating between GCNConv and GATConv layers, combining Graph Convolutional Networks and Graph Attention Networks.

10. **GatNetworkTunable**
    - Based on GATConv (Graph Attention Network) layers, using attention mechanisms to weight neighborhood nodes.

11. **AppnpNetworkTunable**
    - Implements APPNP (Approximate Personalized Propagation of Neural Predictions) layers for efficient message-passing on graphs.

Key Features:
    
All models support hyperparameter tuning via Optuna, allowing users to experiment with various configurations such as:
- Number of layers
- Hidden channels
- Dropout rate
- Attention heads (for attention-based layers)
- Pooling methods (mean, max, add)
- Optimizers (Adam, RMSprop, SGD)
- Learning rate and batch size
"""

from .AppnpNetworkTunable import AppnpNetworkTunable
from .GatNetworkTunable import GatNetworkTunable
from .GcnNetworkTunable import GcnNetworkTunable
from .GcnGatNetworkTunable import GcnGatNetworkTunable
from .GcnSageNetworkTunable import GcnSageNetworkTunable
from .GinNetworkTunable import GinNetworkTunable
from .LeNetworkTunable import LeNetworkTunable
from .SageNetworkTunable import SageNetworkTunable
from .SgNetworkTunable import SgNetworkTunable
from .TransformerNetworkTunable import TransformerNetworkTunable
from .TagNetworkTunable import TagNetworkTunable
