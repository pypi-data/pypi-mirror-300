import optuna
from typing import Dict, Union
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

from ....base_classes.sklearn.SklearnTunable import SklearnTunable

class LinearDiscriminantTunable(SklearnTunable):
    """
    A tunable scikit-learn model class implementing Linear Discriminant Analysis (LDA).
    
    This class uses Optuna for hyperparameter tuning to optimize the performance of the Linear Discriminant Analysis model.
    
    Methods
    -------
    - build_model(hyperparameters: Dict[str, Union[int, float, str]]) -> LinearDiscriminantAnalysis:
        Builds the LDA model based on the provided hyperparameters.
    
    - _suggest_hyperparameters(trial: optuna.Trial) -> Dict[str, Union[int, float, str]]:
        Suggests a set of hyperparameters for tuning via the Optuna trial.
    """

    def build_model(self, hyperparameters: Dict[str, Union[int, float, str]]) -> LinearDiscriminantAnalysis:
        """
        Builds the Linear Discriminant Analysis model based on the provided hyperparameters.

        Args:
            hyperparameters (Dict[str, Union[int, float, str]]): 
                Dictionary containing model hyperparameters. Expected keys include:
                - 'solver' (str): Solver to use in the LDA algorithm ('svd', 'lsqr', 'eigen').
                - 'tol' (float): Tolerance for singular value decomposition (SVD) solver.

        Returns:
            LinearDiscriminantAnalysis: A Linear Discriminant Analysis classifier model.
        """
        model = LinearDiscriminantAnalysis(**hyperparameters)
        return model

    def _suggest_hyperparameters(self, trial: optuna.Trial) -> Dict[str, Union[int, float, str]]:
        """
        Suggests a set of hyperparameters for the Optuna trial.

        Args:
            trial (optuna.Trial): The Optuna trial instance for hyperparameter optimization.

        Returns:
            Dict[str, Union[int, float, str]]: A dictionary of suggested hyperparameters, including:
                - 'solver': Solver used for LDA, suggested from ['svd', 'lsqr', 'eigen'].
                - 'tol': Tolerance for SVD solver, suggested between 1e-5 and 1e-1.
        """
        solver = trial.suggest_categorical('solver', ['svd', 'lsqr', 'eigen'])

        return {
            'solver': solver,
            'tol': trial.suggest_float('tol', 1e-5, 1e-1, log=True)
        }
