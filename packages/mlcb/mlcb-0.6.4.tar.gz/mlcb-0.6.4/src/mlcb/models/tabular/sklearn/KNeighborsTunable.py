import optuna
from typing import Dict, Union
from sklearn.neighbors import KNeighborsClassifier

from ....base_classes.sklearn.SklearnTunable import SklearnTunable

class KNeighborsTunable(SklearnTunable):
    """
    A tunable scikit-learn model class implementing the K-Nearest Neighbors (KNN) algorithm.
    
    This class uses Optuna for hyperparameter tuning to optimize the performance of the `KNeighborsClassifier`.
    
    Methods
    -------
    - build_model(hyperparameters: Dict[str, Union[int, float, str]]) -> KNeighborsClassifier:
        Builds the K-Nearest Neighbors model based on provided hyperparameters.
    
    - _suggest_hyperparameters(trial: optuna.Trial) -> Dict[str, Union[int, float, str]]:
        Suggests a set of hyperparameters for tuning via the Optuna trial.
    """

    def build_model(self, hyperparameters: Dict[str, Union[int, float, str]]) -> KNeighborsClassifier:
        """
        Builds the K-Nearest Neighbors (KNN) model based on the provided hyperparameters.

        Args:
            hyperparameters (Dict[str, Union[int, float, str]]): 
                Dictionary containing model hyperparameters. Expected keys:
                - 'n_neighbors' (int): Number of neighbors to use.
                - 'weights' (str): Weight function used in prediction ('uniform' or 'distance').
                - 'algorithm' (str): Algorithm to compute the nearest neighbors ('auto', 'ball_tree', 'kd_tree', or 'brute').
                - 'leaf_size' (int): Leaf size passed to BallTree or KDTree.
                - 'p' (int): Power parameter for the Minkowski distance metric.

        Returns:
            KNeighborsClassifier: A K-Nearest Neighbors classifier model.
        """
        model = KNeighborsClassifier(**hyperparameters)
        return model

    def _suggest_hyperparameters(self, trial: optuna.Trial) -> Dict[str, Union[int, float, str]]:
        """
        Suggests a set of hyperparameters for the Optuna trial.

        Args:
            trial (optuna.Trial): The Optuna trial instance for hyperparameter optimization.

        Returns:
            Dict[str, Union[int, float, str]]: A dictionary of suggested hyperparameters including:
                - 'n_neighbors' (int): The number of neighbors, suggested between 1 and 50.
                - 'weights' (str): The weight function for prediction ('uniform' or 'distance').
                - 'algorithm' (str): The algorithm used to compute the nearest neighbors ('auto', 'ball_tree', 'kd_tree', 'brute').
                - 'leaf_size' (int): The leaf size for BallTree or KDTree, suggested between 10 and 200.
                - 'p' (int): Power parameter for the Minkowski distance, suggested between 1 and 5.
        """
        return {
            'n_neighbors': trial.suggest_int('n_neighbors', 1, 50),
            'weights': trial.suggest_categorical('weights', ['uniform', 'distance']),
            'algorithm': trial.suggest_categorical('algorithm', ['auto', 'ball_tree', 'kd_tree', 'brute']),
            'leaf_size': trial.suggest_int('leaf_size', 10, 200),
            'p': trial.suggest_int('p', 1, 5)
        }
