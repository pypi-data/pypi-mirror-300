"""
Module for handling logging of model training epochs in projects.

This module provides functionalities for retrieving and visualizing training logs 
from models within a project, including plotting training and validation losses 
and other metrics over epochs.
"""

import matplotlib.pyplot as plt
import seaborn as sns


class ModelLogging:
    """
    A class to manage model logging for tracking training progress.

    The `ModelLogging` class allows fetching training logs from the server and 
    generating visualizations for losses and other metrics during training epochs.

    Parameters
    ----------
    session : object
        An active session object used for making RPC calls to the server.
    model_id : str, optional
        The ID of the model to fetch logs for. Defaults to None.

    Attributes
    ----------
    model_id : str or None
        The unique identifier of the model for which logs are fetched.
    rpc : object
        The RPC client used to make API requests for retrieving logs.

    Example
    -------
    >>> session = Session()
    >>> model_logging = ModelLogging(session=session, model_id="model_12345")
    >>> logs, error, message = model_logging.get_model_training_logs()
    """

    def __init__(self, session, model_id=None):
        self.model_id = model_id
        self.rpc = session.rpc

    def get_model_training_logs(self):
        """
        Fetch training logs for the specified model.

        This method retrieves the logs of the training epochs for a model, including
        both training and validation metrics such as losses and accuracy.

        Returns
        -------
        tuple
            A tuple containing:
            - A dictionary with the response from the RPC call.
            - An error message if the request fails.
            - A success message if the request succeeds.

        Example
        -------
        >>> response, error, message = model_logging.get_model_training_logs()
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(f"Success: {message}")
        """
        path = f"/v1/model_logging/model/{self.model_id}/train_epoch_logs"
        resp = self.rpc.get(path=path)
        if resp.get("success"):
            error = None
            message = "Successfully fetched model logs."
        else:
            error = resp.get("message")
            message = "Failed to fetch model logs."

        return resp, error, message

    def plot_epochs_losses(self):
        """
        Plot training and validation losses over epochs.

        This method generates two subplots: one for the training losses and one for 
        the validation losses, displaying how these metrics evolve over the epochs.

        Returns
        -------
        None

        Example
        -------
        >>> model_logging.plot_epochs_losses()
        """
        resp, error, message = self.get_model_training_logs()
        training_logs = resp["data"]

        epochs = []
        metrics = {"train": {}, "val": {}}
        for epoch_data in training_logs:
            epochs.append(epoch_data["epoch"])
            for detail in epoch_data["epochDetails"]:
                metric_name = detail["metricName"]
                metric_value = detail["metricValue"]
                split_type = detail["splitType"]

                if "loss" in metric_name:
                    if split_type not in metrics:
                        metrics[split_type] = []
                    if metric_name not in metrics[split_type]:
                        metrics[split_type][metric_name] = []
                    metrics[split_type][metric_name].append(metric_value)

        # Set plot style
        sns.set(style="whitegrid")
        # Create figure and axes
        fig, axs = plt.subplots(2, 1, figsize=(12, 18))
        
        # Plot training losses
        for split_type, split_metrics in metrics.items():
            for metric_name in split_metrics.keys():
                if split_type == "train":
                    axs[0].plot(
                        epochs,
                        split_metrics[metric_name],
                        label=f"{split_type} {metric_name}",
                    )
                elif split_type == "val":
                    axs[1].plot(
                        epochs,
                        split_metrics[metric_name],
                        label=f"{split_type} {metric_name}",
                    )

        # Set labels and titles
        axs[0].set_xlabel("Epoch", fontsize=14)
        axs[0].set_ylabel("Loss", fontsize=14)
        axs[0].legend(fontsize=12)
        axs[0].set_title("Training Losses over Epochs", fontsize=16)
        axs[0].grid(True)

        axs[1].set_xlabel("Epoch", fontsize=14)
        axs[1].set_ylabel("Loss", fontsize=14)
        axs[1].legend(fontsize=12)
        axs[1].set_title("Validation Losses over Epochs", fontsize=16)
        axs[1].grid(True)

        plt.tight_layout()
        plt.show()

    def plot_epochs_metrics(self):
        """
        Plot training and validation metrics (excluding losses) over epochs.

        This method generates subplots for each non-loss metric, such as accuracy, 
        showing how these metrics change during training epochs for both training 
        and validation splits.

        Returns
        -------
        None

        Example
        -------
        >>> model_logging.plot_epochs_metrics()
        """
        resp, error, message = self.get_model_training_logs()
        training_logs = resp["data"]

        epochs = []
        metrics = {"train": {}, "val": {}}
        metrics_names = set()

        # Parse metrics data from logs
        for epoch_data in training_logs:
            epochs.append(epoch_data["epoch"])
            for detail in epoch_data["epochDetails"]:
                metric_name = detail["metricName"]
                metric_value = detail["metricValue"]
                split_type = detail["splitType"]

                if "loss" not in metric_name:
                    if split_type not in metrics:
                        metrics[split_type] = []
                    if metric_name not in metrics[split_type]:
                        metrics[split_type][metric_name] = []
                    metrics[split_type][metric_name].append(metric_value)
                    metrics_names.add(metric_name)

        metrics_names = list(metrics_names)
        num_graphs = len(metrics_names)

        # Set plot style
        sns.set(style="whitegrid")
        fig, axs = plt.subplots(num_graphs, 1, figsize=(12, 18))

        # Plot each metric
        for metric_index, metric_name in enumerate(metrics_names):
            for split_type, split_metrics in metrics.items():
                if metric_name in metrics[split_type]:
                    axs[metric_index].plot(
                        epochs,
                        split_metrics[metric_name],
                        label=f"{split_type} {metric_name}",
                    )

            axs[metric_index].set_xlabel("Epoch", fontsize=14)
            axs[metric_index].set_ylabel(metric_name, fontsize=14)
            axs[metric_index].legend(fontsize=12)
            axs[metric_index].set_title(f"{metric_name} over Epochs", fontsize=16)
            axs[metric_index].grid(True)

        plt.tight_layout()
        plt.show()
