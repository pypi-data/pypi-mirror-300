"""
This module provides functionality for building and training tunable PyTorch and PyTorch Geometric models, handling graph datasets, and managing early stopping during model training. The module integrates with Optuna for hyperparameter tuning and MLFlow for experiment tracking.

Package overview
----------------

EarlyStopping
    A utility class for implementing early stopping during model training. This class monitors validation loss and stops training when the loss stops improving.

    Key functionality includes:
    - Tracking model improvement over epochs.
    - Stopping training once the model reaches a plateau.
    - Restoring the best model weights from the epoch with the lowest validation loss.

NetworkxGraphDataset
    A custom dataset class for loading graphs stored in NetworkX format, splitting the dataset into training and testing sets, and converting the graphs into PyTorch Geometric format.

    Key functionality includes:
    - Loading and converting NetworkX graphs to PyTorch Geometric format.
    - Splitting the dataset into training and testing splits for graph-based models.
    - Handling graph-based data with ease for PyTorch Geometric models.

PytorchGeometricTunable
    A tunable PyTorch Geometric model class that integrates graph neural networks (GNNs) with hyperparameter tuning and experiment logging.

    Key functionality includes:
    - Training graph-based models with tunable hyperparameters using PyTorch Geometric.
    - Support for various graph models such as GCN, GAT, etc.
    - Integration with Optuna for hyperparameter optimization and MLFlow for model tracking.

PytorchTabularTunable
    A tunable PyTorch model class designed for tabular data, allowing hyperparameter tuning, training, and evaluation.

    Key functionality includes:
    - Training tabular models with tunable hyperparameters.
    - Support for various tabular model configurations using the PyTorch Tabular library.
    - Hyperparameter tuning with Optuna and experiment logging with MLFlow.

PytorchTunable
    A tunable PyTorch model class that supports training, evaluating, and tuning general neural network models.

    Key functionality includes:
    - Training custom neural networks with tunable hyperparameters (e.g., optimizer type, learning rate).
    - Early stopping and evaluation of models.
    - Integration with Optuna for hyperparameter optimization and MLFlow for experiment tracking.
"""
