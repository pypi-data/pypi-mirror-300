import optuna
from typing import Dict, Union
from sklearn.naive_bayes import GaussianNB

from ....base_classes.sklearn.SklearnTunable import SklearnTunable

class GaussianNaiveBayesTunable(SklearnTunable):
    """
    A tunable scikit-learn model class implementing the Gaussian Naive Bayes algorithm.
    
    This class provides functionality to:
    - Build and train a Gaussian Naive Bayes classifier using scikit-learn's `GaussianNB`.
    - Use Optuna for hyperparameter tuning to optimize model performance.
    
    Methods
    -------
    - build_model(hyperparameters: Dict[str, Union[int, float, str]]) -> GaussianNB:
        Builds the Gaussian Naive Bayes model based on the provided hyperparameters.
    
    - _suggest_hyperparameters(trial: optuna.Trial) -> Dict[str, Union[int, float, str]]:
        Suggests a set of hyperparameters for tuning via the Optuna trial.
    """

    def build_model(self, hyperparameters: Dict[str, Union[int, float, str]]) -> GaussianNB:
        """
        Builds the Gaussian Naive Bayes model based on the provided hyperparameters.

        Args:
            hyperparameters (Dict[str, Union[int, float, str]]): 
                Dictionary containing model hyperparameters. Expected key:
                - 'var_smoothing' (float): Portion of the largest variance of all features to be added 
                   to variances for numerical stability.

        Returns:
            GaussianNB: A Gaussian Naive Bayes classifier model.
        """
        model = GaussianNB(**hyperparameters)
        return model

    def _suggest_hyperparameters(self, trial: optuna.Trial) -> Dict[str, Union[int, float, str]]:
        """
        Suggests a set of hyperparameters for the Optuna trial.

        Args:
            trial (optuna.Trial): The Optuna trial instance for hyperparameter optimization.

        Returns:
            Dict[str, Union[int, float, str]]: A dictionary of suggested hyperparameters.
                - 'var_smoothing' (float): A small positive value to be added to the variance for stability 
                   (log-uniformly sampled between 1e-12 and 1e-5).
        """
        return {
            'var_smoothing': trial.suggest_float('var_smoothing', 1e-12, 1e-5, log=True)
        }
