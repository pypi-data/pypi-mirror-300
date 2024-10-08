import tensorflow as tf
from typing import Dict, Union, Any
import numpy as np
import optuna

from ....base_classes.tensorflow.TensorflowTunable import TensorflowTunable


class TensorflowWideDeepNetworkTunable(TensorflowTunable):
    """
    A tunable TensorFlow model class implementing a Wide and Deep architecture.
    The Wide and Deep architecture combines a linear wide model and a deep neural network to capture both memorization
    and generalization. The model uses Optuna for hyperparameter tuning.

    Methods
    -------
    build_model(input_shape: tuple, hyperparameters: Dict[str, Any]) -> tf.keras.Model
        Builds the Wide and Deep network model based on the provided hyperparameters.

    _suggest_hyperparameters(trial: optuna.Trial) -> Dict[str, Union[int, float, str]]
        Suggests a set of hyperparameters for the Optuna trial.
    """

    def build_model(self, input_shape: tuple, hyperparameters: Dict[str, Any]) -> tf.keras.Model:
        """
        Builds the Wide and Deep network model based on the provided hyperparameters.

        The model consists of two parts:
        - A "wide" part that captures feature interactions via a linear model.
        - A "deep" part that captures feature representations via multiple dense layers.

        Parameters
        ----------
        input_shape : tuple
            The shape of the input data.
        hyperparameters : Dict[str, Any]
            Dictionary containing model hyperparameters:
                - 'n_layers' (int): Number of dense layers in the deep part of the model.
                - 'units' (int): Number of units in each dense layer of the deep part.
                - 'activation' (str): Activation function to use in the deep layers.
                - 'use_batch_normalization' (bool): Whether to apply batch normalization after each deep layer.
                - 'dropout_rate' (float): Dropout rate for regularization in the deep layers.
                - 'wide_units' (int): Number of units in the wide part of the model.

        Returns
        -------
        tf.keras.Model
            A TensorFlow model implementing the Wide and Deep architecture.
        """
        n_layers = hyperparameters.get('n_layers', 3)
        units = hyperparameters.get('units', 128)
        activation = hyperparameters.get('activation', 'relu')
        use_batch_normalization = hyperparameters.get(
            'use_batch_normalization', True)
        dropout_rate = hyperparameters.get('dropout_rate', 0.3)
        wide_units = hyperparameters.get('wide_units', 64)

        inputs = tf.keras.layers.Input(shape=input_shape)

        wide_output = tf.keras.layers.Dense(
            units=wide_units, activation='linear')(inputs)

        x = inputs
        for _ in range(n_layers):
            x = tf.keras.layers.Dense(units=units, activation=activation)(x)
            if use_batch_normalization:
                x = tf.keras.layers.BatchNormalization()(x)
            if dropout_rate > 0:
                x = tf.keras.layers.Dropout(dropout_rate)(x)
        deep_output = x

        combined_output = tf.keras.layers.concatenate(
            [wide_output, deep_output])

        output_units = 2 if len(np.unique(self.train_labels)) == 2 else len(
            np.unique(self.train_labels))
        final_output = tf.keras.layers.Dense(
            output_units, activation='softmax')(combined_output)

        model = tf.keras.Model(inputs=inputs, outputs=final_output)

        return model

    def _suggest_hyperparameters(self, trial: optuna.Trial) -> Dict[str, Union[int, float, str]]:
        """
        Suggests a set of hyperparameters for the Optuna trial.

        Parameters
        ----------
        trial : optuna.Trial
            The Optuna trial instance for hyperparameter optimization.

        Returns
        -------
        Dict[str, Union[int, float, str]]
            A dictionary of suggested hyperparameters, including:
                - 'n_layers' (int): Number of dense layers in the deep part of the model.
                - 'units' (int): Number of units in each dense layer.
                - 'activation' (str): Activation function for the dense layers.
                - 'use_batch_normalization' (bool): Whether to apply batch normalization in the deep part.
                - 'dropout_rate' (float): Dropout rate for regularization in the deep layers.
                - 'wide_units' (int): Number of units in the wide part of the model.
                - 'learning_rate' (float): Learning rate for the optimizer.
                - 'batch_size' (int): Batch size for training.
                - 'optimizer' (str): Optimizer for training the model.
        """
        return {
            'n_layers': trial.suggest_int('n_layers', 1, 5),
            'units': trial.suggest_int('units', 32, 512),
            'activation': trial.suggest_categorical('activation', ['relu', 'tanh', 'sigmoid', 'gelu']),
            'use_batch_normalization': trial.suggest_categorical('use_batch_normalization', [True, False]),
            'dropout_rate': trial.suggest_float('dropout_rate', 0.0, 0.5),
            'wide_units': trial.suggest_int('wide_units', 32, 512),
            'learning_rate': trial.suggest_float('learning_rate', 1e-5, 1e-2, log=True),
            'batch_size': trial.suggest_int('batch_size', 16, 256),
            'optimizer': trial.suggest_categorical('optimizer', ['Adam', 'RMSprop', 'SGD', 'Nadam']),
        }
