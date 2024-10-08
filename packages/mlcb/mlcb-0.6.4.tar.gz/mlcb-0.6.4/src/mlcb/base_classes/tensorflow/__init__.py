"""
This module provides functionality for building, training, tuning, and saving tunable TensorFlow models. 
It integrates Optuna for hyperparameter optimization and MLFlow for experiment tracking and model logging.

Package overview
----------------

TensorflowTunable
    A tunable TensorFlow model class that extends the BaseTunableModel.

    Key functionality includes:
    - Training TensorFlow models with tunable hyperparameters.
    - Using Optuna for hyperparameter tuning to optimize model performance.
    - Saving and logging trained models with MLFlow for experiment tracking.
    - Supporting early stopping during training to prevent overfitting.
    - Evaluating models on training and testing datasets, returning predicted probabilities and labels.
"""
