from abc import ABC, abstractmethod
import mlflow
import optuna
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from typing import Dict, Tuple, Union, Any
import numpy as np
from scipy.sparse import issparse

from ..BaseTunableModel import BaseTunableModel
from .EarlyStopping import EarlyStopping

class PytorchTunable(BaseTunableModel, ABC):
    """
    A tunable PyTorch model that extends the BaseTunableModel and incorporates abstract base class functionality.

    This class provides functionality for:
    - Training a PyTorch model with tunable hyperparameters.
    - Using Optuna for hyperparameter tuning.
    - Saving and logging models with MLFlow for experiment tracking.

    Attributes
    ----------
    train_loader : DataLoader
        PyTorch DataLoader for the training dataset.
    test_loader : DataLoader
        PyTorch DataLoader for the testing dataset.
    max_epochs : int
        Maximum number of epochs for training.
    device : torch.device
        The device (CPU or GPU) to run the model on.
    """
    
    def __init__(self, 
                 train_features: np.ndarray, 
                 train_labels: np.ndarray, 
                 test_features: np.ndarray, 
                 test_labels: np.ndarray, 
                 max_epochs: int = 5000,
                 use_gpu: bool = True):
        """
        Initializes the PytorchTunable class with the provided datasets and configurations.

        Parameters
        ----------
        train_features : np.ndarray
            The feature set for training.
        train_labels : np.ndarray
            The labels for the training set.
        test_features : np.ndarray
            The feature set for testing.
        test_labels : np.ndarray
            The labels for the testing set.
        max_epochs : int, optional
            The maximum number of training epochs (default is 5000).
        use_gpu : bool, optional
            Whether to use GPU if available (default is True).
        """
        self.train_loader = None
        self.test_loader = None
        self.max_epochs = max_epochs
        self.device = torch.device('cuda' if torch.cuda.is_available() and use_gpu else 'cpu')
        super().__init__(train_features, train_labels, test_features, test_labels)

    def _train(self, hyperparameters: Dict[str, Union[int, float, str]]) -> nn.Module:
        """
        Trains the PyTorch model using the provided hyperparameters.

        This method builds the model, prepares the optimizer, loss function, and data loaders,
        and trains the model while applying early stopping.

        Parameters
        ----------
        hyperparameters : Dict[str, Union[int, float, str]]
            A dictionary of hyperparameters, including learning rate, batch size, and optimizer type.

        Returns
        -------
        nn.Module
            The trained PyTorch model.
        """
        input_shape = self.train_features.shape[1:]
        model = self.build_model(input_shape=input_shape, hyperparameters=hyperparameters).to(self.device)
        learning_rate = hyperparameters.get('learning_rate', 1e-3)
        optimizer = self._get_optimizer(hyperparameters.get('optimizer','adam'), model.parameters(), learning_rate)
        
        criterion = nn.CrossEntropyLoss()
        batch_size = hyperparameters.get('batch_size', 32)
        self._prepare_dataloaders(batch_size)

        early_stopping = EarlyStopping(patience=5, min_delta=0.01)

        model.train()
        for epoch in range(self.max_epochs):
            for batch_features, batch_labels in self.train_loader:
                batch_features, batch_labels = batch_features.to(self.device), batch_labels.to(self.device)
                
                optimizer.zero_grad()
                outputs = model(batch_features)
                loss = criterion(outputs, batch_labels)
                loss.backward()
                optimizer.step()

            val_loss = self._evaluate_loss(model, criterion)

            if early_stopping.step(val_loss, model):
                early_stopping.load_best_weights(model)
                break

        return model

    def _evaluate(self, model: torch.nn.Module, dataset: str) -> Tuple[np.ndarray, np.ndarray]:
        """
        Evaluates the model on the specified dataset (train or test) and returns predicted probabilities and labels.

        Parameters
        ----------
        model : torch.nn.Module
            The trained PyTorch model to evaluate.
        dataset : str
            The dataset to evaluate on ('train' or 'test').

        Returns
        -------
        Tuple[np.ndarray, np.ndarray]
            A tuple containing predicted probabilities and predicted class labels.
        """
        model.eval()
        device = next(model.parameters()).device
        features = self.train_features if dataset == 'train' else self.test_features
        features = torch.tensor(features, dtype=torch.float32).to(device)
        
        with torch.no_grad():
            outputs = model(features)
            probabilities = torch.softmax(outputs, dim=1).cpu().numpy()
            predictions = np.argmax(probabilities, axis=1)

        return probabilities, predictions

    def _evaluate_loss(self, model: nn.Module, criterion: nn.Module) -> float:
        """
        Evaluates the loss of the model on the test dataset using the given loss function.

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
        total_loss = 0.0
        with torch.no_grad():
            for batch_features, batch_labels in self.test_loader:
                batch_features, batch_labels = batch_features.to(self.device), batch_labels.to(self.device)
                
                outputs = model(batch_features)
                loss = criterion(outputs, batch_labels)
                total_loss += loss.item()

        return total_loss / len(self.test_loader)

    def _save_model(self, model: nn.Module, signature: Any) -> None:
        """
        Saves the trained PyTorch model using MLFlow.

        Parameters
        ----------
        model : nn.Module
            The trained model to save.
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
            The Optuna trial object used for suggesting hyperparameters.

        Returns
        -------
        Dict[str, Union[int, float, str]]
            A dictionary of suggested hyperparameters.
        """
        pass

    @abstractmethod
    def build_model(self, input_shape: Tuple[int, ...], hyperparameters: Dict[str, Any]) -> nn.Module:
        """
        Abstract method to build a PyTorch model based on the provided hyperparameters.

        Parameters
        ----------
        input_shape : Tuple[int, ...]
            The shape of the input features.
        hyperparameters : Dict[str, Any]
            A dictionary containing model hyperparameters, such as the number of layers and units per layer.

        Returns
        -------
        nn.Module
            The constructed PyTorch model.
        """
        pass

    def _prepare_dataloaders(self, batch_size: int) -> None:
        """
        Prepares the PyTorch DataLoaders for the training and testing datasets.

        This method converts the provided training and testing features and labels into
        PyTorch tensors and creates DataLoader objects.

        Parameters
        ----------
        batch_size : int
            The batch size to use for the DataLoaders.
        """
        def to_tensor(data, dtype):
            if isinstance(data, np.ndarray):
                return torch.tensor(data, dtype=dtype)
            elif issparse(data):
                return torch.tensor(data.toarray(), dtype=dtype)
            elif isinstance(data, torch.Tensor):
                return data.to(dtype)
            else:
                raise TypeError(f"Unsupported data type: {type(data)}")

        train_features_tensor = to_tensor(self.train_features, dtype=torch.float32)
        train_labels_tensor = to_tensor(self.train_labels, dtype=torch.long)
        
        test_features_tensor = to_tensor(self.test_features, dtype=torch.float32)
        test_labels_tensor = to_tensor(self.test_labels, dtype=torch.long)
        
        train_dataset = TensorDataset(train_features_tensor, train_labels_tensor)
        test_dataset = TensorDataset(test_features_tensor, test_labels_tensor)
        
        self.train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
        self.test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

    def _get_optimizer(self, optimizer_name: str, model_parameters: Any, learning_rate: float) -> optim.Optimizer:
        """
        Retrieves the optimizer based on the provided name and learning rate.

        Parameters
        ----------
        optimizer_name : str
            The name of the optimizer ('adam', 'rmsprop', 'sgd', 'adamw').
        model_parameters : Any
            The parameters of the model to optimize.
        learning_rate : float
            The learning rate to use for the optimizer.

        Returns
        -------
        optim.Optimizer
            The selected PyTorch optimizer.

        Raises
        -------
        ValueError
            If an unsupported optimizer name is provided.
        """
        optimizers = {
            'adam': optim.Adam,
            'rmsprop': optim.RMSprop,
            'sgd': optim.SGD,
            'adamw': optim.AdamW
        }

        if optimizer_name.lower() in optimizers:
            return optimizers[optimizer_name.lower()](model_parameters, lr=learning_rate)
        else:
            raise ValueError(f"Unsupported optimizer: {optimizer_name}")
