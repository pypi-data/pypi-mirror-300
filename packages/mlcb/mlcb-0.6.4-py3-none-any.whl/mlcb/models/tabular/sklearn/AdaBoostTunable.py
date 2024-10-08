import optuna
from typing import Dict, Union
from sklearn.ensemble import AdaBoostClassifier
from ....base_classes.sklearn.SklearnTunable import SklearnTunable

class AdaBoostTunable(SklearnTunable):
    """
    A tunable scikit-learn model class implementing the AdaBoost algorithm.

    This class leverages scikit-learn's `AdaBoostClassifier` to build a boosting model and utilizes Optuna 
    for hyperparameter tuning. AdaBoost combines multiple weak classifiers to create a stronger model by 
    iteratively training new models that focus on previously misclassified examples.

    Methods:
    --------
    - build_model(hyperparameters: Dict[str, Union[int, float, str]]) -> AdaBoostClassifier:
        Builds the AdaBoost model using the provided hyperparameters.
    
    - _suggest_hyperparameters(trial: optuna.Trial) -> Dict[str, Union[int, float, str]]:
        Suggests a set of hyperparameters for tuning via the Optuna trial.
    """

    def build_model(self, hyperparameters: Dict[str, Union[int, float, str]]) -> AdaBoostClassifier:
        """
        Builds the AdaBoost model using the provided hyperparameters.

        Args:
            hyperparameters (Dict[str, Union[int, float, str]]): 
                Dictionary containing model hyperparameters. Expected keys:
                - 'n_estimators': Number of boosting stages to run (default: 50).
                - 'learning_rate': Weight applied to each classifier at each boosting iteration.

        Returns:
            AdaBoostClassifier: An instance of the scikit-learn `AdaBoostClassifier` configured with the specified hyperparameters.
        """
        model = AdaBoostClassifier(**hyperparameters, algorithm='SAMME')
        return model

    def _suggest_hyperparameters(self, trial: optuna.Trial) -> Dict[str, Union[int, float, str]]:
        """
        Suggests a set of hyperparameters for tuning via the Optuna trial.

        Args:
            trial (optuna.Trial): The Optuna trial instance for hyperparameter optimization.

        Returns:
            Dict[str, Union[int, float, str]]: A dictionary containing suggested hyperparameters for the AdaBoost model.
                - 'n_estimators': Number of estimators (suggested range: 50 to 1000, with step size of 50).
                - 'learning_rate': Learning rate for the model (log-uniform search between 0.01 and 2.0).
        """
        return {
            'n_estimators': trial.suggest_int('n_estimators', 50, 1000, step=50),
            'learning_rate': trial.suggest_float('learning_rate', 0.01, 2.0, log=True),
        }
