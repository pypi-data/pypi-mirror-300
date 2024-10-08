from matplotlib import pyplot as plt
import numpy as np
from sklearn.metrics import (roc_curve, precision_recall_curve, confusion_matrix)
from sklearn.calibration import calibration_curve
from typing import List, Tuple, Optional
import seaborn as sns

class PlotHelper:
    """
    Helper class to generate plots for binary and multi-class classification evaluation.

    Methods
    -------
    prepare_plots(test_labels: np.ndarray, probabilities: Optional[np.ndarray], predictions: np.ndarray) -> List[Tuple[plt.Figure, str]]
        Prepares all evaluation plots.

    plot_confusion_matrix(test_labels: np.ndarray, predictions: np.ndarray) -> Tuple[plt.Figure, str]
        Generates the confusion matrix plot.

    plot_roc_curve(test_labels: np.ndarray, probabilities: np.ndarray) -> Tuple[plt.Figure, str]
        Generates the ROC curve for binary classification.

    plot_precision_recall_curve(test_labels: np.ndarray, probabilities: np.ndarray) -> Tuple[plt.Figure, str]
        Generates the precision-recall curve for binary classification.

    plot_calibration_curve(test_labels: np.ndarray, probabilities: np.ndarray) -> Tuple[plt.Figure, str]
        Generates the calibration curve for binary classification.

    plot_histogram(test_labels: np.ndarray, probabilities: np.ndarray) -> Tuple[plt.Figure, str]
        Generates the histogram of predicted probabilities.

    plot_normalized_confusion_matrix(test_labels: np.ndarray, probabilities: np.ndarray) -> Tuple[plt.Figure, str]
        Generates the normalized confusion matrix.

    plot_top_k_accuracy_curve(test_labels: np.ndarray, probabilities: np.ndarray) -> Tuple[plt.Figure, str]
        Generates the top-K accuracy curve for multi-class classification.

    plot_cumulative_gains(test_labels: np.ndarray, probabilities: np.ndarray) -> Tuple[plt.Figure, str]
        Generates the cumulative gains plot for binary classification.

    plot_lift_curve(test_labels: np.ndarray, probabilities: np.ndarray) -> Tuple[plt.Figure, str]
        Generates the lift curve for binary classification.

    plot_multiclass_roc_curve(test_labels: np.ndarray, probabilities: np.ndarray) -> Tuple[plt.Figure, str]
        Generates the ROC curve for each class in multi-class classification.

    plot_class_probability_bars(probabilities: np.ndarray, class_names: Optional[List[str]] = None) -> Tuple[plt.Figure, str]
        Generates the class probability bar plot for multi-class classification.
    """

    @staticmethod
    def prepare_plots(
        test_labels: np.ndarray,
        probabilities: Optional[np.ndarray],
        predictions: np.ndarray
    ) -> List[Tuple[plt.Figure, str]]:
        """
        Prepares all evaluation plots for a classification model.

        Parameters
        ----------
        test_labels : np.ndarray
            Ground truth (correct) labels.
        probabilities : Optional[np.ndarray]
            The predicted probabilities returned by the model, required for probability-based plots.
        predictions : np.ndarray
            The predicted class labels returned by the model.

        Returns
        -------
        List[Tuple[plt.Figure, str]]
            A list of tuples where each tuple contains a matplotlib figure and the associated filename for each plot.
        """
        is_binary = len(np.unique(test_labels)) == 2
        plot_list = []

        try:
            plot_list.append(PlotHelper.plot_confusion_matrix(test_labels, predictions))
        except Exception as e:
            print(f"Error in plot_confusion_matrix: {e}")

        if probabilities is not None:
            if is_binary:
                try:
                    plot_list.append(PlotHelper.plot_roc_curve(test_labels, probabilities))
                except Exception as e:
                    print(f"Error in plot_roc_curve: {e}")

                try:
                    plot_list.append(PlotHelper.plot_precision_recall_curve(test_labels, probabilities))
                except Exception as e:
                    print(f"Error in plot_precision_recall_curve: {e}")

                try:
                    plot_list.append(PlotHelper.plot_calibration_curve(test_labels, probabilities))
                except Exception as e:
                    print(f"Error in plot_calibration_curve: {e}")

                try:
                    plot_list.append(PlotHelper.plot_cumulative_gains(test_labels, probabilities))
                except Exception as e:
                    print(f"Error in plot_cumulative_gains: {e}")

                try:
                    plot_list.append(PlotHelper.plot_lift_curve(test_labels, probabilities))
                except Exception as e:
                    print(f"Error in plot_lift_curve: {e}")

            try:
                plot_list.append(PlotHelper.plot_histogram(test_labels, probabilities))
            except Exception as e:
                print(f"Error in plot_histogram: {e}")

            try:
                plot_list.append(PlotHelper.plot_normalized_confusion_matrix(test_labels, probabilities))
            except Exception as e:
                print(f"Error in plot_normalized_confusion_matrix: {e}")

            if not is_binary:
                try:
                    plot_list.append(PlotHelper.plot_top_k_accuracy_curve(test_labels, probabilities))
                except Exception as e:
                    print(f"Error in plot_top_k_accuracy_curve: {e}")

                try:
                    plot_list.append(PlotHelper.plot_multiclass_roc_curve(test_labels, probabilities))
                except Exception as e:
                    print(f"Error in plot_multiclass_roc_curve: {e}")

        return plot_list

    @staticmethod
    def plot_confusion_matrix(test_labels: np.ndarray, predictions: np.ndarray) -> Tuple[plt.Figure, str]:
        """
        Generates the confusion matrix plot.

        Parameters
        ----------
        test_labels : np.ndarray
            Ground truth (correct) labels.
        predictions : np.ndarray
            Predicted class labels.

        Returns
        -------
        Tuple[plt.Figure, str]
            A tuple containing the matplotlib figure of the confusion matrix and the filename to save the plot.
        """
        fig, ax = plt.subplots(figsize=(8, 6))
        cm = confusion_matrix(test_labels, predictions)
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax)
        ax.set_xlabel('Predicted')
        ax.set_ylabel('True')
        ax.set_title('Confusion Matrix')
        plt.close(fig)
        return (fig, "confusion_matrix.png")

    @staticmethod
    def plot_roc_curve(test_labels: np.ndarray, probabilities: np.ndarray) -> Tuple[plt.Figure, str]:
        """
        Generates the ROC curve for binary classification.

        Parameters
        ----------
        test_labels : np.ndarray
            Ground truth (correct) labels.
        probabilities : np.ndarray
            Predicted probabilities, required for the ROC curve.

        Returns
        -------
        Tuple[plt.Figure, str]
            A tuple containing the matplotlib figure of the ROC curve and the filename to save the plot.
        """
        prob = probabilities[:, 1] if probabilities.ndim > 1 else probabilities
        fpr, tpr, _ = roc_curve(test_labels, prob)
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(fpr, tpr, label="ROC Curve")
        ax.set_xlabel("False Positive Rate")
        ax.set_ylabel("True Positive Rate (Recall)")
        ax.set_title("ROC Curve")
        plt.close(fig)
        return (fig, "roc_curve.png")

    @staticmethod
    def plot_precision_recall_curve(test_labels: np.ndarray, probabilities: np.ndarray) -> Tuple[plt.Figure, str]:
        """
        Generates the precision-recall curve for binary classification.

        Parameters
        ----------
        test_labels : np.ndarray
            Ground truth (correct) labels.
        probabilities : np.ndarray
            Predicted probabilities, required for the precision-recall curve.

        Returns
        -------
        Tuple[plt.Figure, str]
            A tuple containing the matplotlib figure of the precision-recall curve and the filename to save the plot.
        """
        precision, recall, _ = precision_recall_curve(test_labels, probabilities[:, 1])
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(recall, precision, label="Precision-Recall Curve")
        ax.set_xlabel("Recall")
        ax.set_ylabel("Precision")
        ax.set_title("Precision-Recall Curve")
        plt.close(fig)
        return (fig, "precision_recall_curve.png")

    @staticmethod
    def plot_calibration_curve(test_labels: np.ndarray, probabilities: np.ndarray) -> Tuple[plt.Figure, str]:
        """
        Generates the calibration curve for binary classification.

        Parameters
        ----------
        test_labels : np.ndarray
            Ground truth (correct) labels.
        probabilities : np.ndarray
            Predicted probabilities, required for the calibration curve.

        Returns
        -------
        Tuple[plt.Figure, str]
            A tuple containing the matplotlib figure of the calibration curve and the filename to save the plot.
        """
        prob_true, prob_pred = calibration_curve(test_labels, probabilities[:, 1], n_bins=10)
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(prob_pred, prob_true, marker='o', label='Calibration Curve')
        ax.plot([0, 1], [0, 1], linestyle='--', label='Perfect Calibration')
        ax.set_xlabel("Predicted Probability")
        ax.set_ylabel("True Probability")
        ax.set_title("Calibration Curve")
        plt.close(fig)
        return (fig, "calibration_curve.png")

    @staticmethod
    def plot_histogram(test_labels: np.ndarray, probabilities: np.ndarray) -> Tuple[plt.Figure, str]:
        """
        Generates the histogram of predicted probabilities.

        Parameters
        ----------
        test_labels : np.ndarray
            Ground truth (correct) labels.
        probabilities : np.ndarray
            Predicted probabilities, required for the histogram plot.

        Returns
        -------
        Tuple[plt.Figure, str]
            A tuple containing the matplotlib figure of the histogram and the filename to save the plot.
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.hist(probabilities.flatten(), bins=len(np.unique(test_labels)), alpha=0.7, color='green', edgecolor='black')
        ax.set_xlabel('Predicted Probability')
        ax.set_ylabel('Frequency')
        ax.set_title('Histogram of Predicted Probabilities for All Classes')
        plt.close(fig)
        return (fig, "histogram_predicted_probabilities.png")

    @staticmethod
    def plot_normalized_confusion_matrix(test_labels: np.ndarray, probabilities: np.ndarray) -> Tuple[plt.Figure, str]:
        """
        Generates the normalized confusion matrix.

        Parameters
        ----------
        test_labels : np.ndarray
            Ground truth (correct) labels.
        probabilities : np.ndarray
            Predicted probabilities, required for calculating normalized confusion matrix.

        Returns
        -------
        Tuple[plt.Figure, str]
            A tuple containing the matplotlib figure of the normalized confusion matrix and the filename to save the plot.
        """
        fig, ax = plt.subplots(figsize=(8, 6))
        cm_normalized = confusion_matrix(test_labels, np.argmax(probabilities, axis=1), normalize='true')
        sns.heatmap(cm_normalized, annot=True, fmt='.2f', cmap='Blues', ax=ax)
        ax.set_xlabel('Predicted')
        ax.set_ylabel('True')
        ax.set_title('Normalized Confusion Matrix')
        plt.close(fig)
        return (fig, "normalized_confusion_matrix.png")

    @staticmethod
    def plot_top_k_accuracy_curve(test_labels: np.ndarray, probabilities: np.ndarray) -> Tuple[plt.Figure, str]:
        """
        Generates the top-K accuracy curve for multi-class classification.

        Parameters
        ----------
        test_labels : np.ndarray
            Ground truth (correct) labels.
        probabilities : np.ndarray
            Predicted probabilities, required for calculating top-K accuracy.

        Returns
        -------
        Tuple[plt.Figure, str]
            A tuple containing the matplotlib figure of the top-K accuracy curve and the filename to save the plot.
        """
        k_values = [1, 3, 5]
        top_k_accuracies = []
        for k in k_values:
            top_k_predictions = np.argsort(probabilities, axis=1)[:, -k:]
            top_k_accuracy = np.mean([1 if test_labels[i] in top_k_predictions[i] else 0 for i in range(len(test_labels))])
            top_k_accuracies.append(top_k_accuracy)

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(k_values, top_k_accuracies, marker='o', label="Top-K Accuracy")
        ax.set_xlabel("K")
        ax.set_ylabel("Accuracy")
        ax.set_title("Top-K Accuracy Curve")
        plt.close(fig)
        return (fig, "top_k_accuracy_curve.png")

    @staticmethod
    def plot_cumulative_gains(test_labels: np.ndarray, probabilities: np.ndarray) -> Tuple[plt.Figure, str]:
        """
        Generates the cumulative gains plot for binary classification.

        Parameters
        ----------
        test_labels : np.ndarray
            Ground truth (correct) labels.
        probabilities : np.ndarray
            Predicted probabilities, required for cumulative gains calculation.

        Returns
        -------
        Tuple[plt.Figure, str]
            A tuple containing the matplotlib figure of the cumulative gains plot and the filename to save the plot.
        """
        sorted_indices = np.argsort(probabilities[:, 1])[::-1]
        sorted_labels = test_labels[sorted_indices]

        cumulative_gains = np.cumsum(sorted_labels) / np.sum(test_labels)
        percentage_of_population = np.arange(1, len(test_labels) + 1) / len(test_labels)

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(percentage_of_population, cumulative_gains, label='Cumulative Gains')
        ax.plot([0, 1], [0, 1], linestyle='--', color='gray', label='Random')
        ax.set_xlabel('Percentage of Population')
        ax.set_ylabel('Cumulative Percentage of Positives')
        ax.set_title('Cumulative Gains Plot')
        plt.close(fig)
        return (fig, "cumulative_gains_plot.png")

    @staticmethod
    def plot_lift_curve(test_labels: np.ndarray, probabilities: np.ndarray) -> Tuple[plt.Figure, str]:
        """
        Generates the lift curve for binary classification.

        Parameters
        ----------
        test_labels : np.ndarray
            Ground truth (correct) labels.
        probabilities : np.ndarray
            Predicted probabilities, required for lift calculation.

        Returns
        -------
        Tuple[plt.Figure, str]
            A tuple containing the matplotlib figure of the lift curve and the filename to save the plot.
        """
        sorted_indices = np.argsort(probabilities[:, 1])[::-1]
        sorted_labels = test_labels[sorted_indices]

        cumulative_gains = np.cumsum(sorted_labels) / np.sum(test_labels)
        percentage_of_population = np.arange(1, len(test_labels) + 1) / len(test_labels)
        lift = np.where(percentage_of_population > 0, cumulative_gains / percentage_of_population, 1)

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(percentage_of_population, lift, label='Lift Curve')
        ax.axhline(1, color='gray', linestyle='--', label='Baseline')
        ax.set_xlabel('Percentage of Population')
        ax.set_ylabel('Lift')
        ax.set_title('Lift Curve')
        plt.close(fig)
        return (fig, "lift_curve.png")

    @staticmethod
    def plot_multiclass_roc_curve(test_labels: np.ndarray, probabilities: np.ndarray) -> Tuple[plt.Figure, str]:
        """
        Generates the ROC curve for each class in a multi-class classification problem.

        Parameters
        ----------
        test_labels : np.ndarray
            Ground truth (correct) labels.
        probabilities : np.ndarray
            Predicted probabilities for each class, required for the ROC curve.

        Returns
        -------
        Tuple[plt.Figure, str]
            A tuple containing the matplotlib figure of the multi-class ROC curve and the filename to save the plot.
        """
        n_classes = probabilities.shape[1]
        fig, ax = plt.subplots(figsize=(10, 6))

        for i in range(n_classes):
            fpr, tpr, _ = roc_curve(test_labels == i, probabilities[:, i])
            ax.plot(fpr, tpr, label=f'Class {i} vs Rest')

        ax.set_xlabel("False Positive Rate")
        ax.set_ylabel("True Positive Rate")
        ax.set_title("ROC Curve for Multi-Class Classification")
        ax.legend()
        plt.close(fig)
        return (fig, "multiclass_roc_curve.png")

    @staticmethod
    def plot_class_probability_bars(probabilities: np.ndarray, class_names: Optional[List[str]] = None) -> Tuple[plt.Figure, str]:
        """
        Plots the predicted probability distribution over classes for a single sample.

        Parameters
        ----------
        probabilities : np.ndarray
            Predicted probabilities for each class.
        class_names : Optional[List[str]], optional
            Optional list of class names for better visualization (default is None).

        Returns
        -------
        Tuple[plt.Figure, str]
            A tuple containing the matplotlib figure of class probability bars and the filename to save the plot.
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        class_indices = np.arange(probabilities.shape[1])
        if class_names is None:
            class_names = [f'Class {i}' for i in class_indices]

        ax.bar(class_indices, probabilities[0], tick_label=class_names)
        ax.set_xlabel('Classes')
        ax.set_ylabel('Predicted Probability')
        ax.set_title('Class Prediction Probabilities')
        plt.close(fig)
        return (fig, "class_probability_bars.png")
