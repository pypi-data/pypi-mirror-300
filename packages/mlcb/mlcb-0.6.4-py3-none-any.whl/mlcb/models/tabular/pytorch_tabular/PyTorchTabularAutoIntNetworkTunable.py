import optuna
from typing import Dict, Union, Any
from pytorch_tabular.models import AutoIntConfig
from ....base_classes.pytorch.PytorchTabularTunable import PytorchTabularTunable


class PyTorchTabularAutoIntNetworkTunable(PytorchTabularTunable):
    """
    A tunable PyTorch Tabular model class implementing the AutoInt architecture.

    This model leverages the AutoIntConfig from `pytorch_tabular`, allowing flexible architecture 
    tuning via Optuna. The AutoInt architecture is designed for tabular data with attention 
    mechanisms, and this class enables automated hyperparameter optimization for classifications.

    Methods
    -------
    build_model(hyperparameters: Dict[str, Any]) -> AutoIntConfig
        Builds the AutoInt model configuration based on the provided hyperparameters.

    _suggest_hyperparameters(trial: optuna.Trial) -> Dict[str, Union[int, float, str]]
        Suggests a set of hyperparameters for tuning using Optuna.
    """

    def build_model(self, hyperparameters: Dict[str, Any]) -> AutoIntConfig:
        """
        Builds the AutoInt model configuration based on the provided hyperparameters.

        Parameters
        ----------
        hyperparameters : Dict[str, Any]
            Dictionary containing model hyperparameters.
            Expected keys:
                - 'num_attn_blocks' (int): Number of attention blocks in the AutoInt model.
                - 'embedding_initialization' (str): Initialization method for embeddings.
                - 'share_embedding' (bool): Whether to share embedding weights across features.
                - 'layers' (str): Structure of the hidden layers (e.g., '128-64' for two layers).
                - 'activation' (str): Activation function for hidden layers (e.g., 'ReLU').
                - 'dropout' (float): Dropout rate for regularization.
                - 'learning_rate' (float): Learning rate for the optimizer.

        Returns
        -------
        AutoIntConfig
            The configuration object for the AutoInt model, which defines its architecture and settings.
        """
        num_attn_blocks: int = hyperparameters.get('num_attn_blocks', 4)
        embedding_initialization: str = hyperparameters.get(
            'embedding_initialization', 'kaiming_uniform')
        share_embedding: bool = hyperparameters.get('share_embedding', False)
        layers: str = hyperparameters.get('layers', '128-64')
        activation: str = hyperparameters.get('activation', 'ReLU')
        dropout: float = hyperparameters.get('dropout', 0.3)
        learning_rate: float = hyperparameters.get('learning_rate', 1e-3)

        model_config = AutoIntConfig(
            task="classification",
            num_attn_blocks=num_attn_blocks,
            embedding_initialization=embedding_initialization,
            share_embedding=share_embedding,
            layers=layers,
            activation=activation,
            dropout=dropout,
            learning_rate=learning_rate,
        )
        return model_config

    def _suggest_hyperparameters(self, trial: optuna.Trial) -> Dict[str, Union[int, float, str]]:
        """
        Suggests a set of hyperparameters for the Optuna trial.

        Parameters
        ----------
        trial : optuna.Trial
            The Optuna trial instance used for hyperparameter optimization.

        Returns
        -------
        Dict[str, Union[int, float, str]]
            A dictionary of suggested hyperparameters. Each key corresponds to a model component or setting, 
            and each value is suggested based on the range defined for Optuna.
        """
        return {
            'batch_size': trial.suggest_int('batch_size', 32, 128),
            'optimizer': trial.suggest_categorical('optimizer', ['Adam', 'RMSprop', 'SGD']),
            'num_attn_blocks': trial.suggest_int('num_attn_blocks', 2, 8),
            'embedding_initialization': trial.suggest_categorical('embedding_initialization', ['kaiming_uniform', 'kaiming_normal']),
            'share_embedding': trial.suggest_categorical('share_embedding', [True, False]),
            'layers': trial.suggest_categorical('layers', ['64-32', '128-64', '256-128-64', '512-256-128-64']),
            'activation': trial.suggest_categorical('activation', ['ReLU', 'LeakyReLU', 'ELU']),
            'dropout': trial.suggest_float('dropout', 0.1, 0.5),
            'learning_rate': trial.suggest_float('learning_rate', 1e-5, 1e-2, log=True),
        }
