import subprocess
import platform
import sys
import os
import signal
from typing import Any, Dict, Optional
import mlflow


class MLFlowLogger:
    """
    A utility class for logging experiments and metrics using MLflow. This class also provides
    functionality to start and stop the MLflow UI process for experiment tracking.

    Attributes
    ----------
    run_name : Optional[str]
        The name of the run to be logged in MLflow.
    experiment_name : Optional[str]
        The name of the MLflow experiment.
    process : Optional[subprocess.Popen]
        The MLflow UI subprocess if launched.
    """

    def __init__(self, run_name: Optional[str] = None, experiment_name: Optional[str] = None):
        """
        Initializes the MLFlowLogger object and launches the MLflow UI and sets the experiment.

        Parameters
        ----------
        run_name : Optional[str]
            Name of the current run (defaults to None, defaults from MLflow will be used).
        experiment_name : Optional[str]
            Name of the experiment to use (defaults to None, defaults from MLflow will be used).
        """
        self.run_name = run_name
        self.process = None
        self.experiment_name = experiment_name
        self._launch_mlflow_ui()
        if self.experiment_name:
            self.set_experiment(self.experiment_name)

    def set_experiment(self, name: str) -> None:
        """
        Set the experiment in MLflow.

        Parameters
        ----------
        name : str
            The name of the MLflow experiment to set.
        """
        mlflow.set_experiment(name)

    def start_run(self) -> None:
        """
        Start a new run in MLflow with the optionally provided run name.
        """
        mlflow.start_run(run_name=self.run_name)

    def start_nested_run(self, trial_number: int) -> None:
        """
        Start a nested run for hyperparameter tuning or multiple trials.

        Parameters
        ----------
        trial_number : int
            The trial number to log as part of the nested run.
        """
        mlflow.start_run(nested=True, run_name=f"trial_{trial_number}")

    def log_params(self, params: Dict[str, Any]) -> None:
        """
        Log a dictionary of parameters for the current run.

        Parameters
        ----------
        params : Dict[str, Any]
            A dictionary of parameter names and values to log.
        """
        mlflow.log_params(params)

    def log_metrics(self, metrics: Dict[str, Any]) -> None:
        """
        Log a dictionary of metrics for the current run.

        Parameters
        ----------
        metrics : Dict[str, Any]
            A dictionary of metric names and values to log.
        """
        mlflow.log_metrics(metrics)

    def log_figure(self, fig: Any, name: str) -> None:
        """
        Log a matplotlib figure for the current run.

        Parameters
        ----------
        fig : Any
            A matplotlib figure object to log.
        name : str
            The name of the figure file to store in MLflow.
        """
        mlflow.log_figure(fig, name)

    def log_param_importances(self, importances: Dict[str, Any]) -> None:
        """
        Log the importance of hyperparameters as a dictionary.

        Parameters
        ----------
        importances : Dict[str, Any]
            A dictionary of hyperparameters and their importances.
        """
        mlflow.log_dict(importances, "hyperparameter_importances.json")

    def log_text(self, text: str, file_name: str = 'logs.txt') -> None:
        """
        Log text data to a file in MLflow.

        Parameters
        ----------
        text : str
            The text content to log.
        file_name : str, optional
            The file name to store the text log in MLflow (default is 'logs.txt').
        """
        mlflow.log_text(text, file_name)

    def end_run(self) -> None:
        """
        End the current MLflow run.
        """
        mlflow.end_run()

    def _close_mlflow(self) -> None:
        """
        Terminate the MLflow UI process if it was started by this instance.
        """
        if self.process:
            try:
                if platform.system() == "Windows":
                    subprocess.run(
                        ["taskkill", "/F", "/T", "/PID", str(self.process.pid)], shell=True)
                else:
                    os.killpg(os.getpgid(self.process.pid), signal.SIGTERM)
                print("MLflow UI process terminated successfully.")
            except Exception as e:
                print(f"Failed to close MLflow UI: {str(e)}")
        else:
            print("No MLflow process to terminate.")

    def _launch_mlflow_ui(self) -> None:
        """
        Launch the MLflow UI in the background as a subprocess.
        Detects the platform and starts the UI accordingly.
        """
        os_name = platform.system()

        try:
            if os_name in ["Linux", "Darwin"]:
                self._launch_on_unix()
            elif os_name == "Windows":
                self._launch_on_windows()
            else:
                print(f"Unsupported OS: {os_name}")
                sys.exit(1)
        except Exception as e:
            print(f"Failed to open MLflow UI: {str(e)}")
            sys.exit(1)

    def _launch_on_unix(self) -> None:
        """
        Launch the MLflow UI on Unix-like systems (Linux, macOS).
        """
        self.process = subprocess.Popen(["mlflow", "ui"], preexec_fn=os.setsid)
        print(f"MLflow UI started with PID {self.process.pid}")

    def _launch_on_windows(self) -> None:
        """
        Launch the MLflow UI on Windows.
        """
        self.process = subprocess.Popen(
            ["mlflow", "ui"], creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
        print(f"MLflow UI started with PID {self.process.pid}")
