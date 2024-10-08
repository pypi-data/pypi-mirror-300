"""
This package offers a variety of tunable models for tabular data and graph data, built on top of popular frameworks 
like PyTorch, TensorFlow, and Scikit-learn but also allow to define own classifiers. It leverages Optuna for
hyperparameter tuning to provide a framework for automatically finding optimal model configurations.

Packages:

- base_classes: Contains base classes for tunable models and helpers for building models in PyTorch, scikit-learn, 
  and TensorFlow. These base classes provide the foundational framework for the tunable models in this package.
  
- models.tabular: Provides tunable models specifically designed for tabular data classification, including both 
  neural network architectures and traditional machine learning models.

- models.graph: Offers tunable graph neural network (GNN) models, built on top of PyTorch Geometric, for tasks 
  such as node classification and graph representation learning.

"""
