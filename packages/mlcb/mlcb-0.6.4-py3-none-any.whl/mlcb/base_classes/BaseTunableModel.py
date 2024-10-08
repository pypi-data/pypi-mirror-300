from abc import ABC, abstractmethod
from typing import Tuple, Union, Dict, Any, Callable, Optional
import warnings
import numpy as np
import optuna
from mlflow.models import infer_signature
import optuna.importance

from .helpers.MetricsHelper import MetricsHelper
from .helpers.PlotHelper import PlotHelper
from .helpers.MLFlowLogger import MLFlowLogger

class BaseTunableModel(ABC):
    """
    Abstract base class for tunable machine learning models. Supports hyperparameter tuning, model training, 
    evaluation, and logging with Optuna and MLFlow.

    Attributes
    ----------
    train_features : np.ndarray
        Features for the training dataset.
    train_labels : np.ndarray
        Labels for the training dataset.
    test_features : np.ndarray
        Features for the test dataset.
    test_labels : np.ndarray
        Labels for the test dataset.
    best_model : Any
        The best model after hyperparameter tuning.
    logger : Optional[MLFlowLogger]
        Logger for tracking experiments and metrics with MLFlow.
    additional_metrics : Optional[Callable]
        A callable to compute additional custom metrics during evaluation.
    """
    
    def __init__(self, 
                 train_features: np.ndarray, 
                 train_labels: np.ndarray, 
                 test_features: np.ndarray, 
                 test_labels: np.ndarray, 
                 additional_metrics: Optional[Callable] = None):
        """
        Initializes the BaseTunableModel with training and testing data.

        Parameters
        ----------
        train_features : np.ndarray
            The features for the training dataset.
        train_labels : np.ndarray
            The labels for the training dataset.
        test_features : np.ndarray
            The features for the test dataset.
        test_labels : np.ndarray
            The labels for the test dataset.
        additional_metrics : Optional[Callable], optional
            A callable to compute additional custom metrics during evaluation (default is None).
        """
        self.train_features = train_features
        self.train_labels = train_labels
        self.test_features = test_features
        self.test_labels = test_labels
        self.best_model = None
        self.logger = None
        self.additional_metrics = additional_metrics

    def tune(self, 
             n_trials: int, 
             experiment_name: str = 'Tuning', 
             run_name: Optional[str] = None, 
             log_nested: bool = False, 
             direction: str = 'maximize', 
             metric: str = 'accuracy') -> Dict[str, Any]:
        """
        Tunes the model using Optuna for hyperparameter optimization.

        This method creates an Optuna study to explore different hyperparameter configurations and logs the results 
        with MLFlow. The best model is stored and evaluated after tuning.

        Parameters
        ----------
        n_trials : int
            The number of trials to run for hyperparameter tuning.
        experiment_name : str, optional
            The name of the MLFlow experiment (default is 'Tuning').
        run_name : Optional[str], optional
            The name of the tuning run (default is the class name).
        log_nested : bool, optional
            Whether to log nested runs for each trial (default is False).
        direction : str, optional
            The direction of optimization, either 'maximize' or 'minimize' (default is 'maximize').
        metric : str, optional
            The main metric to optimize (default is 'accuracy').

        Returns
        -------
        Dict[str, Any]
            The best hyperparameters from the tuning process.
        """
        run_name = run_name if run_name is not None else f"{self.__class__.__name__}"
        self.logger = MLFlowLogger(run_name=run_name, experiment_name=experiment_name)
        self.logger.start_run()
        try:
            study = optuna.create_study(direction=direction)
            study.optimize(lambda trial: self._objective(trial, log_nested, metric), n_trials=n_trials, gc_after_trial=True)
            self.best_model = study.best_trial.user_attrs['best_model']

            probabilities, predictions = self._evaluate(self.best_model, dataset='test')
            best_model_metrics = MetricsHelper.calculate_metrics(self.test_labels, probabilities, predictions)

            if self.additional_metrics:
                additional_metrics = self.additional_metrics(self.test_labels, probabilities, predictions)
                best_model_metrics.update(additional_metrics)

            self.logger.log_params(study.best_params)
            prefixed_metrics = {f"test_{k}": v for k, v in best_model_metrics.items()}
            self.logger.log_metrics(prefixed_metrics)

            signature = infer_signature(self.test_features, probabilities)
            self._save_model(self.best_model, signature)

            plots = PlotHelper.prepare_plots(self.test_labels, probabilities, predictions)
            for fig, name in plots:
                self.logger.log_figure(fig, name)

            param_importances = optuna.importance.get_param_importances(study)
            self.logger.log_param_importances(param_importances)

        except Exception as e:
            self.logger.log_text(str(e))

        finally:
            self.logger.end_run()

        return study.best_params

    def _objective(self, trial: optuna.Trial, log_nested: bool, metric: str) -> float:
        """
        Objective function for Optuna hyperparameter optimization.

        This function suggests hyperparameters, trains the model, evaluates it, and logs metrics using MLFlow.

        Parameters
        ----------
        trial : optuna.Trial
            The current Optuna trial object.
        log_nested : bool
            Whether to log nested runs for each trial.
        metric : str
            The main metric to optimize.

        Returns
        -------
        float
            The optimized value for the specified metric.
        """
        try:
            hyperparameters = self._suggest_hyperparameters(trial)
            model = self._train(hyperparameters)
            probabilities, predictions = self._evaluate(model, dataset='train')
            train_metrics = MetricsHelper.calculate_metrics(self.train_labels, probabilities, predictions)

            if self.additional_metrics:
                additional_train_metrics = self.additional_metrics(self.train_labels, probabilities, predictions)
                train_metrics.update(additional_train_metrics)

            trial.set_user_attr('best_model', model)
            if log_nested:
                self.logger.start_nested_run(trial.number)
                self.logger.log_params(hyperparameters)
                prefixed_metrics = {f"train_{k}": v for k, v in train_metrics.items()}
                self.logger.log_metrics(prefixed_metrics)
            return train_metrics[metric]
        
        except Exception as e:
            print(f"Trial {trial.number} failed: {str(e)}")
            self.logger.log_text(f"Trial {trial.number} failed: {str(e)}")
            return -float("inf")
    
        finally:
            if log_nested:
                self.logger.end_run()

    def train(self, experiment_name: str = 'Training', hyperparameters: Dict[str, Any] = {}, run_name: Optional[str] = None) -> Dict[str, float]:
        """
        Trains the model using the provided hyperparameters.

        This method runs model training with the specified hyperparameters, evaluates it on the test dataset, 
        and logs the results with MLFlow.

        Parameters
        ----------
        experiment_name : str, optional
            The name of the MLFlow experiment (default is 'Training').
        hyperparameters : Dict[str, Any], optional
            The hyperparameters for model training (default is an empty dictionary).
        run_name : Optional[str], optional
            The name of the training run (default is the class name).

        Returns
        -------
        Dict[str, float]
            A dictionary containing the evaluation metrics after training.
        """
        run_name = run_name if run_name is not None else f"{self.__class__.__name__}_training"
        self.logger = MLFlowLogger(run_name=run_name, experiment_name=experiment_name)
        self.logger.start_run()

        try:
            self.logger.log_params(hyperparameters)
            model = self._train(hyperparameters)

            probabilities, predictions = self._evaluate(model, dataset='test')
            test_metrics = MetricsHelper.calculate_metrics(self.test_labels, probabilities, predictions)

            if self.additional_metrics:
                additional_test_metrics = self.additional_metrics(self.test_labels, probabilities, predictions)
                test_metrics.update(additional_test_metrics)

            prefixed_metrics = {f"test_{k}": v for k, v in test_metrics.items()}
            self.logger.log_metrics(prefixed_metrics)

            plots = PlotHelper.prepare_plots(self.test_labels, probabilities, predictions)
            for fig, name in plots:
                self.logger.log_figure(fig, name)

            signature = infer_signature(self.test_features, probabilities)
            self._save_model(model, signature)

        finally:
            self.logger.end_run()

        return test_metrics

    @abstractmethod
    def _train(self, hyperparameters: Dict[str, Any]) -> Any:
        """
        Abstract method for training the model with the given hyperparameters.

        This method must be implemented by subclasses to define the training process.

        Parameters
        ----------
        hyperparameters : Dict[str, Any]
            A dictionary of hyperparameters for model training.

        Returns
        -------
        Any
            The trained model instance.
        """
        raise NotImplementedError(f"{self.__class__.__name__} must implement the _train method.")

    @abstractmethod
    def _evaluate(self, model: Any, dataset: str) -> Tuple[np.ndarray, np.ndarray]:
        """
        Abstract method for evaluating the model on the specified dataset.

        This method must be implemented by subclasses to define the evaluation process, including predicting 
        probabilities and class labels.

        Parameters
        ----------
        model : Any
            The trained model to evaluate.
        dataset : str
            The dataset to evaluate on ('train' or 'test').

        Returns
        -------
        Tuple[np.ndarray, np.ndarray]
            A tuple containing predicted probabilities and predicted class labels.
        """
        raise NotImplementedError(f"{self.__class__.__name__} must implement the _evaluate method.")

    @abstractmethod
    def _save_model(self, model: Any, signature: Any):
        """
        Abstract method for saving the trained model.

        This method must be implemented by subclasses to define how the model is saved, typically using MLFlow.

        Parameters
        ----------
        model : Any
            The trained model to save.
        signature : Any
            The input/output signature for logging the model in MLFlow.
        """
        warnings.warn(f"{self.__class__.__name__} does not implement the _save_model method.", UserWarning)

    @abstractmethod
    def _suggest_hyperparameters(self, trial: optuna.Trial) -> Dict[str, Union[int, float, str]]:
        """
        Abstract method to suggest hyperparameters for the Optuna trial.

        This method must be implemented by subclasses to suggest hyperparameters for tuning, such as batch size, 
        learning rate, etc.

        Parameters
        ----------
        trial : optuna.Trial
            The Optuna trial object for suggesting hyperparameters.

        Returns
        -------
        Dict[str, Union[int, float, str]]
            A dictionary of suggested hyperparameters.
        """
        raise NotImplementedError(f"{self.__class__.__name__} must implement the _suggest_hyperparameters method.")
