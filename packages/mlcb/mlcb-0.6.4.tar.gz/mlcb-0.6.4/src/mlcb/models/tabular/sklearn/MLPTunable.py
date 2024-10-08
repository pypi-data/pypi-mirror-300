import optuna
from typing import Dict, Union
from sklearn.neural_network import MLPClassifier

from ....base_classes.sklearn.SklearnTunable import SklearnTunable

class MLPTunable(SklearnTunable):
    """
    A tunable scikit-learn model class implementing the Multi-layer Perceptron (MLP) classifier.

    This class uses Optuna for hyperparameter tuning to optimize the performance of the MLP classifier.

    Methods
    -------
    - build_model(hyperparameters: Dict[str, Union[int, float, str]]) -> MLPClassifier:
        Builds the MLP classifier model based on the provided hyperparameters.
    
    - _suggest_hyperparameters(trial: optuna.Trial) -> Dict[str, Union[int, float, str]]:
        Suggests a set of hyperparameters for tuning via the Optuna trial.
    """

    def build_model(self, hyperparameters: Dict[str, Union[int, float, str]]) -> MLPClassifier:
        """
        Builds the MLP classifier model based on the provided hyperparameters.

        Args:
            hyperparameters (Dict[str, Union[int, float, str]]): 
                Dictionary containing model hyperparameters. Expected keys include:
                - 'hidden_layer_sizes' (tuple or int): Size of the hidden layers.
                - 'activation' (str): Activation function for the hidden layers ('identity', 'logistic', 'tanh', 'relu').
                - 'solver' (str): Solver for weight optimization ('adam', 'sgd', 'lbfgs').
                - 'alpha' (float): L2 penalty (regularization term).
                - 'learning_rate' (str): Learning rate schedule ('constant', 'invscaling', 'adaptive').
                - 'learning_rate_init' (float): Initial learning rate used for training.
                - 'max_iter' (int): Maximum number of iterations for training.
                - 'tol' (float): Tolerance for the optimization.
                - 'momentum' (float): Momentum for gradient descent updates.
                - 'early_stopping' (bool): Whether to use early stopping during training.
                - 'n_iter_no_change' (int): Number of iterations with no improvement to wait before stopping.
                - 'beta_1' (float): Exponential decay rate for first moment estimates in Adam.
                - 'beta_2' (float): Exponential decay rate for second moment estimates in Adam.

        Returns:
            MLPClassifier: A Multi-layer Perceptron classifier model.
        """
        model = MLPClassifier(**hyperparameters)
        return model

    def _suggest_hyperparameters(self, trial: optuna.Trial) -> Dict[str, Union[int, float, str]]:
        """
        Suggests a set of hyperparameters for the Optuna trial.

        Args:
            trial (optuna.Trial): The Optuna trial instance for hyperparameter optimization.

        Returns:
            Dict[str, Union[int, float, str]]: A dictionary of suggested hyperparameters, including:
                - 'hidden_layer_sizes': Sizes of the hidden layers, suggested from a predefined list of options.
                - 'activation': Activation function for the hidden layers, suggested from ['identity', 'logistic', 'tanh', 'relu'].
                - 'solver': Solver for weight optimization, suggested from ['adam', 'sgd', 'lbfgs'].
                - 'alpha': L2 regularization term, suggested in log scale between 1e-6 and 1e-2.
                - 'learning_rate': Learning rate schedule, suggested from ['constant', 'invscaling', 'adaptive'].
                - 'learning_rate_init': Initial learning rate, suggested in log scale between 1e-5 and 1e-1.
                - 'max_iter': Maximum number of iterations, suggested between 100 and 2000.
                - 'tol': Tolerance for the optimization, suggested in log scale between 1e-6 and 1e-2.
                - 'momentum': Momentum for gradient descent, suggested between 0.0 and 1.0.
                - 'early_stopping': Whether to use early stopping, suggested from [True, False].
                - 'n_iter_no_change': Number of iterations with no improvement for early stopping, suggested between 5 and 20.
                - 'beta_1': Exponential decay rate for first moment estimates in Adam, suggested between 0.0 and 0.999.
                - 'beta_2': Exponential decay rate for second moment estimates in Adam, suggested between 0.0 and 0.999.
        """
        solver = trial.suggest_categorical('solver', ['adam', 'sgd', 'lbfgs'])
        momentum = trial.suggest_float('momentum', 0.0, 1.0)
        
        return {
            'hidden_layer_sizes': trial.suggest_categorical(
                'hidden_layer_sizes', [(50), (100), (50, 50), (100, 50), (100, 100), (150, 100), (150, 150)]
            ),
            'activation': trial.suggest_categorical('activation', ['identity', 'logistic', 'tanh', 'relu']),
            'solver': solver,
            'alpha': trial.suggest_float('alpha', 1e-6, 1e-2, log=True),
            'learning_rate': trial.suggest_categorical('learning_rate', ['constant', 'invscaling', 'adaptive']),
            'learning_rate_init': trial.suggest_float('learning_rate_init', 1e-5, 1e-1, log=True),
            'max_iter': trial.suggest_int('max_iter', 100, 2000),
            'tol': trial.suggest_float('tol', 1e-6, 1e-2, log=True),
            'momentum': momentum,
            'early_stopping': trial.suggest_categorical('early_stopping', [True, False]),
            'n_iter_no_change': trial.suggest_int('n_iter_no_change', 5, 20),
            'beta_1': trial.suggest_float('beta_1', 0.0, 0.999),
            'beta_2': trial.suggest_float('beta_2', 0.0, 0.999),
        }
