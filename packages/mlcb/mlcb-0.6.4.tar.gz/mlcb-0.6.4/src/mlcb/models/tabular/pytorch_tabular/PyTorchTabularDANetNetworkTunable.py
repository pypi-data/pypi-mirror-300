import optuna
from typing import Dict, Union, Any
from pytorch_tabular.models import DANetConfig
from ....base_classes.pytorch.PytorchTabularTunable import PytorchTabularTunable

class PyTorchTabularDANetNetworkTunable(PytorchTabularTunable):
    """
    A tunable PyTorch Tabular model class implementing the DANet architecture.

    This model leverages Optuna for hyperparameter tuning to automatically search for the best configuration
    for the DANet architecture, which is designed for tabular data classification tasks.

    Methods
    -------
    build_model(hyperparameters: Dict[str, Any]) -> DANetConfig
        Builds the DANet model configuration based on the provided hyperparameters.

    _suggest_hyperparameters(trial: optuna.Trial) -> Dict[str, Union[int, float, str]]
        Suggests a set of hyperparameters for tuning via Optuna.
    """

    def build_model(self, hyperparameters: Dict[str, Any]) -> DANetConfig:
        """
        Builds the DANet model configuration based on the provided hyperparameters.

        Parameters
        ----------
        hyperparameters : Dict[str, Any]
            A dictionary containing the model hyperparameters. Expected keys are:
                - 'n_layers' (int): Number of layers in the model.
                - 'abstlay_dim_1' (int): Dimension of the first abstraction layer.
                - 'abstlay_dim_2' (int): Dimension of the second abstraction layer.
                - 'k' (int): Value for the k parameter in DANet.
                - 'dropout_rate' (float): Dropout rate for regularization.
                - 'embedding_dropout' (float): Dropout rate for embedding layers.
                - 'batch_norm_continuous_input' (bool): Whether to apply batch normalization to continuous input features.
                - 'learning_rate' (float): Learning rate for the optimizer.

        Returns
        -------
        DANetConfig
            The configuration object for the DANet model based on the specified hyperparameters.
        """
        n_layers: int = hyperparameters.get('n_layers', 8)
        abstlay_dim_1: int = hyperparameters.get('abstlay_dim_1', 64)
        abstlay_dim_2: int = hyperparameters.get('abstlay_dim_2', 128)
        k: int = hyperparameters.get('k', 5)
        dropout_rate: float = hyperparameters.get('dropout_rate', 0.1)
        embedding_dropout: float = hyperparameters.get('embedding_dropout', 0.1)
        batch_norm_continuous_input: bool = hyperparameters.get('batch_norm_continuous_input', True)
        learning_rate: float = hyperparameters.get('learning_rate', 1e-3)

        model_config = DANetConfig(
            task="classification",
            n_layers=n_layers,
            abstlay_dim_1=abstlay_dim_1,
            abstlay_dim_2=abstlay_dim_2,
            k=k,
            dropout_rate=dropout_rate,
            embedding_dropout=embedding_dropout,
            batch_norm_continuous_input=batch_norm_continuous_input,
            learning_rate=learning_rate
        )

        return model_config

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
            A dictionary of suggested hyperparameters for the model,
            including values for model layers, dimensions, dropout rates, and learning rate.
        """
        return {
            'batch_size': trial.suggest_int('batch_size', 16, 128),
            'optimizer': trial.suggest_categorical('optimizer', ['Adam', 'RMSprop', 'SGD']),
            'n_layers': trial.suggest_categorical('n_layers', [8, 16, 32]),
            'abstlay_dim_1': trial.suggest_int('abstlay_dim_1', 16, 128),
            'abstlay_dim_2': trial.suggest_int('abstlay_dim_2', 32, 256),
            'k': trial.suggest_int('k', 1, 10),
            'dropout_rate': trial.suggest_float('dropout_rate', 0.0, 0.5),
            'embedding_dropout': trial.suggest_float('embedding_dropout', 0.0, 0.5),
            'batch_norm_continuous_input': trial.suggest_categorical('batch_norm_continuous_input', [True, False]),
            'learning_rate': trial.suggest_float('learning_rate', 1e-5, 1e-2, log=True),
        }
