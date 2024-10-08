import optuna
from typing import Dict, Union
from sklearn.naive_bayes import BernoulliNB
from ....base_classes.sklearn.SklearnTunable import SklearnTunable

class BernoulliNaiveBayesTunable(SklearnTunable):
    """
    A tunable scikit-learn model class implementing the Bernoulli Naive Bayes algorithm.
    
    This class leverages scikit-learn's `BernoulliNB` to build and train a Bernoulli Naive Bayes model.
    It also uses Optuna for hyperparameter tuning to optimize the model's performance.

    Methods:
    --------
    - build_model(hyperparameters: Dict[str, Union[int, float, str]]) -> BernoulliNB:
        Builds the Bernoulli Naive Bayes model based on the provided hyperparameters.
    
    - _suggest_hyperparameters(trial: optuna.Trial) -> Dict[str, Union[int, float, str]]:
        Suggests a set of hyperparameters for tuning via the Optuna trial.
    """

    def build_model(self, hyperparameters: Dict[str, Union[int, float, str]]) -> BernoulliNB:
        """
        Builds the Bernoulli Naive Bayes model based on the provided hyperparameters.

        Args:
            hyperparameters (Dict[str, Union[int, float, str]]): 
                Dictionary containing model hyperparameters. Expected keys:
                - 'alpha': Additive smoothing parameter (float).
                - 'binarize': Threshold for binarizing (mapping to 0 or 1) the input features (float).
                - 'fit_prior': Whether to learn class prior probabilities or not (boolean).

        Returns:
            BernoulliNB: An instance of the scikit-learn `BernoulliNB` classifier.
        """
        model = BernoulliNB(**hyperparameters)
        return model

    def _suggest_hyperparameters(self, trial: optuna.Trial) -> Dict[str, Union[int, float, str]]:
        """
        Suggests a set of hyperparameters for tuning via the Optuna trial.

        Args:
            trial (optuna.Trial): The Optuna trial instance for hyperparameter optimization.

        Returns:
            Dict[str, Union[int, float, str]]: A dictionary containing suggested hyperparameters for the Bernoulli Naive Bayes model.
                - 'alpha': Additive smoothing parameter (1e-4 to 100.0, log scale).
                - 'binarize': Threshold for binarizing the input features (range: 0.0 to 1.0, step: 0.1).
                - 'fit_prior': Whether to learn class prior probabilities (True/False).
        """
        return {
            'alpha': trial.suggest_float('alpha', 1e-4, 100.0, log=True),
            'binarize': trial.suggest_float('binarize', 0.0, 1.0, step=0.1),
            'fit_prior': trial.suggest_categorical('fit_prior', [True, False])
        }
