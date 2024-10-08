import optuna
from typing import Dict, Union, Any
from pytorch_tabular.models import CategoryEmbeddingModelConfig
from ....base_classes.pytorch.PytorchTabularTunable import PytorchTabularTunable

class PyTorchTabularCategoryEmbeddingNetworkTunable(PytorchTabularTunable):
    """
    A tunable PyTorch Tabular model class implementing a Category Embedding architecture.
    
    This model utilizes `CategoryEmbeddingModelConfig` from `pytorch_tabular` and incorporates Optuna 
    for hyperparameter tuning. The Category Embedding model is designed to handle categorical data 
    with configurable hidden layers, activations, and regularization techniques, such as dropout 
    and batch normalization.
    
    Methods
    -------
    build_model(hyperparameters: Dict[str, Any]) -> CategoryEmbeddingModelConfig
        Builds the Category Embedding model configuration based on the provided hyperparameters.
        
    _suggest_hyperparameters(trial: optuna.Trial) -> Dict[str, Union[int, float, str]]
        Suggests a set of hyperparameters for tuning using Optuna.
    """

    def build_model(self, hyperparameters: Dict[str, Any]) -> CategoryEmbeddingModelConfig:
        """
        Builds the Category Embedding model configuration based on the provided hyperparameters.

        Parameters
        ----------
        hyperparameters : Dict[str, Any]
            Dictionary containing model hyperparameters. The expected keys are:
                - 'layers' (str): Architecture of the hidden layers, e.g., '1024-512-512'.
                - 'activation' (str): Activation function for the hidden layers.
                - 'learning_rate' (float): Learning rate for the optimizer.
                - 'dropout' (float): Dropout rate for regularization.
                - 'use_batch_normalization' (bool): Whether to apply batch normalization.
                - 'initialization' (str): Weight initialization method, e.g., 'kaiming' or 'xavier'.

        Returns
        -------
        CategoryEmbeddingModelConfig
            The configuration object for the Category Embedding model, which defines its architecture 
            and various settings like layers, activation, and initialization.
        """
        layers: str = hyperparameters.get('layers', '1024-512-512')
        activation: str = hyperparameters.get('activation', 'ReLU')
        learning_rate: float = hyperparameters.get('learning_rate', 1e-3)
        dropout: float = hyperparameters.get('dropout', 0.1)
        use_batch_normalization: bool = hyperparameters.get('use_batch_normalization', True)
        initialization: str = hyperparameters.get('initialization', 'kaiming')

        model_config = CategoryEmbeddingModelConfig(
            task="classification",
            layers=layers,
            activation=activation,
            learning_rate=learning_rate,
            dropout=dropout,
            use_batch_norm=use_batch_normalization,
            initialization=initialization,
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
            A dictionary of suggested hyperparameters, including configurations such as layer structure, 
            activation functions, dropout rate, and learning rate. These hyperparameters will be tuned 
            by Optuna to find the optimal values.
        """
        return {
            'batch_size': trial.suggest_int('batch_size', 16, 128),
            'optimizer': trial.suggest_categorical('optimizer', ['Adam', 'RMSprop', 'SGD']),
            'layers': trial.suggest_categorical(
                'layers', 
                ['64-32', '128-64-32', '256-128-64-32', '512-256-128-64-32', '1024-512-256-128-64-32']
            ),
            'dropout': trial.suggest_float('dropout', 0.0, 0.5),
            'initialization': trial.suggest_categorical('initialization', ['kaiming', 'xavier', 'random']),
            'head': trial.suggest_categorical('head', [None, 'LinearHead', 'MixtureDensityHead']),
            'use_batch_normalization': trial.suggest_categorical('use_batch_normalization', [True, False]),
            'activation': trial.suggest_categorical('activation', ['ReLU', 'ELU', 'SELU', 'LeakyReLU']),
            'learning_rate': trial.suggest_float('learning_rate', 1e-5, 1e-2, log=True),
        }
