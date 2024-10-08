import optuna
from typing import Dict, Union
from sklearn.naive_bayes import ComplementNB

from ....base_classes.sklearn.SklearnTunable import SklearnTunable

class ComplementNaiveBayesTunable(SklearnTunable):
    """
    A tunable scikit-learn model class implementing the Complement Naive Bayes algorithm.
    
    This class leverages scikit-learn's `ComplementNB` to build and train a Complement Naive Bayes model.
    It also uses Optuna for hyperparameter tuning to optimize the model's performance.

    Methods:
    --------
    - build_model(hyperparameters: Dict[str, Union[int, float, str]]) -> ComplementNB:
        Builds the Complement Naive Bayes model based on the provided hyperparameters.
    
    - _suggest_hyperparameters(trial: optuna.Trial) -> Dict[str, Union[int, float, str]]:
        Suggests a set of hyperparameters for tuning via the Optuna trial.
    """

    def build_model(self, hyperparameters: Dict[str, Union[int, float, str]]) -> ComplementNB:
        """
        Builds the Complement Naive Bayes model based on the provided hyperparameters.

        Args:
            hyperparameters (Dict[str, Union[int, float, str]]): 
                Dictionary containing model hyperparameters. Expected keys:
                - 'alpha': Additive smoothing parameter (float).
                - 'fit_prior': Whether to learn class prior probabilities or not (boolean).
                - 'norm': Whether to normalize weights by the total number of features in each class (boolean).

        Returns:
            ComplementNB: An instance of the scikit-learn `ComplementNB` classifier.
        """
        model = ComplementNB(**hyperparameters)
        return model

    def _suggest_hyperparameters(self, trial: optuna.Trial) -> Dict[str, Union[int, float, str]]:
        """
        Suggests a set of hyperparameters for tuning via the Optuna trial.

        Args:
            trial (optuna.Trial): The Optuna trial instance for hyperparameter optimization.

        Returns:
            Dict[str, Union[int, float, str]]: A dictionary containing suggested hyperparameters for the 
            Complement Naive Bayes model.
                - 'alpha': Smoothing parameter for ComplementNB (1e-4 to 100.0, log scale).
                - 'fit_prior': Whether to learn class prior probabilities (True/False).
                - 'norm': Whether to normalize the weights by the total number of features in each class (True/False).
        """
        return {
            'alpha': trial.suggest_float('alpha', 1e-4, 100.0, log=True),
            'fit_prior': trial.suggest_categorical('fit_prior', [True, False]),
            'norm': trial.suggest_categorical('norm', [True, False])
        }
