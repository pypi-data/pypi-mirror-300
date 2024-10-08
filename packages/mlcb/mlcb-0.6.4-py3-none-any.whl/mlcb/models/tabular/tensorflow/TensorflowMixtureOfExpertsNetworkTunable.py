import tensorflow as tf
from typing import Dict, Union, Any
import numpy as np
import optuna

from ....base_classes.tensorflow.TensorflowTunable import TensorflowTunable

class TensorflowMixtureOfExpertsNetworkTunable(TensorflowTunable):
    """
    A tunable TensorFlow model class implementing a Mixture of Experts (MoE) architecture.
    
    This model uses Optuna for hyperparameter tuning and includes multiple expert networks and a gating mechanism 
    that determines which experts contribute to the final decision. It is well-suited for tasks that benefit 
    from having different sub-networks specializing in different parts of the input space.

    Methods
    -------
    build_model(input_shape: tuple, hyperparameters: Dict[str, Any]) -> tf.keras.Model
        Builds the Mixture of Experts model with the specified number of experts and layers.
    
    _suggest_hyperparameters(trial: optuna.Trial) -> Dict[str, Union[int, float, str]]
        Suggests a set of hyperparameters for the Optuna trial.
    """

    def build_model(self, input_shape: tuple, hyperparameters: Dict[str, Any]) -> tf.keras.Model:
        """
        Builds the Mixture of Experts model based on the provided hyperparameters.

        Parameters
        ----------
        input_shape : tuple
            The shape of the input data (without the batch size).
        hyperparameters : Dict[str, Any]
            Dictionary containing model hyperparameters:
                - 'n_layers' (int): Number of layers in each expert network.
                - 'units' (int): Number of units (neurons) in each layer of the expert networks.
                - 'activation' (str): Activation function used in the expert networks.
                - 'use_batch_normalization' (bool): Whether to apply batch normalization.
                - 'dropout_rate' (float): The dropout rate applied in the expert networks.
                - 'n_experts' (int): Number of expert networks in the mixture.

        Returns
        -------
        tf.keras.Model
            A TensorFlow model implementing the Mixture of Experts architecture.
        """
        n_layers = hyperparameters.get('n_layers', 3)
        units = hyperparameters.get('units', 64)
        activation = hyperparameters.get('activation', 'relu')
        use_batch_normalization = hyperparameters.get('use_batch_normalization', True)
        dropout_rate = hyperparameters.get('dropout_rate', 0.3)
        n_experts = hyperparameters.get('n_experts', 3)

        inputs = tf.keras.layers.Input(shape=input_shape)

        experts = []
        for _ in range(n_experts):
            expert = tf.keras.layers.Dense(units=units, activation=activation)(inputs)
            for _ in range(n_layers - 1):
                expert = tf.keras.layers.Dense(units=units, activation=activation)(expert)
                if use_batch_normalization:
                    expert = tf.keras.layers.BatchNormalization()(expert)
                if dropout_rate > 0:
                    expert = tf.keras.layers.Dropout(dropout_rate)(expert)
            experts.append(expert)

        gate_output = tf.keras.layers.Dense(units=n_experts, activation='softmax')(inputs)

        weighted_experts = tf.reduce_sum(
            [tf.expand_dims(gate_output[:, i], axis=-1) * experts[i] for i in range(n_experts)], axis=0
        )

        output_units = 2 if len(np.unique(self.train_labels)) == 2 else len(np.unique(self.train_labels))
        outputs = tf.keras.layers.Dense(output_units, activation='softmax')(weighted_experts)

        model = tf.keras.Model(inputs=inputs, outputs=outputs)

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
                - 'n_layers' (int): Number of layers in the expert networks.
                - 'units' (int): Number of units (neurons) in the expert layers.
                - 'activation' (str): Activation function for the expert networks.
                - 'use_batch_normalization' (bool): Whether to apply batch normalization.
                - 'dropout_rate' (float): The dropout rate applied in the expert layers.
                - 'n_experts' (int): Number of expert networks in the mixture.
                - 'learning_rate' (float): The learning rate for model training.
                - 'batch_size' (int): The batch size for training.
                - 'optimizer' (str): Optimizer to use for training the model.
        """
        return {
            'n_layers': trial.suggest_int('n_layers', 1, 5),
            'units': trial.suggest_int('units', 32, 512),
            'activation': trial.suggest_categorical('activation', ['relu', 'tanh', 'gelu']),
            'use_batch_normalization': trial.suggest_categorical('use_batch_normalization', [True, False]),
            'dropout_rate': trial.suggest_float('dropout_rate', 0.0, 0.5),
            'n_experts': trial.suggest_int('n_experts', 2, 10),
            'learning_rate': trial.suggest_float('learning_rate', 1e-5, 1e-2, log=True),
            'batch_size': trial.suggest_int('batch_size', 16, 256),
            'optimizer': trial.suggest_categorical('optimizer', ['Adam', 'RMSprop', 'SGD', 'Nadam']),
        }
