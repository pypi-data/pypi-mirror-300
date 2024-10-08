from abc import ABC, abstractmethod
from typing import Tuple, Union, Dict, Any
import mlflow
import numpy as np
import optuna
import pandas as pd
from pytorch_tabular import TabularModel
from pytorch_tabular.config import (
    DataConfig,
    OptimizerConfig,
    TrainerConfig,
)
import torch.nn as nn

from ..BaseTunableModel import BaseTunableModel

class PytorchTabularTunable(BaseTunableModel, ABC):
    """
    A tunable PyTorch Tabular model that extends the BaseTunableModel and incorporates abstract base class functionality.

    This class provides functionality for:
    - Training a PyTorch Tabular model with tunable hyperparameters using the PyTorch Tabular library.
    - Using Optuna for hyperparameter tuning.
    - Saving and logging models with MLFlow for experiment tracking.

    Attributes
    ----------
    tabular_model : TabularModel
        The PyTorch Tabular model used for training and evaluation.
    max_epochs : int
        Maximum number of epochs for training. Defaults to 5000.
    train_df : pd.DataFrame
        The training dataset containing features and the target.
    test_df : pd.DataFrame
        The testing dataset containing features and the target.
    """

    def __init__(self, train_features, train_labels, test_features, test_labels, max_epochs: int = 5000):
        """
        Initializes the PytorchTabularTunable class with the provided training and testing datasets and configurations.

        Parameters
        ----------
        train_features : np.ndarray
            The feature set for training.
        train_labels : np.ndarray
            The target labels for the training set.
        test_features : np.ndarray
            The feature set for testing.
        test_labels : np.ndarray
            The target labels for the testing set.
        max_epochs : int, optional
            The maximum number of training epochs (default is 5000).
        """
        super().__init__(train_features, train_labels, test_features, test_labels)
        self.tabular_model = None
        self.max_epochs = max_epochs
        self.train_df = pd.DataFrame(self.train_features, columns=[f'feature_{i}' for i in range(self.train_features.shape[1])]).astype(float)
        test_df = pd.DataFrame(self.test_features, columns=[f'feature_{i}' for i in range(self.test_features.shape[1])]).astype(float)
        self.train_df['target'] = self.train_labels.astype(float)
        self.test_df = test_df.assign(target=self.test_labels.astype(float))

    def _train(self, hyperparameters: Dict[str, Any]) -> TabularModel:
        """
        Trains the PyTorch Tabular model using the provided hyperparameters.

        This method builds the model configuration, sets up the optimizer, data configuration, 
        and trainer configuration, and trains the model on the provided training dataset.

        Parameters
        ----------
        hyperparameters : Dict[str, Any]
            A dictionary of hyperparameters, such as batch size, optimizer type, etc., for model training.

        Returns
        -------
        TabularModel
            The trained PyTorch Tabular model.
        """
        batch_size = hyperparameters.get('batch_size', 32)
        optimizer = hyperparameters.get('optimizer', 'Adam')

        data_config = DataConfig(
            target=['target'],
            continuous_cols=self.train_df.select_dtypes(include=['float64', 'int64']).columns.tolist(),
            categorical_cols=self.train_df.select_dtypes(include=['object', 'category']).columns.tolist(),
            validation_split=0.2,
        )

        trainer_config = TrainerConfig(
            batch_size=batch_size,
            max_epochs=self.max_epochs,
            early_stopping_patience=5,
            early_stopping_min_delta=0.001
        )

        optimizer_config = OptimizerConfig(optimizer)

        model_config = self.build_model(hyperparameters=hyperparameters)
        
        self.tabular_model = TabularModel(
            data_config=data_config,
            model_config=model_config,
            optimizer_config=optimizer_config,
            trainer_config=trainer_config,
            suppress_lightning_logger=True,
            verbose=False
        )
        self.tabular_model.fit(train=self.train_df, validation=self.test_df)
        return self.tabular_model

    def _evaluate(self, model: TabularModel, dataset: str) -> Tuple[np.ndarray, np.ndarray]:
        """
        Evaluates the given model on the specified dataset and returns predicted probabilities and predicted classes.

        The evaluation can be performed on the training or testing dataset, as specified by the `dataset` argument.

        Parameters
        ----------
        model : TabularModel
            The trained PyTorch Tabular model to evaluate.
        dataset : str
            A string indicating which dataset to evaluate on ('train' or 'test').

        Returns
        -------
        Tuple[np.ndarray, np.ndarray]
            A tuple containing the predicted probabilities and predicted class labels.
        """
        data_df = self.train_df if dataset == 'train' else self.test_df
        predictions_df = model.predict(data_df)
        probabilities = predictions_df.drop('prediction', axis=1).values
        predictions = np.argmax(probabilities, axis=1)
        return probabilities, predictions

    def _save_model(self, model, signature):
        """
        Saves the trained PyTorch Tabular model using MLFlow.

        Parameters
        ----------
        model : TabularModel
            The trained PyTorch Tabular model.
        signature : Any
            The input/output signature for logging the model in MLFlow.
        """
        mlflow.pytorch.log_model(model.model, "trained_best_model", signature=signature)

    @abstractmethod
    def _suggest_hyperparameters(self, trial: optuna.Trial) -> Dict[str, Union[int, float, str]]:
        """
        Abstract method to suggest hyperparameters for Optuna hyperparameter tuning.

        This method should be implemented by subclasses to provide suggestions for hyperparameters such as batch size, 
        learning rate, optimizer type, etc., to optimize the model performance during tuning.

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
    def build_model(self, hyperparameters: Dict[str, Any]) -> nn.Module:
        """
        Abstract method to build a PyTorch Tabular model based on the provided hyperparameters.

        This method should be implemented by subclasses to define the structure and configuration of the PyTorch Tabular model.

        Parameters
        ----------
        hyperparameters : Dict[str, Any]
            A dictionary containing hyperparameters that define the model's architecture and configuration.

        Returns
        -------
        nn.Module
            The PyTorch Tabular model configured according to the provided hyperparameters.
        """
        pass
