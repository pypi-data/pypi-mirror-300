from abc import ABC, abstractmethod
import mlflow
import optuna
import tensorflow as tf
from typing import Dict, Union, Any, Tuple
import numpy as np

from mlcb.base_classes.BaseTunableModel import BaseTunableModel

class TensorflowTunable(BaseTunableModel, ABC):
    """
    A tunable TensorFlow model that extends the BaseTunableModel.

    This class provides functionality for:
    - Training a TensorFlow model with tunable hyperparameters.
    - Using Optuna for hyperparameter tuning.
    - Saving and logging models with MLFlow for experiment tracking.

    Attributes
    ----------
    train_features : np.ndarray
        The feature set for the training dataset.
    train_labels : np.ndarray
        The labels for the training dataset.
    test_features : np.ndarray
        The feature set for the testing dataset.
    test_labels : np.ndarray
        The labels for the testing dataset.
    max_epochs : int
        The maximum number of epochs for training.
    """

    def __init__(self, 
                 train_features: np.ndarray, 
                 train_labels: np.ndarray, 
                 test_features: np.ndarray, 
                 test_labels: np.ndarray, 
                 max_epochs: int = 5000):
        """
        Initializes the TensorflowTunable class with the provided datasets and configurations.

        Parameters
        ----------
        train_features : np.ndarray
            The feature set for the training dataset.
        train_labels : np.ndarray
            The labels for the training dataset.
        test_features : np.ndarray
            The feature set for the testing dataset.
        test_labels : np.ndarray
            The labels for the testing dataset.
        max_epochs : int, optional
            The maximum number of training epochs (default is 5000).
        """
        super().__init__(train_features, train_labels, test_features, test_labels)
        self.max_epochs = max_epochs

    def _train(self, hyperparameters: Dict[str, Union[int, float, str]]) -> tf.keras.Model:
        """
        Trains a TensorFlow model with the provided hyperparameters.

        This method compiles the model, applies the early stopping callback, and fits the model on the training dataset.

        Parameters
        ----------
        hyperparameters : Dict[str, Union[int, float, str]]
            A dictionary of hyperparameters, including 'batch_size', 'learning_rate', and 'optimizer'.

        Returns
        -------
        tf.keras.Model
            The trained TensorFlow model.
        """
        input_shape = self.train_features.shape[1:]
        batch_size = hyperparameters.get('batch_size', 32)
        learning_rate = hyperparameters.get('learning_rate', 1e-3)
        optimizer = self._get_optimizer(hyperparameters.get('optimizer', 'Adam'), learning_rate)
        model = self.build_model(input_shape=input_shape, hyperparameters=hyperparameters)
        early_stopping = self._create_early_stopping_callback()

        model.compile(
            optimizer=optimizer,
            loss='sparse_categorical_crossentropy',
        )
        
        model.fit(
            self.train_features,
            self.train_labels,
            validation_split=0.2,
            epochs=self.max_epochs,
            batch_size=batch_size,
            callbacks=[early_stopping],
            verbose=0
        )

        return model

    def _evaluate(self, model: tf.keras.Model, dataset: str) -> Tuple[np.ndarray, np.ndarray]:
        """
        Evaluates the TensorFlow model on the specified dataset (train or test).

        This method predicts the probabilities and labels for the specified dataset.

        Parameters
        ----------
        model : tf.keras.Model
            The trained TensorFlow model.
        dataset : str
            The dataset to evaluate ('train' or 'test').

        Returns
        -------
        Tuple[np.ndarray, np.ndarray]
            A tuple containing predicted probabilities and predicted labels.
        """
        features = self.train_features if dataset == 'train' else self.test_features
        probabilities = model.predict(features)
        predictions = np.argmax(probabilities, axis=1)
        return probabilities, predictions

    def _save_model(self, model: tf.keras.Model, signature: Any) -> None:
        """
        Saves the trained TensorFlow model using MLFlow for experiment tracking.

        Parameters
        ----------
        model : tf.keras.Model
            The trained TensorFlow model to save.
        signature : Any
            The input/output signature for logging the model in MLFlow.
        """
        mlflow.tensorflow.log_model(model, "trained_best_model", signature=signature)

    @abstractmethod
    def _suggest_hyperparameters(self, trial: optuna.Trial) -> Dict[str, Union[int, float, str]]:
        """
        Abstract method to suggest hyperparameters for Optuna hyperparameter tuning.

        This method should be implemented by subclasses to suggest hyperparameters like batch size, learning rate, and optimizer.

        Parameters
        ----------
        trial : optuna.Trial
            The Optuna trial object used for suggesting hyperparameters.

        Returns
        -------
        Dict[str, Union[int, float, str]]
            A dictionary of suggested hyperparameters.
        """
        pass

    @abstractmethod
    def build_model(self, input_shape: Tuple[int, ...], hyperparameters: Dict[str, Any]) -> tf.keras.Model:
        """
        Abstract method to build a TensorFlow model based on the provided hyperparameters.

        This method should be implemented by subclasses to define the structure of the TensorFlow model.

        Parameters
        ----------
        input_shape : Tuple[int, ...]
            The shape of the input features.
        hyperparameters : Dict[str, Any]
            A dictionary of hyperparameters that define the model architecture and configuration.

        Returns
        -------
        tf.keras.Model
            The TensorFlow model.
        """
        pass

    def _create_early_stopping_callback(self) -> tf.keras.callbacks.EarlyStopping:
        """
        Creates an early stopping callback for TensorFlow training.

        This callback monitors the validation loss and stops training if it doesn't improve after a certain number of epochs.

        Returns
        -------
        tf.keras.callbacks.EarlyStopping
            The early stopping callback.
        """
        return tf.keras.callbacks.EarlyStopping(
            monitor='val_loss',
            patience=5,
            restore_best_weights=True
        )

    def _get_optimizer(self, optimizer_name: str, learning_rate: float) -> tf.keras.optimizers.Optimizer:
        """
        Retrieves the optimizer based on the provided name and learning rate.

        Parameters
        ----------
        optimizer_name : str
            The name of the optimizer ('adam', 'rmsprop', 'sgd', 'nadam').
        learning_rate : float
            The learning rate for the optimizer.

        Returns
        -------
        tf.keras.optimizers.Optimizer
            The corresponding TensorFlow optimizer.

        Raises
        -------
        ValueError
            If an unsupported optimizer is provided.
        """
        optimizers = {
            'adam': tf.keras.optimizers.Adam,
            'rmsprop': tf.keras.optimizers.RMSprop,
            'sgd': tf.keras.optimizers.SGD,
            'nadam': tf.keras.optimizers.Nadam
        }

        if optimizer_name.lower() in optimizers:
            return optimizers[optimizer_name.lower()](learning_rate)
        else:
            raise ValueError(f"Unsupported optimizer: {optimizer_name}")
