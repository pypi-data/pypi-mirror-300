from abc import ABC, abstractmethod
import mlflow
import torch
import torch.nn as nn
import torch.optim as optim
import torch_geometric
from torch_geometric.loader import DataLoader
import optuna
import numpy as np
from typing import Dict, Tuple, Union, Any
from ..BaseTunableModel import BaseTunableModel
from .EarlyStopping import EarlyStopping

class PyTorchGeometricTunable(BaseTunableModel, ABC):
    """
    A tunable PyTorch Geometric model that extends the BaseTunableModel.

    This class integrates PyTorch Geometric for graph-based machine learning, Optuna for hyperparameter tuning, 
    and MLFlow for experiment tracking and model saving. It supports training, evaluating, and saving models with 
    tunable hyperparameters.

    Attributes
    ----------
    train_data : torch_geometric.data.Dataset
        The PyTorch Geometric dataset for training.
    test_data : torch_geometric.data.Dataset
        The PyTorch Geometric dataset for testing.
    max_epochs : int
        Maximum number of epochs for training. Defaults to 5000. Early stopping is implemented to prevent unnecessary long training.
    device : torch.device
        The device (CPU or GPU) to run the model on.
    num_node_features : int
        The number of features for each node in the graph.
    train_loader : torch_geometric.loader.DataLoader
        The data loader for the training dataset.
    test_loader : torch_geometric.loader.DataLoader
        The data loader for the test dataset.
    """

    def __init__(self, 
                 train_data: torch_geometric.data.Dataset, 
                 test_data: torch_geometric.data.Dataset,
                 train_labels,
                 test_labels,
                 num_node_features: int,
                 max_epochs: int = 5000,
                 use_gpu: bool = True):
        """
        Initializes the PyTorchGeometricTunable class with provided datasets, labels, and configuration.

        Parameters
        ----------
        train_data : torch_geometric.data.Dataset
            The dataset for training, in PyTorch Geometric format.
        test_data : torch_geometric.data.Dataset
            The dataset for testing, in PyTorch Geometric format.
        train_labels : array-like
            The labels corresponding to the training dataset.
        test_labels : array-like
            The labels corresponding to the testing dataset.
        num_node_features : int
            The number of features for each node in the dataset.
        max_epochs : int, optional
            The maximum number of epochs to run during training (default is 5000).
        use_gpu : bool, optional
            Flag to indicate if GPU should be used for training (default is True).
        """
        self.train_data = train_data
        self.test_data = test_data
        self.max_epochs = max_epochs
        self.num_node_features = num_node_features if num_node_features is not None else self.train_data.num_node_features
        self.device = torch.device('cuda' if torch.cuda.is_available() and use_gpu else 'cpu')
        super().__init__(train_features=None, train_labels=train_labels, test_features=None, test_labels=test_labels)

    def _train(self, hyperparameters: Dict[str, Union[int, float, str]]) -> nn.Module:
        """
        Trains the PyTorch Geometric model using the specified hyperparameters.

        Parameters
        ----------
        hyperparameters : Dict[str, Union[int, float, str]]
            A dictionary of hyperparameters for training, such as batch size and learning rate.

        Returns
        -------
        nn.Module
            The trained PyTorch Geometric model.
        """
        batch_size = hyperparameters.get('batch_size', 32)
        learning_rate = hyperparameters.get('learning_rate', 1e-3)

        model = self.build_model(hyperparameters).to(self.device)
        optimizer = self._get_optimizer(hyperparameters.get('optimizer', 'adam'), model.parameters(), learning_rate)
        criterion = nn.CrossEntropyLoss()

        self.train_loader = DataLoader(self.train_data, batch_size=batch_size, shuffle=True)
        self.test_loader = DataLoader(self.test_data, batch_size=batch_size, shuffle=False)

        early_stopping = EarlyStopping(patience=5, min_delta=0.01)
        model.train()

        for epoch in range(self.max_epochs):
            for batch in self.train_loader:
                batch = batch.to(self.device)
                optimizer.zero_grad()
                output = model(batch)
                loss = criterion(output, batch.y)
                loss.backward()
                optimizer.step()

            val_loss = self._evaluate_loss(model, criterion)

            if early_stopping.step(val_loss, model):
                early_stopping.load_best_weights(model)
                break

        return model

    def _evaluate(self, model: nn.Module, dataset: str) -> Tuple[np.ndarray, np.ndarray]:
        """
        Evaluates the trained model on the specified dataset and returns predicted probabilities and predicted classes.

        Parameters
        ----------
        model : nn.Module
            The trained PyTorch Geometric model.
        dataset : str
            Specifies which dataset to evaluate ('train' or 'test').

        Returns
        -------
        Tuple[np.ndarray, np.ndarray]
            A tuple containing predicted probabilities and predicted class labels.
        """
        model.eval()
        all_probabilities = []
        all_predictions = []

        data_loader = self.train_loader if dataset == 'train' else self.test_loader

        with torch.no_grad():
            for batch in data_loader:
                batch = batch.to(self.device)
                output = model(batch)
                
                probabilities = torch.softmax(output, dim=1)
                all_probabilities.append(probabilities.cpu().numpy())
                
                predictions = torch.argmax(probabilities, dim=1)
                all_predictions.append(predictions.cpu().numpy())

        all_probabilities = np.concatenate(all_probabilities)
        all_predictions = np.concatenate(all_predictions)
        
        return all_probabilities, all_predictions

    def _evaluate_loss(self, model: nn.Module, criterion: nn.Module) -> float:
        """
        Evaluates the model loss on the test dataset.

        Parameters
        ----------
        model : nn.Module
            The trained PyTorch model.
        criterion : nn.Module
            The loss function to use for evaluation.

        Returns
        -------
        float
            The average loss on the test dataset.
        """
        model.eval()
        total_loss = 0
        with torch.no_grad():
            for batch in self.test_loader:
                batch = batch.to(self.device)
                output = model(batch)
                loss = criterion(output, batch.y)
                total_loss += loss.item()
        return total_loss / len(self.test_loader)

    def _save_model(self, model, signature):
        """
        Saves the trained model using MLFlow.

        Parameters
        ----------
        model : nn.Module
            The trained PyTorch Geometric model.
        signature : Any
            The input/output signature for logging the model in MLFlow.
        """
        mlflow.pytorch.log_model(model, "trained_best_model", signature=signature)

    @abstractmethod
    def _suggest_hyperparameters(self, trial: optuna.Trial) -> Dict[str, Union[int, float, str]]:
        """
        Abstract method to suggest hyperparameters for Optuna hyperparameter tuning.

        Parameters
        ----------
        trial : optuna.Trial
            The Optuna trial object, which is used to suggest hyperparameters.

        Returns
        -------
        Dict[str, Union[int, float, str]]
            A dictionary of hyperparameters suggested by Optuna.
        """
        pass

    @abstractmethod
    def build_model(self, hyperparameters: Dict[str, Any]) -> nn.Module:
        """
        Abstract method to build a PyTorch Geometric model based on the provided hyperparameters.

        Parameters
        ----------
        hyperparameters : Dict[str, Any]
            A dictionary containing hyperparameters for model construction.

        Returns
        -------
        nn.Module
            A PyTorch Geometric model.
        """
        pass

    def _get_optimizer(self, optimizer_name: str, model_parameters, learning_rate: float) -> optim.Optimizer:
        """
        Retrieves the optimizer based on the given optimizer name.

        Parameters
        ----------
        optimizer_name : str
            The name of the optimizer ('adam', 'rmsprop', 'sgd').
        model_parameters : Any
            The parameters of the model to optimize.
        learning_rate : float
            The learning rate for the optimizer.

        Returns
        -------
        optim.Optimizer
            The optimizer object for updating model weights during training.
        """
        optimizers = {
            'adam': optim.Adam,
            'rmsprop': optim.RMSprop,
            'sgd': optim.SGD
        }
        return optimizers[optimizer_name.lower()](model_parameters, lr=learning_rate)
