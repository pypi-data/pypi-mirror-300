"""
This module provides utilities for machine learning evaluation metrics, experiment logging, and visualization.

Package overview
----------------

MetricsHelper
    Contains functions to calculate various classification metrics for both binary and multi-class classification tasks.

    Key functionality includes:
    - `calculate_metrics`: Computes a wide range of classification metrics, such as accuracy, precision, recall, F1 score, ROC AUC, and more.

MLFlowLogger
    A utility class to log experiments, metrics, and artifacts to MLflow, with support for single and nested runs.

    Key functionality includes:
    - Starting and ending MLflow runs.
    - Logging metrics, parameters, figures, and custom text to MLflow.
    - Launching and terminating the MLflow UI for real-time experiment tracking.

PlotHelper
    Provides functions to generate various evaluation plots for binary and multi-class classification models.

    Key functionality includes:
    - Generating confusion matrices, ROC curves, precision-recall curves, calibration curves, and more.
    - Support for both binary and multi-class classification plots.
    - Preparing multiple evaluation plots for easier analysis of model performance.
"""
