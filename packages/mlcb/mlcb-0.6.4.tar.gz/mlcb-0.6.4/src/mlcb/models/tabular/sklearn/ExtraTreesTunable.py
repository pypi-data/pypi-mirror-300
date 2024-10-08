import optuna
from typing import Dict, Union
from sklearn.ensemble import ExtraTreesClassifier

from ....base_classes.sklearn.SklearnTunable import SklearnTunable

class ExtraTreesTunable(SklearnTunable):
    """
    A tunable scikit-learn model class implementing the Extra Trees (Extremely Randomized Trees) algorithm.
    
    This class provides functionality to:
    - Build and train an Extra Trees classifier using scikit-learn's `ExtraTreesClassifier`.
    - Use Optuna for hyperparameter tuning to optimize model performance.

    Methods
    -------
    - build_model(hyperparameters: Dict[str, Union[int, float, str]]) -> ExtraTreesClassifier:
        Builds the Extra Trees model based on the provided hyperparameters.
    
    - _suggest_hyperparameters(trial: optuna.Trial) -> Dict[str, Union[int, float, str]]:
        Suggests a set of hyperparameters for tuning via the Optuna trial.
    """

    def build_model(self, hyperparameters: Dict[str, Union[int, float, str]]) -> ExtraTreesClassifier:
        """
        Builds the Extra Trees model based on the provided hyperparameters.

        Args:
            hyperparameters (Dict[str, Union[int, float, str]]): 
                Dictionary containing model hyperparameters. Expected keys:
                - 'n_estimators' (int): Number of trees in the forest.
                - 'criterion' (str): Function to measure the quality of a split ('gini', 'entropy', 'log_loss').
                - 'max_depth' (int): Maximum depth of the tree.
                - 'min_samples_split' (int): Minimum number of samples required to split an internal node.
                - 'min_samples_leaf' (int): Minimum number of samples required to be at a leaf node.
                - 'max_features' (str or None): Number of features to consider for the best split ('None', 'log2', 'sqrt').
                - 'bootstrap' (bool): Whether to use bootstrap sampling when building trees.
                - 'min_impurity_decrease' (float): Minimum impurity decrease required to split a node.

        Returns:
            ExtraTreesClassifier: An Extra Trees classifier model.
        """
        model = ExtraTreesClassifier(**hyperparameters)
        return model

    def _suggest_hyperparameters(self, trial: optuna.Trial) -> Dict[str, Union[int, float, str]]:
        """
        Suggests a set of hyperparameters for the Optuna trial.

        Args:
            trial (optuna.Trial): The Optuna trial instance for hyperparameter optimization.

        Returns:
            Dict[str, Union[int, float, str]]: A dictionary of suggested hyperparameters for the model.
                - 'n_estimators' (int): Number of trees in the forest (50 to 2000).
                - 'criterion' (str): Criterion for evaluating split quality ('gini', 'entropy', 'log_loss').
                - 'max_depth' (int): Maximum depth of the tree (1 to 1000).
                - 'min_samples_split' (int): Minimum samples required to split a node (2 to 50).
                - 'min_samples_leaf' (int): Minimum samples at a leaf node (1 to 50).
                - 'max_features' (str or None): Features to consider for splitting ('None', 'log2', 'sqrt').
                - 'bootstrap' (bool): Whether to use bootstrap sampling ('True' or 'False').
                - 'min_impurity_decrease' (float): Minimum decrease in impurity for a split (0.0 to 0.5).
        """
        return {
            'n_estimators': trial.suggest_int('n_estimators', 50, 2000, step=50),
            'criterion': trial.suggest_categorical('criterion', ['gini', 'entropy', 'log_loss']),
            'max_depth': trial.suggest_int('max_depth', 1, 1000),
            'min_samples_split': trial.suggest_int('min_samples_split', 2, 50),
            'min_samples_leaf': trial.suggest_int('min_samples_leaf', 1, 50),
            'max_features': trial.suggest_categorical('max_features', [None, 'log2', 'sqrt']),
            'bootstrap': trial.suggest_categorical('bootstrap', [True, False]),
            'min_impurity_decrease': trial.suggest_float('min_impurity_decrease', 0.0, 0.5, step=0.01)
        }
