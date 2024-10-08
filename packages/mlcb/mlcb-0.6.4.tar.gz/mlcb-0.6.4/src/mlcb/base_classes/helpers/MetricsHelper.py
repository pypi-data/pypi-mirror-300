from typing import Dict, Optional
import numpy as np
from sklearn.metrics import (
    accuracy_score, log_loss, precision_score, recall_score, f1_score,
    balanced_accuracy_score, cohen_kappa_score, roc_auc_score,
    average_precision_score, matthews_corrcoef, hamming_loss,
    jaccard_score, brier_score_loss, zero_one_loss, fowlkes_mallows_score,
)


class MetricsHelper:
    """
    Helper class to calculate various classification metrics for both binary and multi-class classification problems.

    Methods
    -------
    calculate_metrics(labels: np.ndarray, probabilities: Optional[np.ndarray], predictions: np.ndarray) -> Dict[str, float]
        Computes a dictionary of various performance metrics based on the provided labels, probabilities, and predictions.
    """

    @staticmethod
    def calculate_metrics(
        labels: np.ndarray,
        probabilities: Optional[np.ndarray],
        predictions: np.ndarray
    ) -> Dict[str, float]:
        """
        Calculates a range of classification performance metrics.

        Parameters
        ----------
        labels : np.ndarray
            Ground truth (correct) class labels. Can be binary or multi-class.
        probabilities : Optional[np.ndarray]
            The predicted probabilities returned by the model. Required for metrics such as log loss, ROC AUC, and Brier score. 
            Should be of shape (n_samples, n_classes) or (n_samples, 2) for binary classification.
        predictions : np.ndarray
            The predicted class labels returned by the model.

        Returns
        -------
        metrics : Dict[str, float]
            A dictionary containing various calculated metrics, such as accuracy, precision, recall, F1 score, etc. 
            If probabilities are provided, metrics like log loss, ROC AUC, PR AUC, and Brier score will also be included.

        Notes
        -----
        - Some metrics (e.g., ROC AUC, PR AUC, Brier score) require probability estimates for the positive class in binary classification.
        """
        labels_count = len(np.unique(labels))
        is_binary = labels_count == 2
        average_type = 'weighted'
        metrics = {}

        try:
            metrics['accuracy'] = accuracy_score(labels, predictions)
        except Exception as e:
            print(f"Error calculating accuracy: {e}")

        try:
            metrics['precision'] = precision_score(
                labels, predictions, average=average_type, zero_division=0)
        except Exception as e:
            print(f"Error calculating precision: {e}")

        try:
            metrics['recall'] = recall_score(
                labels, predictions, average=average_type, zero_division=0)
        except Exception as e:
            print(f"Error calculating recall: {e}")

        try:
            metrics['f1_score'] = f1_score(
                labels, predictions, average=average_type, zero_division=0)
        except Exception as e:
            print(f"Error calculating f1_score: {e}")

        try:
            metrics['balanced_accuracy'] = balanced_accuracy_score(
                labels, predictions)
        except Exception as e:
            print(f"Error calculating balanced_accuracy: {e}")

        try:
            metrics['cohen_kappa'] = cohen_kappa_score(labels, predictions)
        except Exception as e:
            print(f"Error calculating cohen_kappa: {e}")

        try:
            metrics['matthews_corrcoef'] = matthews_corrcoef(
                labels, predictions)
        except Exception as e:
            print(f"Error calculating matthews_corrcoef: {e}")

        try:
            metrics['hamming_loss'] = hamming_loss(labels, predictions)
        except Exception as e:
            print(f"Error calculating hamming_loss: {e}")

        try:
            metrics['jaccard_score'] = jaccard_score(
                labels, predictions, average=average_type)
        except Exception as e:
            print(f"Error calculating jaccard_score: {e}")

        try:
            metrics['zero_one_loss'] = zero_one_loss(labels, predictions)
        except Exception as e:
            print(f"Error calculating zero_one_loss: {e}")

        try:
            metrics['fowlkes_mallows'] = fowlkes_mallows_score(
                labels, predictions)
        except Exception as e:
            print(f"Error calculating fowlkes_mallows: {e}")

        if probabilities is not None:
            try:
                metrics['log_loss'] = log_loss(
                    labels, probabilities, labels=np.unique(labels))
            except Exception as e:
                print(f"Error calculating log_loss: {e}")

            if is_binary:
                try:
                    positive_class_probs = probabilities[:, 1]
                    metrics['roc_auc'] = roc_auc_score(
                        labels, positive_class_probs)
                except Exception as e:
                    print(f"Error calculating roc_auc: {e}")

                try:
                    metrics['pr_auc'] = average_precision_score(
                        labels, positive_class_probs)
                except Exception as e:
                    print(f"Error calculating pr_auc: {e}")

                try:
                    metrics['brier_score'] = brier_score_loss(
                        labels, positive_class_probs)
                except Exception as e:
                    print(f"Error calculating brier_score: {e}")

        return metrics
