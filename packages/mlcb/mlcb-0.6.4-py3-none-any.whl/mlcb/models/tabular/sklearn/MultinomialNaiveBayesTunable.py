import optuna
from typing import Dict, Union
from sklearn.naive_bayes import MultinomialNB

from ....base_classes.sklearn.SklearnTunable import SklearnTunable

class MultinomialNaiveBayesTunable(SklearnTunable):
    """
    A tunable scikit-learn model class implementing the Multinomial Naive Bayes algorithm.

    This class utilizes Optuna for hyperparameter tuning to optimize the performance of the Multinomial Naive Bayes model.

    Methods
    -------
    - build_model(hyperparameters: Dict[str, Union[int, float, str]]) -> MultinomialNB:
        Builds the Multinomial Naive Bayes classifier model based on the provided hyperparameters.
    
    - _suggest_hyperparameters(trial: optuna.Trial) -> Dict[str, Union[int, float, str]]:
        Suggests a set of hyperparameters for tuning via the Optuna trial.
    """

    def build_model(self, hyperparameters: Dict[str, Union[int, float, str]]) -> MultinomialNB:
        """
        Builds the Multinomial Naive Bayes model based on the provided hyperparameters.

        Args:
            hyperparameters (Dict[str, Union[int, float, str]]): 
                Dictionary containing model hyperparameters:
                - 'alpha' (float): Additive (Laplace/Lidstone) smoothing parameter.
                - 'fit_prior' (bool): Whether to learn class prior probabilities or not.

        Returns:
            MultinomialNB: A Multinomial Naive Bayes classifier model.
        """
        model = MultinomialNB(**hyperparameters)
        return model

    def _suggest_hyperparameters(self, trial: optuna.Trial) -> Dict[str, Union[int, float, str]]:
        """
        Suggests a set of hyperparameters for the Optuna trial.

        Args:
            trial (optuna.Trial): The Optuna trial instance for hyperparameter optimization.

        Returns:
            Dict[str, Union[int, float, str]]: 
                A dictionary of suggested hyperparameters, including:
                - 'alpha': Additive smoothing parameter (sampled in log scale between 1e-4 and 100).
                - 'fit_prior': Whether to learn class prior probabilities (True or False).
        """
        return {
            'alpha': trial.suggest_float('alpha', 1e-4, 100.0, log=True),
            'fit_prior': trial.suggest_categorical('fit_prior', [True, False]),
        }
