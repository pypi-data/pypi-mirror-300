import optuna
from typing import Dict, Union
from sklearn.tree import DecisionTreeClassifier

from ....base_classes.sklearn.SklearnTunable import SklearnTunable

class DecisionTreeTunable(SklearnTunable):
    """
    A tunable scikit-learn model class implementing the Decision Tree algorithm.
    
    This class leverages scikit-learn's `DecisionTreeClassifier` to build and train a Decision Tree model. 
    It also uses Optuna for hyperparameter tuning to optimize model performance.

    Methods:
    --------
    - build_model(hyperparameters: Dict[str, Union[int, float, str]]) -> DecisionTreeClassifier:
        Builds the Decision Tree model based on the provided hyperparameters.
    
    - _suggest_hyperparameters(trial: optuna.Trial) -> Dict[str, Union[int, float, str]]:
        Suggests a set of hyperparameters for tuning via the Optuna trial.
    """

    def build_model(self, hyperparameters: Dict[str, Union[int, float, str]]) -> DecisionTreeClassifier:
        """
        Builds the Decision Tree model based on the provided hyperparameters.

        Args:
            hyperparameters (Dict[str, Union[int, float, str]]): 
                Dictionary containing model hyperparameters. Expected keys:
                - 'criterion' (str): The function to measure the quality of a split ('gini', 'entropy', 'log_loss').
                - 'splitter' (str): Strategy used to split at each node ('best', 'random').
                - 'max_depth' (int): Maximum depth of the tree.
                - 'min_samples_split' (int): Minimum number of samples required to split an internal node.
                - 'min_samples_leaf' (int): Minimum number of samples required to be at a leaf node.
                - 'max_features' (str or None): Number of features to consider for the best split ('None', 'log2', 'sqrt').
                - 'min_impurity_decrease' (float): Minimum impurity decrease to split a node.

        Returns:
            DecisionTreeClassifier: A Decision Tree classifier model.
        """
        model = DecisionTreeClassifier(**hyperparameters)
        return model

    def _suggest_hyperparameters(self, trial: optuna.Trial) -> Dict[str, Union[int, float, str]]:
        """
        Suggests a set of hyperparameters for the Optuna trial.

        Args:
            trial (optuna.Trial): The Optuna trial instance for hyperparameter optimization.

        Returns:
            Dict[str, Union[int, float, str]]: A dictionary of suggested hyperparameters for the model.
                - 'criterion' (str): Criterion for evaluating split quality ('gini', 'entropy', 'log_loss').
                - 'splitter' (str): Strategy to split nodes ('best', 'random').
                - 'max_depth' (int): Maximum depth of the tree (1 to 100).
                - 'min_samples_split' (int): Minimum samples to split a node (2 to 40).
                - 'min_samples_leaf' (int): Minimum samples at a leaf node (1 to 20).
                - 'max_features' (str or None): Features to consider for splitting ('None', 'log2', 'sqrt').
                - 'min_impurity_decrease' (float): Minimum decrease in impurity for a split (0.0 to 0.5).
        """
        return {
            'criterion': trial.suggest_categorical('criterion', ['gini', 'entropy', 'log_loss']),
            'splitter': trial.suggest_categorical('splitter', ['best', 'random']),
            'max_depth': trial.suggest_int('max_depth', 1, 100),
            'min_samples_split': trial.suggest_int('min_samples_split', 2, 40),
            'min_samples_leaf': trial.suggest_int('min_samples_leaf', 1, 20),
            'max_features': trial.suggest_categorical('max_features', [None, 'log2', 'sqrt']),
            'min_impurity_decrease': trial.suggest_float('min_impurity_decrease', 0.0, 0.5, step=0.01)
        }
