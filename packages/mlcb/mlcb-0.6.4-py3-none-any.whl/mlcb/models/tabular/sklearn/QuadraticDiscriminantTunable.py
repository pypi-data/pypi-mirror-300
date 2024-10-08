import optuna
from typing import Dict, Union
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis

from ....base_classes.sklearn.SklearnTunable import SklearnTunable

class QuadraticDiscriminantTunable(SklearnTunable):
    """
    A tunable scikit-learn model class implementing Quadratic Discriminant Analysis (QDA).

    This class utilizes Optuna for hyperparameter tuning to optimize the performance of the Quadratic Discriminant Analysis model.

    Methods
    -------
    - build_model(hyperparameters: Dict[str, Union[int, float, str]]) -> QuadraticDiscriminantAnalysis:
        Builds the Quadratic Discriminant Analysis classifier based on the provided hyperparameters.
    
    - _suggest_hyperparameters(trial: optuna.Trial) -> Dict[str, Union[int, float, str]]:
        Suggests a set of hyperparameters for the Optuna trial.
    """

    def build_model(self, hyperparameters: Dict[str, Union[int, float, str]]) -> QuadraticDiscriminantAnalysis:
        """
        Builds the Quadratic Discriminant Analysis model based on the provided hyperparameters.

        Args:
            hyperparameters (Dict[str, Union[int, float, str]]): 
                Dictionary containing model hyperparameters:
                - 'reg_param' (float): Regularization parameter to shrink the covariance estimates (between 0 and 1).
                - 'tol' (float): Tolerance threshold for rank estimation.
                - 'store_covariance' (bool): If True, the covariance matrices are computed and stored.

        Returns:
            QuadraticDiscriminantAnalysis: A Quadratic Discriminant Analysis classifier model.
        """
        model = QuadraticDiscriminantAnalysis(**hyperparameters)
        return model

    def _suggest_hyperparameters(self, trial: optuna.Trial) -> Dict[str, Union[int, float, str]]:
        """
        Suggests a set of hyperparameters for the Optuna trial.

        Args:
            trial (optuna.Trial): The Optuna trial instance for hyperparameter optimization.

        Returns:
            Dict[str, Union[int, float, str]]: 
                A dictionary of suggested hyperparameters, including:
                - 'reg_param' (float): Regularization parameter for covariance shrinkage (between 0.0 and 1.0).
                - 'tol' (float): Tolerance for rank estimation (log-uniform scale between 1e-6 and 1e-1).
                - 'store_covariance' (bool): Whether to store the covariance matrices (True or False).
        """
        return {
            'reg_param': trial.suggest_float('reg_param', 0.0, 1.0),
            'tol': trial.suggest_float('tol', 1e-6, 1e-1, log=True),
            'store_covariance': trial.suggest_categorical('store_covariance', [True, False]),
        }
