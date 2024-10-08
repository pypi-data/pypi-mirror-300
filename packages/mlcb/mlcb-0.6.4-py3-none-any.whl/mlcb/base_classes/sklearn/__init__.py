"""
This module provides functionality for building, tuning, and saving tunable scikit-learn models. It integrates with 
Optuna for hyperparameter optimization and MLFlow for experiment tracking and model logging.

Package overview
----------------

SklearnTunable
    A tunable scikit-learn model class that extends the BaseTunableModel.

    Key functionality includes:
    - Training scikit-learn models with tunable hyperparameters.
    - Using Optuna for hyperparameter tuning to optimize model performance.
    - Saving and logging trained models with MLFlow for experiment tracking.
    - Supporting the evaluation of models on training and testing datasets.
"""
