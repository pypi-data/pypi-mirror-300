import optuna
from typing import Dict, Union
from sklearn.ensemble import RandomForestClassifier

from ....base_classes.sklearn.SklearnTunable import SklearnTunable

class RandomForestTunable(SklearnTunable):
    """
    A tunable scikit-learn model class implementing the Random Forest algorithm.

    This class utilizes Optuna for hyperparameter tuning to optimize the performance of a Random Forest model.

    Methods
    -------
    - build_model(hyperparameters: Dict[str, Union[int, float, str]]) -> RandomForestClassifier:
        Builds the Random Forest classifier based on the provided hyperparameters.
    
    - _suggest_hyperparameters(trial: optuna.Trial) -> Dict[str, Union[int, float, str]]:
        Suggests a set of hyperparameters for the Optuna trial.
    """

    def build_model(self, hyperparameters: Dict[str, Union[int, float, str]]) -> RandomForestClassifier:
        """
        Builds the Random Forest model based on the provided hyperparameters.

        Args:
            hyperparameters (Dict[str, Union[int, float, str]]): 
                Dictionary containing model hyperparameters, including:
                - 'n_estimators' (int): The number of trees in the forest.
                - 'criterion' (str): The function to measure the quality of a split ('gini', 'entropy', or 'log_loss').
                - 'max_depth' (int): The maximum depth of the tree.
                - 'min_samples_split' (int): The minimum number of samples required to split an internal node.
                - 'min_samples_leaf' (int): The minimum number of samples required to be at a leaf node.
                - 'max_features' (str or None): The number of features to consider when looking for the best split ('log2', 'sqrt', or None).
                - 'bootstrap' (bool): Whether bootstrap samples are used when building trees.
                - 'random_state' (int): The seed used by the random number generator.

        Returns:
            RandomForestClassifier: A Random Forest classifier model.
        """
        model = RandomForestClassifier(**hyperparameters)
        return model

    def _suggest_hyperparameters(self, trial: optuna.Trial) -> Dict[str, Union[int, float, str]]:
        """
        Suggests a set of hyperparameters for the Optuna trial.

        Args:
            trial (optuna.Trial): The Optuna trial instance for hyperparameter optimization.

        Returns:
            Dict[str, Union[int, float, str]]:
                A dictionary of suggested hyperparameters, including:
                - 'n_estimators' (int): Number of trees in the forest, suggested between 50 and 2000 with steps of 50.
                - 'criterion' (str): Criterion to measure the quality of a split ('gini', 'entropy', or 'log_loss').
                - 'max_depth' (int): Maximum depth of the tree, suggested between 1 and 100.
                - 'min_samples_split' (int): Minimum number of samples to split an internal node, suggested between 2 and 50.
                - 'min_samples_leaf' (int): Minimum number of samples at a leaf node, suggested between 1 and 50.
                - 'max_features' (str or None): Number of features to consider when splitting ('log2', 'sqrt', or None).
                - 'bootstrap' (bool): Whether to use bootstrap samples, suggested as True or False.
                - 'random_state' (int): Random seed, suggested between 1 and 10000.
        """
        return {
            'n_estimators': trial.suggest_int('n_estimators', 50, 2000, step=50),
            'criterion': trial.suggest_categorical('criterion', ['gini', 'entropy', 'log_loss']),
            'max_depth': trial.suggest_int('max_depth', 1, 100),
            'min_samples_split': trial.suggest_int('min_samples_split', 2, 50),
            'min_samples_leaf': trial.suggest_int('min_samples_leaf', 1, 50),
            'max_features': trial.suggest_categorical('max_features', [None, 'log2', 'sqrt']),
            'bootstrap': trial.suggest_categorical('bootstrap', [True, False]),
            'random_state': trial.suggest_int('random_state', 1, 10000)
        }
