"""
Overview
--------

This package provides a flexible and modular framework for building, tuning, evaluating, and logging machine learning models 
using various libraries such as PyTorch, TensorFlow, and scikit-learn. It integrates Optuna for hyperparameter optimization 
and MLFlow for experiment tracking and model management.

Module and packages:

1. **BaseTunableModel**: 
    The abstract base class that defines the core structure for tunable machine learning models. It provides functionality for:
    - Hyperparameter tuning using Optuna.
    - Model training and evaluation.
    - Experiment logging and model saving with MLFlow.
    - Customizable metric evaluations.
   
2. **helpers**:
    Contains helper modules for metrics calculation, plotting, and logging:
    - **MetricsHelper**: A helper class for calculating various classification performance metrics like accuracy, precision, recall, F1-score, etc.
    - **PlotHelper**: A helper class for generating various evaluation plots such as ROC curves, confusion matrices, precision-recall curves, etc.
    - **MLFlowLogger**: A utility class for logging experiment metrics, parameters, and models using MLFlow. Also supports launching the MLFlow UI for tracking.
   
3. **pytorch**:
    Submodule containing tunable PyTorch models:
    - **PytorchTunable**: A tunable PyTorch model class for training and evaluating standard feedforward neural networks.
    - **PytorchTabularTunable**: A tunable PyTorch model designed for tabular data using the PyTorch Tabular library.
    - **PyTorchGeometricTunable**: A tunable PyTorch Geometric model for graph-based machine learning tasks.
    - **NetworkxGraphDataset**: A custom dataset class for loading and processing graphs in NetworkX format.
    - **EarlyStopping**: A utility class for implementing early stopping during PyTorch model training to avoid overfitting.

4. **sklearn**:
    Submodule containing tunable scikit-learn models:
    - **SklearnTunable**: A tunable scikit-learn model class that supports training and evaluating models built using scikit-learn’s Pipeline interface.
   
5. **tensorflow**:
    Submodule containing tunable TensorFlow models:
    - **TensorflowTunable**: A tunable TensorFlow model class for training, tuning, and evaluating TensorFlow models, including support for hyperparameter tuning and MLFlow logging.

Functionalities:

- **Hyperparameter Tuning**: 
    All tunable model classes in the package support hyperparameter tuning using Optuna. This allows automatic optimization of hyperparameters such as learning rates, batch sizes, optimizers, and model architecture parameters.
   
- **Experiment Tracking and Logging**: 
    MLFlow is integrated for tracking and logging experiments, including saving trained models, hyperparameters, and evaluation metrics.
   
- **Cross-library Support**: 
    The package supports models from multiple machine learning libraries (PyTorch, TensorFlow, and scikit-learn) and provides a consistent interface for model tuning, training, evaluation, and logging.

- **Custom Metric Support**: 
    In addition to standard metrics, there can be defined custom evaluation metrics and integrate them into the training and evaluation pipelines.
"""
