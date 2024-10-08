import optuna
from typing import Dict, Union
from sklearn.ensemble import GradientBoostingClassifier

from ....base_classes.sklearn.SklearnTunable import SklearnTunable

class GradientBoostingTunable(SklearnTunable):
    """
    A tunable scikit-learn model class implementing the Gradient Boosting algorithm.
    
    This class provides functionality to:
    - Build and train a Gradient Boosting classifier using scikit-learn's `GradientBoostingClassifier`.
    - Use Optuna for hyperparameter tuning to optimize model performance.

    Methods
    -------
    - build_model(hyperparameters: Dict[str, Union[int, float, str]]) -> GradientBoostingClassifier:
        Builds the Gradient Boosting model based on the provided hyperparameters.
    
    - _suggest_hyperparameters(trial: optuna.Trial) -> Dict[str, Union[int, float, str]]:
        Suggests a set of hyperparameters for tuning via the Optuna trial.
    """

    def build_model(self, hyperparameters: Dict[str, Union[int, float, str]]) -> GradientBoostingClassifier:
        """
        Builds the Gradient Boosting model based on the provided hyperparameters.

        Args:
            hyperparameters (Dict[str, Union[int, float, str]]): 
                Dictionary containing model hyperparameters. Expected keys include:
                - 'learning_rate' (float): The learning rate shrinks the contribution of each tree.
                - 'n_estimators' (int): The number of boosting stages to be run.
                - 'subsample' (float): The fraction of samples used for fitting the individual base learners.
                - 'criterion' (str): The function to measure the quality of splits.
                - 'min_samples_split' (int): The minimum number of samples required to split an internal node.
                - 'min_samples_leaf' (int): The minimum number of samples required to be at a leaf node.
                - 'max_depth' (int): The maximum depth of the individual base learners.
                - 'max_features' (str or None): The number of features to consider when looking for the best split.

        Returns:
            GradientBoostingClassifier: A Gradient Boosting classifier model.
        """
        model = GradientBoostingClassifier(**hyperparameters)
        return model

    def _suggest_hyperparameters(self, trial: optuna.Trial) -> Dict[str, Union[int, float, str]]:
        """
        Suggests a set of hyperparameters for the Optuna trial.

        Args:
            trial (optuna.Trial): The Optuna trial instance for hyperparameter optimization.

        Returns:
            Dict[str, Union[int, float, str]]: A dictionary of suggested hyperparameters, which includes:
                - 'learning_rate': A learning rate sampled between 1e-4 and 1.0.
                - 'n_estimators': Number of boosting stages to be run, between 50 and 2000.
                - 'subsample': Fraction of samples used for fitting the base learners, sampled between 0.5 and 1.0.
                - 'criterion': The function to measure the quality of a split ('friedman_mse' or 'squared_error').
                - 'min_samples_split': Minimum samples required to split an internal node (2 to 50).
                - 'min_samples_leaf': Minimum samples required to be at a leaf node (1 to 50).
                - 'max_depth': Maximum depth of the individual base learners (1 to 100).
                - 'max_features': Number of features to consider for the best split (None, 'log2', or 'sqrt').
        """
        return {
            'learning_rate': trial.suggest_float('learning_rate', 1e-4, 1.0, log=True),
            'n_estimators': trial.suggest_int('n_estimators', 50, 2000, step=50),
            'subsample': trial.suggest_float('subsample', 0.5, 1.0, step=0.05),
            'criterion': trial.suggest_categorical('criterion', ['friedman_mse', 'squared_error']),
            'min_samples_split': trial.suggest_int('min_samples_split', 2, 50),
            'min_samples_leaf': trial.suggest_int('min_samples_leaf', 1, 50),
            'max_depth': trial.suggest_int('max_depth', 1, 100),
            'max_features': trial.suggest_categorical('max_features', [None, 'log2', 'sqrt'])
        }
