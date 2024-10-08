import optuna
from typing import Dict, Union
from sklearn.ensemble import BaggingClassifier
from ....base_classes.sklearn.SklearnTunable import SklearnTunable

class BaggingTunable(SklearnTunable):
    """
    A tunable scikit-learn model class implementing the Bagging algorithm.
    
    This class leverages scikit-learn's `BaggingClassifier` to build an ensemble model using 
    base estimators trained on different subsets of data. It also utilizes Optuna for 
    hyperparameter tuning to optimize model performance.

    Methods:
    --------
    - build_model(hyperparameters: Dict[str, Union[int, float, str]]) -> BaggingClassifier:
        Builds the Bagging model using the provided hyperparameters.
    
    - _suggest_hyperparameters(trial: optuna.Trial) -> Dict[str, Union[int, float, str]]:
        Suggests a set of hyperparameters for tuning via the Optuna trial.
    """

    def build_model(self, hyperparameters: Dict[str, Union[int, float, str]]) -> BaggingClassifier:
        """
        Builds the Bagging model based on the provided hyperparameters.

        Args:
            hyperparameters (Dict[str, Union[int, float, str]]): 
                Dictionary containing model hyperparameters. Expected keys:
                - 'n_estimators': The number of base estimators in the ensemble.
                - 'max_samples': The fraction of samples to draw from the training set for each base estimator.
                - 'max_features': The fraction of features to draw for each base estimator.
                - 'bootstrap': Whether samples are drawn with replacement (True/False).
                - 'bootstrap_features': Whether features are drawn with replacement (True/False).
                - 'oob_score': Whether to use out-of-bag samples to estimate generalization error (True/False).

        Returns:
            BaggingClassifier: An instance of the scikit-learn `BaggingClassifier` configured with the specified hyperparameters.
        """
        model = BaggingClassifier(**hyperparameters)
        return model

    def _suggest_hyperparameters(self, trial: optuna.Trial) -> Dict[str, Union[int, float, str]]:
        """
        Suggests a set of hyperparameters for tuning via the Optuna trial.

        Args:
            trial (optuna.Trial): The Optuna trial instance for hyperparameter optimization.

        Returns:
            Dict[str, Union[int, float, str]]: A dictionary containing suggested hyperparameters for the Bagging model.
                - 'n_estimators': Number of base estimators (range: 50 to 1000, step size: 50).
                - 'max_samples': Fraction of samples to use for each base estimator (range: 0.1 to 1.0, step size: 0.05).
                - 'max_features': Fraction of features to use for each base estimator (range: 0.1 to 1.0, step size: 0.05).
                - 'bootstrap': Whether samples are drawn with replacement (True/False).
                - 'bootstrap_features': Whether features are drawn with replacement (True/False).
                - 'oob_score': Whether to use out-of-bag samples for evaluation (True/False, only applicable if 'bootstrap' is True).
        """
        bootstrap = trial.suggest_categorical('bootstrap', [True, False])

        if bootstrap:
            oob_score = trial.suggest_categorical('oob_score', [True, False])
        else:
            oob_score = False

        return {
            'n_estimators': trial.suggest_int('n_estimators', 50, 1000, step=50),
            'max_samples': trial.suggest_float('max_samples', 0.1, 1.0, step=0.05),
            'max_features': trial.suggest_float('max_features', 0.1, 1.0, step=0.05),
            'bootstrap': bootstrap,
            'bootstrap_features': trial.suggest_categorical('bootstrap_features', [True, False]),
            'oob_score': oob_score
        }
