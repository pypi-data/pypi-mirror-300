import tensorflow as tf
from typing import Dict, Union, Any
import numpy as np
import optuna

from ....base_classes.tensorflow.TensorflowTunable import TensorflowTunable


class TensorflowRecurrentNetworkTunable(TensorflowTunable):
    """
    A tunable TensorFlow model class implementing a recurrent neural network (RNN) architecture
    with options for LSTM, GRU, and SimpleRNN layers. The model uses Optuna for hyperparameter tuning.

    This architecture is designed for sequence data..

    Methods
    -------
    build_model(input_shape: tuple, hyperparameters: Dict[str, Any]) -> tf.keras.Model
        Builds the recurrent neural network based on the provided hyperparameters.

    _suggest_hyperparameters(trial: optuna.Trial) -> Dict[str, Union[int, float, str]]
        Suggests a set of hyperparameters for the Optuna trial.
    """

    def __init__(self, X_train: np.ndarray, y_train: np.ndarray, X_test: np.ndarray, y_test: np.ndarray, max_epochs: int = 5000):
        """
        Initializes the TensorflowRecurrentNetworkTunable class by expanding the dimensions of the input data
        and setting up the train and test datasets.

        Parameters
        ----------
        X_train : np.ndarray
            The training input data.
        y_train : np.ndarray
            The training labels.
        X_test : np.ndarray
            The test input data.
        y_test : np.ndarray
            The test labels.
        max_epochs : int, optional
            The maximum number of training epochs (default is 5000).
        """
        X_train = np.expand_dims(X_train, axis=-1)
        X_test = np.expand_dims(X_test, axis=-1)
        super().__init__(X_train, y_train, X_test, y_test, max_epochs)

    def build_model(self, input_shape: tuple, hyperparameters: Dict[str, Any]) -> tf.keras.Model:
        """
        Builds the recurrent neural network model based on the provided hyperparameters.

        Parameters
        ----------
        input_shape : tuple
            The shape of the input data (excluding batch size).
        hyperparameters : Dict[str, Any]
            Dictionary containing model hyperparameters:
                - 'n_layers' (int): Number of RNN layers in the model.
                - 'units' (int): Number of units (neurons) in each RNN layer.
                - 'activation' (str): Activation function to use in RNN layers.
                - 'use_batch_normalization' (bool): Whether to apply batch normalization in the layers.
                - 'dropout_rate' (float): The dropout rate for regularization.
                - 'rnn_type' (str): The type of RNN layer to use ('SimpleRNN', 'LSTM', 'GRU').

        Returns
        -------
        tf.keras.Model
            A TensorFlow recurrent neural network model.
        """
        n_layers = hyperparameters.get('n_layers', 2)
        units = hyperparameters.get('units', 128)
        activation = hyperparameters.get('activation', 'tanh')
        use_batch_normalization = hyperparameters.get(
            'use_batch_normalization', True)
        dropout_rate = hyperparameters.get('dropout_rate', 0.3)
        rnn_type = hyperparameters.get('rnn_type', 'LSTM')

        model = tf.keras.Sequential()
        model.add(tf.keras.layers.InputLayer(shape=input_shape))

        for _ in range(n_layers):
            if rnn_type == 'LSTM':
                rnn_layer = tf.keras.layers.LSTM(
                    units=units, activation=activation, return_sequences=True)
            elif rnn_type == 'GRU':
                rnn_layer = tf.keras.layers.GRU(
                    units=units, activation=activation, return_sequences=True)
            else:
                rnn_layer = tf.keras.layers.SimpleRNN(
                    units=units, activation=activation, return_sequences=True)

            model.add(rnn_layer)

            if use_batch_normalization:
                model.add(tf.keras.layers.BatchNormalization())
            if dropout_rate > 0:
                model.add(tf.keras.layers.Dropout(dropout_rate))

        if rnn_type == 'LSTM':
            model.add(tf.keras.layers.LSTM(
                units=units, activation=activation, return_sequences=False))
        elif rnn_type == 'GRU':
            model.add(tf.keras.layers.GRU(
                units=units, activation=activation, return_sequences=False))
        else:
            model.add(tf.keras.layers.SimpleRNN(
                units=units, activation=activation, return_sequences=False))

        model.add(tf.keras.layers.Dense(units=units, activation=activation))
        model.add(tf.keras.layers.Dropout(dropout_rate))

        output_units = 2 if len(np.unique(self.train_labels)) == 2 else len(
            np.unique(self.train_labels))
        model.add(tf.keras.layers.Dense(output_units, activation='softmax'))

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
            A dictionary of suggested hyperparameters including:
                - 'n_layers' (int): Number of RNN layers in the model.
                - 'units' (int): Number of units (neurons) in each RNN layer.
                - 'activation' (str): Activation function for the RNN layers.
                - 'use_batch_normalization' (bool): Whether to apply batch normalization.
                - 'dropout_rate' (float): Dropout rate for regularization.
                - 'rnn_type' (str): Type of RNN layer to use ('SimpleRNN', 'LSTM', 'GRU').
                - 'learning_rate' (float): Learning rate for the optimizer.
                - 'batch_size' (int): Batch size for training the model.
                - 'optimizer' (str): Optimizer to use for model training.
        """
        return {
            'n_layers': trial.suggest_int('n_layers', 1, 4),
            'units': trial.suggest_int('units', 32, 512),
            'activation': trial.suggest_categorical('activation', ['relu', 'tanh', 'sigmoid']),
            'use_batch_normalization': trial.suggest_categorical('use_batch_normalization', [True, False]),
            'dropout_rate': trial.suggest_float('dropout_rate', 0.0, 0.5),
            'rnn_type': trial.suggest_categorical('rnn_type', ['SimpleRNN', 'LSTM', 'GRU']),
            'learning_rate': trial.suggest_float('learning_rate', 1e-5, 1e-2, log=True),
            'batch_size': trial.suggest_int('batch_size', 16, 256),
            'optimizer': trial.suggest_categorical('optimizer', ['Adam', 'RMSprop', 'SGD', 'Nadam']),
        }
