import tensorflow as tf
from typing import Dict, Union, Any
import numpy as np
import optuna

from ....base_classes.tensorflow.TensorflowTunable import TensorflowTunable


class TensorflowConvolutionalNetworkTunable(TensorflowTunable):
    """
    A tunable TensorFlow model class implementing a convolutional neural network (CNN).

    This model architecture uses 1D convolutions to extract temporal patterns from sequential data, 
    making it suitable for tasks like time series classification. The class leverages Optuna for 
    hyperparameter tuning to optimize layers, filters, kernel sizes, activations, and regularization methods.

    Methods
    -------
    __init__(X_train: np.ndarray, y_train: np.ndarray, X_test: np.ndarray, y_test: np.ndarray, max_epochs: int = 5000)
        Initializes the model by expanding the input data dimensions for 1D convolutions.

    build_model(input_shape: tuple, hyperparameters: Dict[str, Any]) -> tf.keras.Model
        Builds the CNN model based on the provided hyperparameters.

    _suggest_hyperparameters(trial: optuna.Trial) -> Dict[str, Union[int, float, str]]
        Suggests a set of hyperparameters for tuning using Optuna.
    """

    def __init__(self, X_train: np.ndarray, y_train: np.ndarray, X_test: np.ndarray, y_test: np.ndarray, max_epochs: int = 5000):
        """
        Initializes the TensorflowConvolutionalNetworkTunable class.

        Expands the dimensions of the input data to fit the 1D convolutional layers and sets up 
        the training and test datasets.

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
            The maximum number of training epochs, by default 5000.
        """
        X_train = np.expand_dims(X_train, axis=-1)
        X_test = np.expand_dims(X_test, axis=-1)
        super().__init__(X_train, y_train, X_test, y_test, max_epochs)

    def build_model(self, input_shape: tuple, hyperparameters: Dict[str, Any]) -> tf.keras.Model:
        """
        Builds the convolutional neural network model based on the provided hyperparameters.

        Parameters
        ----------
        input_shape : tuple
            The shape of the input data (without the batch size).
        hyperparameters : Dict[str, Any]
            Dictionary containing model hyperparameters:
                - 'n_layers' (int): Number of convolutional layers to include.
                - 'filters' (int): Number of filters in the convolutional layers.
                - 'kernel_size' (int): Size of the convolution kernels (window size).
                - 'activation' (str): Activation function for the convolutional layers.
                - 'use_batch_normalization' (bool): Whether to use batch normalization.
                - 'dropout_rate' (float): Dropout rate applied after each convolutional layer.

        Returns
        -------
        tf.keras.Model
            A TensorFlow convolutional neural network model.
        """
        n_layers = hyperparameters.get('n_layers', 3)
        filters = hyperparameters.get('filters', 64)
        kernel_size = hyperparameters.get('kernel_size', 3)
        activation = hyperparameters.get('activation', 'relu')
        use_batch_normalization = hyperparameters.get(
            'use_batch_normalization', True)
        dropout_rate = hyperparameters.get('dropout_rate', 0.3)

        model = tf.keras.Sequential()
        model.add(tf.keras.layers.InputLayer(shape=input_shape))

        for i in range(n_layers):
            model.add(tf.keras.layers.Conv1D(filters=filters * (i + 1),
                      kernel_size=kernel_size, activation=activation, padding='same'))
            if use_batch_normalization:
                model.add(tf.keras.layers.BatchNormalization())
            if dropout_rate > 0:
                model.add(tf.keras.layers.Dropout(dropout_rate))
            if model.output_shape[1] > 1:
                model.add(tf.keras.layers.MaxPooling1D(pool_size=2))
            else:
                break

        model.add(tf.keras.layers.GlobalMaxPooling1D())
        output_units = 2 if len(np.unique(self.train_labels)) == 2 else len(
            np.unique(self.train_labels))
        model.add(tf.keras.layers.Dense(output_units, activation='softmax'))

        return model

    def _suggest_hyperparameters(self, trial: optuna.Trial) -> Dict[str, Union[int, float, str]]:
        """
        Suggests a set of hyperparameters for the Optuna trial.

        This method proposes different configurations of layers, activations, and other parameters 
        for the CNN model to be evaluated during the hyperparameter tuning process.

        Parameters
        ----------
        trial : optuna.Trial
            The Optuna trial instance for hyperparameter optimization.

        Returns
        -------
        Dict[str, Union[int, float, str]]
            A dictionary of suggested hyperparameters including:
                - 'n_layers' (int): Number of convolutional layers.
                - 'filters' (int): Number of filters in each convolutional layer.
                - 'kernel_size' (int): Size of the kernel in the convolutional layers.
                - 'activation' (str): Activation function for the layers.
                - 'use_batch_normalization' (bool): Whether to use batch normalization.
                - 'dropout_rate' (float): Dropout rate for regularization.
                - 'optimizer' (str): Optimizer to use for training.
                - 'learning_rate' (float): Learning rate for the optimizer.
                - 'batch_size' (int): Batch size for training.
        """
        return {
            'n_layers': trial.suggest_int('n_layers', 1, 5),
            'filters': trial.suggest_int('filters', 16, 256),
            'kernel_size': trial.suggest_int('kernel_size', 2, 7),
            'activation': trial.suggest_categorical('activation', ['relu', 'tanh', 'sigmoid', 'elu']),
            'use_batch_normalization': trial.suggest_categorical('use_batch_normalization', [True, False]),
            'dropout_rate': trial.suggest_float('dropout_rate', 0.0, 0.5),
            'optimizer': trial.suggest_categorical('optimizer', ['Adam', 'RMSprop', 'SGD', 'Nadam']),
            'learning_rate': trial.suggest_float('learning_rate', 1e-5, 1e-2, log=True),
            'batch_size': trial.suggest_int('batch_size', 16, 256),
        }
