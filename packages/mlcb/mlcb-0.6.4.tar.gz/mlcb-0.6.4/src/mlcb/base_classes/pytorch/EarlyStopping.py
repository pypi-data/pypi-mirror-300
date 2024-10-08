import torch.nn as nn
from typing import Optional, Dict
import torch

class EarlyStopping:
    """
    Implements early stopping to terminate training when the validation loss stops improving.

    This class is useful for preventing overfitting and unnecessary training when the model has stopped improving on the validation set.

    Attributes
    ----------
    patience : int
        Number of epochs with no improvement after which training will be stopped.
    min_delta : float
        Minimum change in the monitored loss to qualify as an improvement. Smaller changes are considered insignificant.
    best_loss : float
        The best validation loss observed so far.
    best_model_weights : Optional[Dict[str, torch.Tensor]]
        The model weights from the epoch with the best validation loss.
    patience_counter : int
        Counter to track the number of epochs without improvement in the validation loss.
    """
    
    def __init__(self, patience: int = 5, min_delta: float = 0.001):
        """
        Initializes the EarlyStopping instance with the specified patience and minimum delta.

        Parameters
        ----------
        patience : int, optional
            Number of epochs to wait for an improvement before stopping (default is 5).
        min_delta : float, optional
            Minimum change in the validation loss required to reset the patience counter (default is 0.001).
        """
        self.patience = patience
        self.min_delta = min_delta
        self.best_loss = float('inf')
        self.best_model_weights = None
        self.patience_counter = 0

    def step(self, current_loss: float, model: nn.Module) -> bool:
        """
        Evaluates the current validation loss and updates the early stopping state.

        If the current loss is lower than the previous best loss by at least `min_delta`, the patience counter is reset,
        and the best model weights are saved. If the loss has not improved, the patience counter is incremented.

        Parameters
        ----------
        current_loss : float
            The current validation loss of the model.
        model : nn.Module
            The model whose weights will be saved if an improvement is detected in the validation loss.

        Returns
        -------
        bool
            True if early stopping criteria are met (i.e., patience is exhausted), signaling to stop training. 
            False otherwise, indicating training should continue.
        """
        if current_loss < self.best_loss - self.min_delta:
            self.best_loss = current_loss
            self.best_model_weights = model.state_dict()
            self.patience_counter = 0
        else:
            self.patience_counter += 1

        if self.patience_counter >= self.patience:
            return True
        return False

    def load_best_weights(self, model: nn.Module) -> None:
        """
        Loads the best model weights, which were saved when the validation loss was at its lowest point.

        Parameters
        ----------
        model : nn.Module
            The model whose weights will be replaced with the best saved weights.
        """
        if self.best_model_weights is not None:
            model.load_state_dict(self.best_model_weights)
