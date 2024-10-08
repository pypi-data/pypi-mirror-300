from abc import ABC, abstractmethod
import mlflow
from sklearn.pipeline import Pipeline
from typing import Dict, Tuple, Union, Any
import numpy as np
import optuna

from ..BaseTunableModel import BaseTunableModel

class SklearnTunable(BaseTunableModel, ABC):
    """
    A tunable model for scikit-learn that extends the BaseTunableModel class.

    This class provides functionality for:
    - Training a scikit-learn model with tunable hyperparameters.
    - Using Optuna for hyperparameter tuning.
    - Saving and logging models with MLFlow for experiment tracking.

    Attributes
    ----------
    train_features : np.ndarray
        The feature set for the training data.
    train_labels : np.ndarray
        The labels corresponding to the training data.
    test_features : np.ndarray
        The feature set for the testing data.
    test_labels : np.ndarray
        The labels corresponding to the testing data.
    """

    def _train(self, hyperparameters: Dict[str, Union[int, float, str]]) -> Pipeline:
        """
        Trains a scikit-learn model using the provided hyperparameters.

        This method builds the scikit-learn model, fits it on the training dataset, and returns the trained model pipeline.

        Parameters
        ----------
        hyperparameters : Dict[str, Union[int, float, str]]
            A dictionary of hyperparameters for building and training the model.

        Returns
        -------
        Pipeline
            The trained scikit-learn model pipeline.
        """
        model = self.build_model(hyperparameters)
        model.fit(self.train_features, self.train_labels)
        return model

    def _evaluate(self, model: Pipeline, dataset: str) -> Tuple[np.ndarray, np.ndarray]:
        """
        Evaluates the trained scikit-learn model on the specified dataset (train or test) and returns the predicted probabilities 
        (if available) and predicted labels.

        Parameters
        ----------
        model : Pipeline
            The trained scikit-learn model pipeline to evaluate.
        dataset : str
            The dataset to evaluate on ('train' or 'test').

        Returns
        -------
        Tuple[np.ndarray, np.ndarray]
            A tuple containing:
            - probabilities: Predicted probabilities (or None if `predict_proba` is not available).
            - predictions: Predicted class labels.
        """
        if dataset == 'train':
            features = self.train_features
        else:
            features = self.test_features

        if hasattr(model, "predict_proba"):
            probabilities = model.predict_proba(features)
            predictions = np.argmax(probabilities, axis=1)
        else:
            predictions = model.predict(features)
            probabilities = None
        return probabilities, predictions

    def _save_model(self, model: Pipeline, signature: Any) -> None:
        """
        Saves the trained scikit-learn model using MLFlow for experiment tracking and model saving.

        Parameters
        ----------
        model : Pipeline
            The trained scikit-learn model pipeline to save.
        signature : Any
            The input/output signature for logging the model in MLFlow.
        """
        mlflow.sklearn.log_model(model, "trained_best_model", signature=signature)

    @abstractmethod
    def _suggest_hyperparameters(self, trial: optuna.Trial) -> Dict[str, Union[int, float, str]]:
        """
        Abstract method to suggest hyperparameters for Optuna hyperparameter tuning.

        This method should be implemented by subclasses to suggest hyperparameters specific to the scikit-learn model being optimized.

        Parameters
        ----------
        trial : optuna.Trial
            The Optuna trial object used to suggest hyperparameters.

        Returns
        -------
        Dict[str, Union[int, float, str]]
            A dictionary of suggested hyperparameters for model training.
        """
        pass

    @abstractmethod
    def build_model(self, hyperparameters: Dict[str, Any]) -> Pipeline:
        """
        Abstract method to build a scikit-learn model pipeline according to the provided hyperparameters.

        This method should be implemented by subclasses to define the model pipeline structure and configurations.

        Parameters
        ----------
        hyperparameters : Dict[str, Any]
            A dictionary of hyperparameters for building the model pipeline.

        Returns
        -------
        Pipeline
            The constructed scikit-learn model pipeline.
        """
        pass
