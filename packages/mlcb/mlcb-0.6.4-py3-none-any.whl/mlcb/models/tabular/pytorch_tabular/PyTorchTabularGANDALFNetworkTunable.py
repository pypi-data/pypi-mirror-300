import optuna
from typing import Dict, Union, Any
from pytorch_tabular.models import GANDALFConfig
from ....base_classes.pytorch.PytorchTabularTunable import PytorchTabularTunable

class PyTorchTabularGANDALFNetworkTunable(PytorchTabularTunable):
    """
    A tunable PyTorch Tabular model class implementing the GANDALF architecture.

    This model leverages Optuna for hyperparameter tuning to adjust various aspects of the 
    GANDALF architecture and training parameters for tabular data tasks.

    Methods
    -------
    build_model(hyperparameters: Dict[str, Any]) -> GANDALFConfig
        Builds the GANDALF model configuration based on the provided hyperparameters.

    _suggest_hyperparameters(trial: optuna.Trial) -> Dict[str, Union[int, float, str]]
        Suggests a set of hyperparameters for the Optuna trial.
    """

    def build_model(self, hyperparameters: Dict[str, Any]) -> GANDALFConfig:
        """
        Builds the GANDALF model configuration based on the provided hyperparameters.

        Parameters
        ----------
        hyperparameters : Dict[str, Any]
            A dictionary containing the model hyperparameters. Expected keys include:
                - 'learning_rate' (float): Learning rate for the optimizer.
                - 'gflu_stages' (int): Number of Gated Feature Learning Unit (GFLU) stages.
                - 'gflu_dropout' (float): Dropout rate applied within GFLU layers.
                - 'gflu_feature_init_sparsity' (float): Initial sparsity level for GFLU features.
                - 'learnable_sparsity' (bool): Whether sparsity should be learnable during training.

        Returns
        -------
        GANDALFConfig
            Configuration object for the GANDALF model based on the specified hyperparameters.
        """
        learning_rate: float = hyperparameters.get('learning_rate', 1e-3)
        gflu_stages: int = hyperparameters.get('gflu_stages', 5)
        gflu_dropout: float = hyperparameters.get('gflu_dropout', 0.2)
        gflu_feature_init_sparsity: float = hyperparameters.get('gflu_feature_init_sparsity', 0.3)
        learnable_sparsity: bool = hyperparameters.get('learnable_sparsity', True)

        model_config = GANDALFConfig(
            task="classification",
            learning_rate=learning_rate,
            gflu_stages=gflu_stages,
            gflu_dropout=gflu_dropout,
            gflu_feature_init_sparsity=gflu_feature_init_sparsity,
            learnable_sparsity=learnable_sparsity
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
            A dictionary of suggested hyperparameters for the GANDALF model, including:
                - 'batch_size' (int): Batch size for training.
                - 'optimizer' (str): Optimizer type (e.g., Adam, RMSprop, SGD).
                - 'learning_rate' (float): Learning rate for the optimizer.
                - 'gflu_stages' (int): Number of GFLU stages.
                - 'gflu_dropout' (float): Dropout rate within GFLU layers.
                - 'gflu_feature_init_sparsity' (float): Initial sparsity for GFLU feature.
                - 'learnable_sparsity' (bool): Whether sparsity is learnable during training.
        """
        return {
            'batch_size': trial.suggest_int('batch_size', 16, 128),
            'optimizer': trial.suggest_categorical('optimizer', ['Adam', 'RMSprop', 'SGD']),
            'learning_rate': trial.suggest_float('learning_rate', 1e-5, 1e-2, log=True),
            'gflu_stages': trial.suggest_int('gflu_stages', 3, 10),
            'gflu_dropout': trial.suggest_float('gflu_dropout', 0.0, 0.3),
            'gflu_feature_init_sparsity': trial.suggest_float('gflu_feature_init_sparsity', 0.1, 0.5),
            'learnable_sparsity': trial.suggest_categorical('learnable_sparsity', [True, False]),
        }
