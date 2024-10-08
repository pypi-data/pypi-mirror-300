import tensorflow as tf
from typing import Dict, Union, Any
import numpy as np
import optuna
from ....base_classes.tensorflow.TensorflowTunable import TensorflowTunable


class TensorflowAttentionNetworkTunable(TensorflowTunable):
    """
    A tunable TensorFlow model class implementing an attention-based dense neural network.

    This model architecture includes customizable dense layers combined with an attention 
    mechanism to improve feature representation and is suitable for classification tasks 
    (binary or multi-class). The class leverages Optuna for hyperparameter tuning.

    Methods
    -------
    build_model(input_shape: tuple, hyperparameters: Dict[str, Any]) -> tf.keras.Model
        Builds the attention-based dense neural network model with the provided hyperparameters.

    _suggest_hyperparameters(trial: optuna.Trial) -> Dict[str, Union[int, float, str]]
        Suggests a set of hyperparameters for the Optuna trial, such as the number of units, 
        layers, and learning rate.
    """

    def build_model(self, input_shape: tuple, hyperparameters: Dict[str, Any]) -> tf.keras.Model:
        """
        Builds the attention-based dense neural network model using the specified hyperparameters.

        Parameters
        ----------
        input_shape : tuple
            The shape of the input data, which must be compatible with the model architecture.
        hyperparameters : Dict[str, Any]
            Dictionary containing model hyperparameters, including:
                - 'units' (int): Number of units in each dense layer.
                - 'activation' (str): Activation function for the dense layers.
                - 'use_batch_normalization' (bool): Whether to apply batch normalization after each dense layer.
                - 'dropout_rate' (float): Dropout rate for regularization.
                - 'attention_units' (int): Number of units in the attention layer.
                - 'attention_activation' (str): Activation function for the attention layer.
                - 'n_layers' (int): Number of dense layers in the model.

        Returns
        -------
        tf.keras.Model
            A TensorFlow model with attention mechanisms and dense layers.
        """

        def attention_layer(x, attention_units: int, attention_activation: str) -> tf.Tensor:
            """
            Adds an attention mechanism to dynamically weigh input features.

            Parameters
            ----------
            x : tf.Tensor
                Input tensor to apply attention to.
            attention_units : int
                Number of units in the attention layer.
            attention_activation : str
                Activation function to use in the attention layer.

            Returns
            -------
            tf.Tensor
                Output tensor after applying attention to the input features.
            """
            attention_scores = tf.keras.layers.Dense(
                attention_units, activation=attention_activation)(x)
            attention_scores = tf.keras.layers.Dense(
                1, activation='sigmoid')(attention_scores)
            attention_weights = tf.keras.layers.RepeatVector(
                x.shape[-1])(attention_scores)
            attention_weights = tf.keras.layers.Permute(
                [2, 1])(attention_weights)
            attended_output = tf.keras.layers.multiply([x, attention_weights])
            return attended_output

        units = hyperparameters.get('units', 64)
        activation = hyperparameters.get('activation', 'relu')
        use_batch_normalization = hyperparameters.get(
            'use_batch_normalization', True)
        dropout_rate = hyperparameters.get('dropout_rate', 0.3)
        attention_units = hyperparameters.get('attention_units', 64)
        attention_activation = hyperparameters.get(
            'attention_activation', 'relu')
        n_layers = hyperparameters.get('n_layers', 3)

        inputs = tf.keras.layers.Input(shape=input_shape)
        x = tf.keras.layers.Dense(units=units, activation=activation)(inputs)
        if use_batch_normalization:
            x = tf.keras.layers.BatchNormalization()(x)
        if dropout_rate > 0:
            x = tf.keras.layers.Dropout(dropout_rate)(x)

        x = attention_layer(x, attention_units, attention_activation)

        for _ in range(n_layers - 1):
            x = tf.keras.layers.Dense(units=units, activation=activation)(x)
            if use_batch_normalization:
                x = tf.keras.layers.BatchNormalization()(x)
            if dropout_rate > 0:
                x = tf.keras.layers.Dropout(dropout_rate)(x)

        x = tf.keras.layers.GlobalAveragePooling1D()(x)
        output_units = 2 if len(np.unique(self.train_labels)) == 2 else len(
            np.unique(self.train_labels))
        outputs = tf.keras.layers.Dense(output_units, activation='softmax')(x)

        model = tf.keras.Model(inputs=inputs, outputs=outputs)
        return model

    def _suggest_hyperparameters(self, trial: optuna.Trial) -> Dict[str, Union[int, float, str]]:
        """
        Suggests a set of hyperparameters for the Optuna trial to explore different configurations 
        of the attention-based dense neural network.

        Parameters
        ----------
        trial : optuna.Trial
            The Optuna trial instance for hyperparameter optimization.

        Returns
        -------
        Dict[str, Union[int, float, str]]
            A dictionary of suggested hyperparameters, including:
                - 'n_layers' (int): Number of layers in the model.
                - 'units' (int): Number of units per dense layer.
                - 'activation' (str): Activation function for the dense layers.
                - 'use_batch_normalization' (bool): Whether to apply batch normalization.
                - 'dropout_rate' (float): Dropout rate for regularization.
                - 'attention_units' (int): Number of units in the attention layer.
                - 'attention_activation' (str): Activation function for the attention layer.
                - 'learning_rate' (float): Learning rate for the optimizer.
                - 'batch_size' (int): Batch size for training.
                - 'optimizer' (str): Optimizer for training (e.g., Adam, RMSprop).
        """
        return {
            'n_layers': trial.suggest_int('n_layers', 1, 5),
            'units': trial.suggest_int('units', 32, 512),
            'activation': trial.suggest_categorical('activation', ['relu', 'tanh', 'gelu', 'elu']),
            'use_batch_normalization': trial.suggest_categorical('use_batch_normalization', [True, False]),
            'dropout_rate': trial.suggest_float('dropout_rate', 0.0, 0.5),
            'attention_units': trial.suggest_int('attention_units', 16, 256),
            'attention_activation': trial.suggest_categorical('attention_activation', ['relu', 'tanh', 'sigmoid', 'softmax']),
            'learning_rate': trial.suggest_float('learning_rate', 1e-5, 1e-2, log=True),
            'batch_size': trial.suggest_int('batch_size', 16, 256),
            'optimizer': trial.suggest_categorical('optimizer', ['Adam', 'RMSprop', 'SGD', 'Nadam']),
        }
