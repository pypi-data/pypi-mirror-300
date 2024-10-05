import math
import os
import shutil
import sys
import tarfile
import traceback
import zipfile
from types import SimpleNamespace

import requests
import yaml
from bson import ObjectId
from pycocotools.coco import COCO

from matrice import rpc
from matrice.models import Model
from matrice.session import Session


class dotdict(dict):
    """
    A dictionary subclass that allows dot notation access to its attributes.

    This class enables both standard dictionary key access and dot notation access for easier manipulation
    of data attributes. It can be particularly useful for handling configuration parameters or other data
    structures where attributes are frequently accessed.

    Example
    -------
    >>> my_dict = dotdict({'key': 'value'})
    >>> print(my_dict.key)  # Outputs: value
    >>> print(my_dict['key'])  # Outputs: value

    Parameters
    ----------
    initial_data : dict, optional
        An optional dictionary to initialize the `dotdict`. If provided, the items will be added to the `dotdict`.

    Attributes
    ----------
    None

    Methods
    -------
    __getattr__(key)
        Retrieves the value associated with the given key using dot notation.
    
    __setattr__(key, value)
        Sets the value for the given key using dot notation.
    
    __delattr__(key)
        Deletes the specified key from the dictionary using dot notation.

    Examples
    --------
    >>> my_dict = dotdict({'name': 'Alice', 'age': 30})
    >>> print(my_dict.name)  # Outputs: Alice
    >>> my_dict.location = 'Wonderland'
    >>> print(my_dict['location'])  # Outputs: Wonderland
    >>> del my_dict.age
    >>> print(my_dict)  # Outputs: dotdict({'name': 'Alice', 'location': 'Wonderland'})
    """

    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

# TODO: Need to add documentation
class ActionTracker:
    """
    Tracks and manages the status, actions, and related data of a model's lifecycle, including training, evaluation, and deployment processes.

    The `ActionTracker` is responsible for tracking various stages of an action (e.g., model training, evaluation, or deployment),
    logging details, fetching configuration parameters, downloading model checkpoints, and handling error logging.
    It interacts with the backend system to retrieve and update action statuses.

    Parameters
    ----------
    action_id : str, optional
        The unique identifier of the action to be tracked. If not provided, the class will initialize without an active action.
        The `action_id` is typically linked to specific activities such as model training, evaluation, or deployment.

    Attributes
    ----------
    rpc : RPCClient
        A Remote Procedure Call (RPC) client for interacting with the backend API.
    action_id : bson.ObjectId
        The ObjectId representing the action being tracked. This is used for retrieving action details from the backend.
    action_id_str : str
        The string representation of the `action_id`.
    action_doc : dict
        The detailed document containing information about the action, including its status, type, and related model details.
    action_type : str
        The type of action being tracked, such as 'model_train', 'model_eval', or 'deploy_add'.
    _idModel : bson.ObjectId
        The ObjectId of the model associated with the current action.
    _idModel_str : str
        The string representation of `_idModel`.
    session : Session
        A session object that manages the user session and ensures that API requests are authorized.

    Examples
    --------
    >>> tracker = ActionTracker(action_id="60f5f5bfb5a1c2a123456789")
    >>> tracker.get_job_params()
    >>> tracker.update_status("training", "in_progress", "Model training started")
    >>> tracker.log_epoch_results(1, [{'loss': 0.25, 'accuracy': 0.92}])
    """

    def __init__(self, action_id=None):
        """
        Initializes the ActionTracker instance and retrieves details related to the specified action ID.

        This constructor fetches the action document, which contains metadata about the action, including the model's ID.
        If no `action_id` is provided, the tracker is initialized without an action.

        Parameters
        ----------
        action_id : str, optional
            The unique identifier of the action to track. If not provided, the instance is initialized without an action.

        Raises
        ------
        ConnectionError
            If there is an error retrieving action details from the backend.
        SystemExit
            If there is a critical error during initialization, causing the system to terminate.

        Examples
        --------
        >>> tracker = ActionTracker(action_id="60f5f5bfb5a1c2a123456789")
        >>> print(tracker.action_type)  # Outputs the action type, e.g., "model_train"
        """
        try:
            session = Session()
            self.rpc = session.rpc #TODO: Make this private as self.__rpc

            if action_id is not None:
                self.action_id = ObjectId(action_id)
                self.action_id_str = str(self.action_id)
                url = f"/v1/project/action/{self.action_id_str}/details"
                self.action_doc = self.rpc.get(url)['data']
                #print(self.action_doc)
                self.action_details = self.action_doc['actionDetails']
                self.action_type = self.action_doc['action']

                # Will be updated
                if self.action_type in ("model_train", "model_eval"):
                    self._idModel = self.action_doc["_idService"]
                    self._idModel_str = str(self._idModel)
                elif self.action_type == "deploy_add":
                    self._idModel = self.action_details["_idModelDeploy"]
                    self._idModel_str = str(self._idModel)
                else:
                    self._idModel = self.action_details["_idModel"]
                    self._idModel_str = str(self._idModel)
            else:
                self.action_id = None
                print("ActionTracker initialized. but No action found")

            project_id = self.action_doc["_idProject"]
            # port=self.action_doc["port"]

            try:
                session.update_session(project_id=project_id)
                self.session = session
            except Exception as e:
                print("update project error", e)

            try:
                print(self.get_job_params()) #TODO: comment out
                self.checkpoint_path, self.pretrained = self.get_checkpoint_path(self.get_job_params())
            except Exception as e:
                print("get checkpoint error", e)

        except Exception as e:
            print("PAR", e)
            self.log_error(__file__, "__init__", str(e))
            self.update_status("error", "error", "Initialization failed")
            sys.exit(1)

    ## TODO: Make this private using __log_error 
    def log_error(self, filename, function_name, error_message):
        """
        Logs error details to the backend system for debugging and tracking purposes.

        Parameters
        ----------
        filename : str
            The name of the file where the error occurred.
        function_name : str
            The function in which the error occurred.
        error_message : str
            A description of the error encountered.

        Returns
        -------
        None

        Examples
        --------
        >>> tracker.log_error("action_tracker.py", "__init__", "Failed to initialize tracker")
        """
        traceback_str = traceback.format_exc().rstrip()
        # Constructing the exception information dictionary
        log_err = {
            "serviceName": "Python-Common",
            "stackTrace": traceback_str,
            "errorType": "Internal",
            "description": error_message,
            "fileName": filename,
            "functionName": function_name,
            "moreInfo": {},
        }
        r = rpc.RPC()
        error_logging_route = "/internal/v1/system/log_error"
        #r.post(url=error_logging_route, data=log_err) #TODO: Why is this comment out? Fix this
        print("An exception occurred. Logging the exception information: "+traceback_str)

    ## TODO: rename this function to download_model or something different and meaningful
    def download_model_1(self, model_save_path, presigned_url):
        try:
            response = requests.get(presigned_url)
            if response.status_code == 200:
                with open(model_save_path, "wb") as file:
                    file.write(response.content)
                print("Download Successful")
                return True
            else:
                print(f"Download failed with status code: {response.status_code}")
                return False
        except Exception as e:
            self.log_error(__file__, "download_model_1", str(e))
            print(f"Exception in download_model_1: {str(e)}")
            sys.exit(1)

    def get_checkpoint_path(self, model_config):
        """
        Determines the checkpoint path for the model based on the configuration provided.

        This function checks if the model's checkpoint should be retrieved from a pre-trained source or a specific model ID.
        It also handles downloading the model if necessary.

        Parameters
        ----------
        model_config : dict
            A dictionary containing the configuration parameters for the model, such as `checkpoint_type` and `model_checkpoint`.

        Returns
        -------
        tuple
            A tuple containing:
            - The absolute path of the model checkpoint if found.
            - A boolean indicating whether the model is pre-trained.

        Raises
        ------
        FileNotFoundError
            If the model checkpoint cannot be downloaded or located.
        ConnectionError
            If there is an issue communicating with the model's API.

        Examples
        --------
        >>> config = {"checkpoint_type": "model_id", "model_checkpoint": "12345abcde"}
        >>> checkpoint_path, is_pretrained = tracker.get_checkpoint_path(config)
        >>> print(checkpoint_path, is_pretrained)
        """
        try:
            checkpoint_type = model_config.get("checkpoint_type", "predefined")
            model_checkpoint = model_config.get("model_checkpoint", "auto")
            checkpoint_dir = "./checkpoints"
            os.makedirs(checkpoint_dir, exist_ok=True)

            if checkpoint_type == "model_id":
                if model_checkpoint.lower() not in ["", "none", "auto"]:
                    model_save_path = os.path.abspath(f"{checkpoint_dir}/last.pt")
                    return (
                        self._download_trained_model_checkpoint(
                            model_save_path, model_checkpoint
                        ),
                        True,
                    )
                else:
                    print(
                        f"model_checkpoint {model_checkpoint} is one of [none, auto, ''] it should be a model id"
                    )
                    return None, False

            elif checkpoint_type == "predefined":
                if model_checkpoint.lower() == "auto":
                    return None, True
                elif model_checkpoint.lower() in ["none", ""]:
                    return None, False
                else:
                    print(
                        f"model_checkpoint {model_checkpoint} not from [none, auto, '']"
                    )
                    return None, False
            else:
                print(
                    f"checkpoint_type {checkpoint_type} not from [model_id, predefined]"
                )
                return None, False

        except Exception as e:
            self.log_error(__file__, "get_checkpoint_path", str(e))
            print(f"Exception in get_checkpoint_path: {str(e)}")
            return None, False

    def _download_trained_model_checkpoint(
        self, model_save_path, model_id
    ):  # TODO test this func and update it with the updated SDK
        try:
            model_sdk = Model(self.session, model_id)
            model_save_path = model_sdk.download_model(model_save_path)

            if model_save_path:
                print("Download Successful")
                return model_save_path
            else:
                print(f"Download failed")
                raise Exception(f"Failed to download model from presigned_url")
        except Exception as e:
            self.log_error(__file__, "download_trained_model_checkpoint", str(e))
            print(f"Exception in download_trained_model_checkpoint: {str(e)}")
            sys.exit(1)

    def get_job_params(self):
        """
        Fetches the parameters for the job associated with the current action.

        This method retrieves the parameters required to perform a specific action, such as model training or evaluation.
        The parameters are returned as a dot-accessible dictionary (`dotdict`) for convenience.

        Returns
        -------
        dotdict
            A dot-accessible dictionary containing the job parameters.

        Raises
        ------
        KeyError
            If the job parameters cannot be found in the action document.
        SystemExit
            If the job parameters cannot be retrieved and the system needs to terminate.

        Examples
        --------
        >>> job_params = tracker.get_job_params()
        >>> print(job_params.learning_rate)  # Accessing parameters using dot notation
        """
        try:
            self.jobParams = self.action_doc["jobParams"]
            return dotdict(self.jobParams)
        except Exception as e:
            self.log_error(__file__, "get_job_params", str(e))
            print(f"Exception in get_job_params: {str(e)}")
            self.update_status("error", "error", "Failed to get job parameters")
            sys.exit(1)

    def update_status(self, stepCode, status, status_description):
        """
        Updates the status of the tracked action in the backend system.

        This method allows changing the action's status, such as from "in progress" to "completed" or "error".
        It logs the provided message with the updated status.

        Parameters
        ----------
        action_name : str
            The name of the action being tracked (e.g., "training", "evaluation").
        status : str
            The new status to set for the action (e.g., "in_progress", "completed", "error").
        message : str
            A message providing context about the status update.

        Returns
        -------
        None

        Examples
        --------
        >>> tracker.update_status("training", "completed", "Training completed successfully")
        """
        try:
            print(status_description)
            url = f"/v1/project/action"

            payload = {
                "_id": self.action_id_str,
                "action": self.action_type,
                "serviceName": self.action_doc["serviceName"],
                "stepCode": stepCode,
                "status": status,
                "statusDescription": status_description,
            }

            self.rpc.put(path=url, payload=payload)
        except Exception as e:
            self.log_error(__file__, "update_status", str(e))
            print(f"Exception in update_status: {str(e)}")
            if status == "error":
                sys.exit(1)

    def log_epoch_results(self, epoch, epoch_result_list):
        """
        Logs the results of an epoch during model training or evaluation.

        This method records various metrics (like loss and accuracy) for a specific epoch.
        It updates the action status and logs the results for tracking purposes.

        Parameters
        ----------
        epoch : int
            The epoch number for which the results are being logged.
        results : list of dict
            A list of dictionaries containing the metric results for the epoch.

        Returns
        -------
        None

        Raises
        ------
        ValueError
            If the epoch number is invalid.

        Examples
        --------
        >>> tracker.log_epoch_results(1, [{'loss': 0.25, 'accuracy': 0.92}])
        """
        try:
            epoch_result_list = self.round_metrics(epoch_result_list)
            model_log_payload = {
                "_idModel": self._idModel_str,
                "_idAction": self.action_id_str,
                "epoch": epoch,
                "epochDetails": epoch_result_list,
            }

            headers = {"Content-Type": "application/json"}
            path = f"/v1/model_logging/model/{self._idModel_str}/train_epoch_log"

            self.rpc.post(path=path, headers=headers, payload=model_log_payload)
        except Exception as e:
            self.log_error(__file__, "log_epoch_results", str(e))
            print(f"Exception in log_epoch_results: {str(e)}")
            self.update_status("error", "error", "Failed to log epoch results")
            sys.exit(1)

    def round_metrics(self, epoch_result_list):
        """Rounds the metrics in the epoch results to 4 decimal places.

        Parameters
        ----------
        epoch_result_list : list
            A list of result dictionaries for the epoch. Each dictionary contains:
                - "metricValue" (float): The value of the metric to be rounded.

        Returns
        -------
        list
            The updated list of epoch results with rounded metrics. Each metric value is rounded to four decimal places, with special handling for invalid values (NaN or infinity).

        Examples
        --------
        >>> results = [{'metricValue': 0.123456}, {'metricValue': float('inf')}, {'metricValue': None}]
        >>> rounded_results = round_metrics(results)
        >>> print(rounded_results)
        [{'metricValue': 0.1235}, {'metricValue': 0}, {'metricValue': 0.0001}]
        """
        for metric in epoch_result_list:
            if metric["metricValue"] is not None:
                # Check if the value is within JSON-compliant range
                if math.isinf(metric["metricValue"]) or math.isnan(
                    metric["metricValue"]
                ):
                    metric["metricValue"] = 0
                else:
                    metric["metricValue"] = round(metric["metricValue"], 4)
                if metric["metricValue"] == 0:
                    metric["metricValue"] = 0.0001
        return epoch_result_list

    def upload_checkpoint(self, checkpoint_path, model_type="trained"):
        """Uploads a model checkpoint to the backend system.

        Parameters
        ----------
        checkpoint_path : str
            The file path of the checkpoint to upload. This should point to a valid model checkpoint file.
        model_type : str, optional
            The type of the model ("trained" or "exported"). Defaults to "trained", which refers to a model that has been trained but not yet exported.

        Returns
        -------
        bool
            True if the upload was successful, False otherwise. The function will log an error and exit if an exception occurs during the upload process.

        Examples
        --------
        >>> success = upload_checkpoint("path/to/checkpoint.pth")
        >>> if success:
        >>>     print("Checkpoint uploaded successfully!")
        >>> else:
        >>>     print("Checkpoint upload failed.")
        """
        try:
            if self.action_type == "model_export" and model_type == "exported":
                model_id = self.action_doc["_idService"]
            else:
                model_id = self._idModel_str

            presigned_url = self.rpc.get(
                path=f"/v1/model/get_model_upload_path",
                params={
                    "modelID": model_id,
                    "modelType": model_type,
                    "filePath": checkpoint_path.split("/")[-1],
                    "expiryTimeInMinutes": 59,
                },
            )["data"]

            with open(checkpoint_path, "rb") as file:
                response = requests.put(presigned_url, data=file)

            if response.status_code == 200:
                print("Upload Successful")
                return True
            else:
                print(f"Upload failed with status code: {response.status_code}")
                return False
        except Exception as e:
            self.log_error(__file__, "upload_checkpoint", str(e))
            print(f"Exception in upload_checkpoint: {str(e)}")
            self.update_status("error", "error", "Checkpoint upload failed")
            sys.exit(1)

    def download_model(self, model_path, model_type="trained"):
        """Downloads a model from the backend system.

        Parameters
        ----------
        model_path : str
            The path to save the downloaded model. The file will be saved at this location after downloading.
        model_type : str, optional
            The type of the model ("trained" or "exported"). Defaults to "trained".

        Returns
        -------
        bool
            True if the download was successful, False otherwise. The function will log an error and exit if an exception occurs during the download process.

        Examples
        --------
        >>> success = download_model("path/to/save/model.pth")
        >>> if success:
        >>>     print("Model downloaded successfully!")
        >>> else:
        >>>     print("Model download failed.")
        """
        try:
            model_id = self._idModel_str

            if model_type == "trained":
                presigned_url = self.rpc.post(
                    path=f"/v1/model/get_model_download_path",
                    payload={
                        "modelID": model_id,
                        "modelType": model_type,
                        "expiryTimeInMinutes": 59,
                    },
                )["data"]

            if model_type == "exported":
                presigned_url = self.rpc.post(
                    path=f"/v1/model/get_model_download_path",
                    payload={
                        "modelID": model_id,
                        "modelType": model_type,
                        "expiryTimeInMinutes": 59,
                        "exportFormat": self.action_details["runtimeFramework"],
                    },
                )["data"]

            response = requests.get(presigned_url)

            if response.status_code == 200:
                with open(model_path, "wb") as file:
                    file.write(response.content)
                print("Download Successful")
                return True
            else:
                print(f"Download failed with status code: {response.status_code}")
                return False
        except Exception as e:
            self.log_error(__file__, "download_model", str(e))
            print(f"Exception in download_model: {str(e)}")
            self.update_status("error", "error", "Model download failed")
            sys.exit(1)

    def save_evaluation_results(self, list_of_result_dicts):
        """Saves the evaluation results for a model.

        Parameters
        ----------
        list_of_result_dicts : list
            A list of dictionaries containing the evaluation results. Each dictionary should include relevant metrics and their values for the model's performance.

        Raises
        ------
        Exception
            Logs an error and exits if an exception occurs during the saving process.

        Examples
        --------
        >>> evaluation_results = [
        >>>     {"metric": "accuracy", "value": 0.95},
        >>>     {"metric": "loss", "value": 0.05},
        >>> ]
        >>> save_evaluation_results(evaluation_results)
        """
        try:
            url = f"/v1/model/add_eval_results"

            Payload = {
                "_idModel": self._idModel,
                "_idDataset": self.action_details["_idDataset"],
                "_idProject": self.action_doc["_idProject"],
                "isOptimized": self.action_details.get("isOptimized", False),
                "runtimeFramework": self.action_details.get(
                    "runtimeFramework", "Pytorch"
                ),
                "datasetVersion": self.action_details["datasetVersion"],
                "splitTypes": "",
                "evalResults": list_of_result_dicts,
            }

            self.rpc.post(path=url, payload=Payload)
        except Exception as e:
            self.log_error(__file__, "save_evaluation_results", str(e))
            print(f"Exception in save_evaluation_results: {str(e)}")
            self.update_status("error", "error", "Failed to save evaluation results")
            sys.exit(1)

    def add_index_to_category(self, indexToCat):
        """Adds an index-to-category mapping to the model.

        This function is used to establish a relationship between numerical indices 
        and their corresponding categorical labels for the model. This mapping is 
        essential for interpreting the model's output, particularly when the 
        model is designed to classify input data into distinct categories.

        When to Use:
        -------------
        - This function is typically called after the model has been trained 
        but before deploying the model for inference. It ensures that the 
        indices output by the model during predictions can be accurately 
        translated to human-readable category labels.
        - It is also useful when there are changes in the class labels 
        or when initializing a new model.

        Parameters
        ----------
        indexToCat : dict
            A dictionary mapping integer indices to category names. For example, 
            `{0: 'cat', 1: 'dog', 2: 'bird'}` indicates that index 0 corresponds 
            to 'cat', index 1 to 'dog', and index 2 to 'bird'.

        Raises
        ------
        Exception
            If an error occurs while trying to add the mapping, it logs the error 
            details and exits the process.

        Examples
        --------
        >>> index_mapping = {0: 'cat', 1: 'dog', 2: 'bird'}
        >>> add_index_to_category(index_mapping)
        """
        try:
            url = f"/v1/model/{self._idModel}/update_index_to_cat"
            payload = {"indexToCat": indexToCat}
            self.rpc.put(path=url, payload=payload)
        except Exception as e:
            self.log_error(__file__, "add_index_to_category", str(e))
            print(f"Exception in add_index_to_category: {str(e)}")
            self.update_status("error", "error", "Failed to add index to category")
            sys.exit(1)

    def get_index_to_category(self, is_exported=False):
        """Fetches the index-to-category mapping for the model.

        This function retrieves the current mapping of indices to categories 
        from the backend system. This is crucial for understanding the model's 
        predictions, as it allows users to decode the model outputs back 
        into meaningful category labels.

        When to Use:
        -------------
        - This function is often called before making predictions with the model 
        to ensure that the index-to-category mapping is up to date and correctly 
        reflects the model's configuration.
        - It can also be used after exporting a model to validate that the 
        expected mappings are correctly stored and accessible.

        Parameters
        ----------
        is_exported : bool, optional
            A flag indicating whether to fetch the mapping for an exported model. 
            Defaults to False. If True, the mapping is retrieved based on the export ID.

        Returns
        -------
        dict
            The index-to-category mapping as a dictionary, where keys are indices 
            and values are corresponding category names.

        Raises
        ------
        Exception
            If an error occurs during the retrieval process, it logs the error 
            details and exits the process.

        Examples
        --------
        >>> mapping = get_index_to_category()
        >>> print(mapping)
        {0: 'cat', 1: 'dog', 2: 'bird'}

        >>> exported_mapping = get_index_to_category(is_exported=True)
        >>> print(exported_mapping)
        {0: 'cat', 1: 'dog'}
        """
        try:
            url = "/v1/model/model_train/" + str(self._idModel_str)
            if is_exported:
                url = f"/v1/model/get_model_train_by_export_id?exportId={self._idModel_str}"

            modelTrain_doc = self.rpc.get(url)["data"]
            self.index_to_category = modelTrain_doc.get("indexToCat", {})

            return self.index_to_category
        except Exception as e:
            self.log_error(__file__, "get_index_to_category", str(e))
            print(f"Exception in get_index_to_category: {str(e)}")
            self.update_status("error", "error", "Failed to get index to category")
            sys.exit(1)


import json
import os
import shutil
import zipfile

import requests


class _LocalActionTracker(ActionTracker):
    def __init__(
        self,
        action_type,
        model_name,
        model_arch,
        output_type,
        action_id=None,
        local_model_path=None,
    ):
        session = Session()
        self.rpc = session.rpc
        self.local_model_path = local_model_path
        self.model_name = model_name
        self.model_arch = model_arch
        self.output_type = output_type
        self.checkpoint_path, self.pretrained = self.get_checkpoint_path()
        self.action_type = action_type
        assert action_id is None, "Action ID should be None for LocalActionTracker"
        self.action_doc = self.mock_action_doc()
        self.action_details = self.action_doc["actionDetails"]

        # Download the dataset and prepare it for the action type in the specific format
        self.prepare_dataset()
        self.create_config()

    def mock_action_doc(self, input_type="image"):
        try:
            api_url = f"/v1/system/get_dataset_url?inputType={input_type}&outputType={self.output_type}"
            response = self.rpc.get(
                path=api_url,
                params={"inputType": input_type, "outputType": self.output_type},
            )
            if response and "data" in response:
                mock_dataset = response["data"]
            else:
                raise ValueError("Invalid response from the API call")

            action_details = {
                "_idModel": "mocked_model_id",
                "runtimeFramework": "Pytorch",
                "datasetVersion": "v1.0",
                "dataset_url": mock_dataset,
                "project_type": self.output_type,
                "input_type": input_type,
                "output_type": self.output_type,
            }
            # Store _idModel as an instance variable
            self._idModel = action_details["_idModel"]
            return {
                "actionDetails": action_details,
                "action": self.action_type,
                "serviceName": "mocked_service_name",
                "_idProject": "mocked_project_id",
            }
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def prepare_dataset(self):
        dataset_images_dir = "workspace/dataset"

        if os.path.exists(dataset_images_dir):
            print(
                f"Dataset directory {dataset_images_dir} already exists. Skipping download and preparation."
            )
        else:
            dataset_url = self.action_details.get("dataset_url")
            project_type = self.action_details.get("project_type")
            input_type = self.action_details.get("input_type")
            output_type = self.action_details.get("output_type")

            print(
                f"Preparing dataset from {dataset_url} for project type {project_type} with input type {input_type} and output type {output_type}"
            )

            dataset_dir = "workspace/dataset"
            os.makedirs(dataset_dir, exist_ok=True)
            self.download_and_extract_dataset(dataset_url, dataset_dir)

            # Prepare the dataset according to the project type
            if project_type == "classification":
                self.prepare_classification_dataset(dataset_dir)

            elif project_type == "detection":
                if self.model_name == "Yolov8":
                    self.prepare_yolo_dataset(dataset_dir)
                else:
                    self.prepare_detection_dataset(dataset_dir)
            else:
                print(f"Unsupported project type: {project_type}")

    def download_and_extract_dataset(self, dataset_url, dataset_dir):
        # Extract the file name from the URL
        file_name = os.path.basename(dataset_url)
        local_file_path = os.path.join(dataset_dir, file_name)

        try:
            # Download the file
            with requests.get(dataset_url, stream=True) as r:
                r.raise_for_status()

                print(f"Response status code: {r.status_code}")
                print(f"Response headers: {r.headers}")

                content_type = r.headers.get("Content-Type", "Unknown")
                print(f"Content-Type: {content_type}")

                # Save the file
                with open(local_file_path, "wb") as f:
                    shutil.copyfileobj(r.raw, f)

            print(f"File downloaded successfully from {dataset_url}")
            print(f"Saved as: {local_file_path}")

            # Extract the file based on its extension
            if file_name.endswith(".zip"):
                with zipfile.ZipFile(local_file_path, "r") as zip_ref:
                    zip_ref.extractall(dataset_dir)
                print("Zip file extracted successfully")
            elif file_name.endswith(".tar.gz") or file_name.endswith(".tgz"):
                with tarfile.open(local_file_path, "r:gz") as tar:
                    tar.extractall(path=dataset_dir)
                print("Tar.gz file extracted successfully")
            else:
                print(f"Unsupported file format: {file_name}")
                return

            # Remove the compressed file after extraction
            os.remove(local_file_path)
            print(f"Removed the compressed file: {local_file_path}")

        except requests.exceptions.RequestException as e:
            print(f"Error downloading dataset from {dataset_url}: {e}")
        except (zipfile.BadZipFile, tarfile.TarError) as e:
            print(f"Error extracting dataset from {local_file_path}: {e}")

    def get_file_extension(self, content_type):
        content_type = content_type.lower()
        if "zip" in content_type:
            return ".zip"
        elif "gzip" in content_type or "x-gzip" in content_type:
            return ".gz"
        elif "tar" in content_type:
            return ".tar"
        elif "octet-stream" in content_type:
            return ""  # Binary file, no specific extension
        else:
            return ""  # Unknown type, no extension

    def prepare_classification_dataset(self, dataset_dir):
        print("Preparing classification dataset...")

        # Locate the vehicle-c10-20 directory
        sub_dirs = [
            os.path.join(dataset_dir, d)
            for d in os.listdir(dataset_dir)
            if os.path.isdir(os.path.join(dataset_dir, d))
        ]
        if len(sub_dirs) != 1:
            raise ValueError("Expected a single subdirectory in the dataset directory")
        vehicle_dir = sub_dirs[0]
        print(f"Main Sub directory: {vehicle_dir}")

        images_dir = os.path.join(dataset_dir, "images")
        os.makedirs(images_dir, exist_ok=True)
        print(f"Images directory: {images_dir}")

        class_names = set()
        split_info = {}  # To keep track of which images belong to which split

        # Iterate through train, val, and test splits
        for split in ["train", "val", "test"]:
            split_dir = os.path.join(vehicle_dir, split)
            dst_split_dir = os.path.join(images_dir, split)
            os.makedirs(dst_split_dir, exist_ok=True)
            split_info[split] = {}

            for class_name in os.listdir(split_dir):
                class_dir = os.path.join(split_dir, class_name)
                if os.path.isdir(class_dir):
                    class_names.add(class_name)
                    dst_class_dir = os.path.join(dst_split_dir, class_name)
                    os.makedirs(dst_class_dir, exist_ok=True)

                    # Copy images and keep track of which split they belong to
                    for img in os.listdir(class_dir):
                        src_path = os.path.join(class_dir, img)
                        dst_path = os.path.join(dst_class_dir, img)
                        shutil.copy2(src_path, dst_path)

                        if class_name not in split_info[split]:
                            split_info[split][class_name] = []
                        split_info[split][class_name].append(dst_path)

        # Retrieve class names and count
        self.num_classes = len(class_names)
        self.class_names = list(class_names)

        print(f"Number of classes: {self.num_classes}")
        print(f"Class names: {self.class_names}")

        # Optionally, you can save the split information for later use
        # For example, you could save it as a JSON file
        import json

        with open(os.path.join(dataset_dir, "split_info.json"), "w") as f:
            json.dump(split_info, f)

    def prepare_detection_dataset(self, dataset_dir):
        print("Preparing detection dataset...")

        # Find the downloaded folder
        contents = os.listdir(dataset_dir)
        downloaded_dirs = [
            d
            for d in contents
            if os.path.isdir(os.path.join(dataset_dir, d))
            and d not in ("images", "annotations")
        ]

        if not downloaded_dirs:
            print("No suitable subdirectory found in the dataset directory.")
            return

        if len(downloaded_dirs) > 1:
            print(
                f"Multiple subdirectories found: {downloaded_dirs}. Using the first one."
            )

        downloaded_dir = os.path.join(dataset_dir, downloaded_dirs[0])
        print(f"Found downloaded directory: {downloaded_dir}")

        # Source paths
        src_images_dir = os.path.join(downloaded_dir, "images")
        src_annotations_dir = os.path.join(downloaded_dir, "annotations")

        # Destination paths
        dst_images_dir = os.path.join(dataset_dir, "images")
        dst_annotations_dir = os.path.join(dataset_dir, "annotations")

        # Move images folder
        if os.path.exists(src_images_dir):
            if os.path.exists(dst_images_dir):
                shutil.rmtree(dst_images_dir)
            shutil.move(src_images_dir, dst_images_dir)
            print(f"Moved images folder to {dst_images_dir}")
        else:
            print("Images folder not found in the downloaded directory")

        # Move annotations folder
        if os.path.exists(src_annotations_dir):
            if os.path.exists(dst_annotations_dir):
                shutil.rmtree(dst_annotations_dir)
            shutil.move(src_annotations_dir, dst_annotations_dir)
            print(f"Moved annotations folder to {dst_annotations_dir}")
        else:
            print("Annotations folder not found in the downloaded directory")

        # Remove the downloaded folder if it's empty
        if os.path.exists(downloaded_dir) and not os.listdir(downloaded_dir):
            os.rmdir(downloaded_dir)
            print(f"Removed empty downloaded folder: {downloaded_dir}")

        print("Dataset preparation completed.")

    def convert_bbox_to_yolo(self, size, box):
        dw = 1.0 / size[0]
        dh = 1.0 / size[1]
        x = (box[0] + box[2] / 2.0) * dw
        y = (box[1] + box[3] / 2.0) * dh
        w = box[2] * dw
        h = box[3] * dh
        return (x, y, w, h)

    def create_data_yaml(self, dataset_dir, class_names):
        data_yaml = {
            "path": dataset_dir,
            "train": "images/train2017",
            "val": "images/val2017",
            "test": "images/test2017",
            "names": class_names,
        }

        yaml_path = os.path.join(dataset_dir, "data.yaml")
        with open(yaml_path, "w") as file:
            yaml.dump(data_yaml, file, default_flow_style=False)

        print(f"Created data.yaml file at {yaml_path}")

    import os
    import shutil

    from pycocotools.coco import COCO

    def prepare_yolo_dataset(self, dataset_dir):
        print("Preparing YOLO dataset...")

        # Create the 'datasets' directory one level above the 'workspace' directory
        root_dir = os.path.abspath(os.path.join(dataset_dir, os.pardir, os.pardir))
        datasets_dir = os.path.join(root_dir, "datasets")
        if not os.path.exists(datasets_dir):
            os.makedirs(datasets_dir)

        # New directory structure: datasets/workspace/dataset
        workspace_dir = os.path.basename(os.path.dirname(dataset_dir))
        new_workspace_dir = os.path.join(datasets_dir, workspace_dir)
        if not os.path.exists(new_workspace_dir):
            os.makedirs(new_workspace_dir)

        new_dataset_dir = os.path.join(new_workspace_dir, os.path.basename(dataset_dir))
        if os.path.exists(new_dataset_dir):
            shutil.rmtree(new_dataset_dir)
        shutil.move(dataset_dir, new_dataset_dir)
        dataset_dir = new_dataset_dir

        # Find the downloaded folder
        contents = os.listdir(dataset_dir)
        downloaded_dirs = [
            d
            for d in contents
            if os.path.isdir(os.path.join(dataset_dir, d))
            and d not in ("images", "annotations")
        ]

        if not downloaded_dirs:
            print("No suitable subdirectory found in the dataset directory.")
            return

        if len(downloaded_dirs) > 1:
            print(
                f"Multiple subdirectories found: {downloaded_dirs}. Using the first one."
            )

        downloaded_dir = os.path.join(dataset_dir, downloaded_dirs[0])
        print(f"Found downloaded directory: {downloaded_dir}")

        # Source paths
        src_images_dir = os.path.join(downloaded_dir, "images")
        src_annotations_dir = os.path.join(downloaded_dir, "annotations")

        # Destination paths
        dst_images_dir = os.path.join(dataset_dir, "images")
        dst_annotations_dir = os.path.join(dataset_dir, "annotations")

        # Move images folder
        if os.path.exists(src_images_dir):
            if os.path.exists(dst_images_dir):
                shutil.rmtree(dst_images_dir)
            shutil.move(src_images_dir, dst_images_dir)
            print(f"Moved images folder to {dst_images_dir}")
        else:
            print("Images folder not found in the downloaded directory")

        # Move annotations folder
        if os.path.exists(src_annotations_dir):
            if os.path.exists(dst_annotations_dir):
                shutil.rmtree(dst_annotations_dir)
            shutil.move(src_annotations_dir, dst_annotations_dir)
            print(f"Moved annotations folder to {dst_annotations_dir}")
        else:
            print("Annotations folder not found in the downloaded directory")

        # Convert annotations to YOLO format
        annotation_file = os.path.join(dst_annotations_dir, "instances_train2017.json")
        coco = COCO(annotation_file)
        img_dir = dst_images_dir
        ann_dir = os.path.join(dataset_dir, "labels")
        if not os.path.exists(ann_dir):
            os.makedirs(ann_dir)

        # Subdirectories for labels
        label_dirs = {
            "train": os.path.join(ann_dir, "train2017"),
            "val": os.path.join(ann_dir, "val2017"),
            "test": os.path.join(ann_dir, "test2017"),
        }
        for dir_path in label_dirs.values():
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)

        # Get class names
        categories = coco.loadCats(coco.getCatIds())
        class_names = [category["name"] for category in categories]

        for img_id in coco.getImgIds():
            img_info = coco.loadImgs(img_id)[0]
            img_filename = img_info["file_name"]
            img_width = img_info["width"]
            img_height = img_info["height"]

            ann_ids = coco.getAnnIds(imgIds=img_id)
            anns = coco.loadAnns(ann_ids)

            if "train" in img_filename:
                label_path = os.path.join(
                    label_dirs["train"], img_filename.replace(".jpg", ".txt")
                )
            elif "val" in img_filename:
                label_path = os.path.join(
                    label_dirs["val"], img_filename.replace(".jpg", ".txt")
                )
            else:
                label_path = os.path.join(
                    label_dirs["test"], img_filename.replace(".jpg", ".txt")
                )

            with open(label_path, "w") as f:
                for ann in anns:
                    bbox = ann["bbox"]
                    yolo_bbox = self.convert_bbox_to_yolo((img_width, img_height), bbox)
                    category_id = ann["category_id"] - 1
                    f.write(f"{category_id} {' '.join(map(str, yolo_bbox))}\n")

        # Remove the downloaded folder if it's empty
        if os.path.exists(downloaded_dir) and not os.listdir(downloaded_dir):
            os.rmdir(downloaded_dir)
            print(f"Removed empty downloaded folder: {downloaded_dir}")

        # Create the data.yaml file
        self.create_data_yaml(dataset_dir, class_names)

        print("Dataset preparation completed.")

    def get_checkpoint_path(self):
        try:
            checkpoint_dir = "./checkpoints"
            # Ensure the checkpoints directory exists
            if not os.path.exists(checkpoint_dir):
                os.makedirs(checkpoint_dir)
                print(f"Created checkpoint directory: {checkpoint_dir}")
                return None, False  # No checkpoints available
            # List all files in the checkpoints directory
            checkpoint_files = [
                f for f in os.listdir(checkpoint_dir) if f.endswith(".pt")
            ]
            if not checkpoint_files:
                print("No checkpoint files found in the checkpoints directory.")
                return None, False
            # If there are multiple checkpoints, you might want to choose the most recent one
            # For simplicity, we're just choosing the first one here
            checkpoint_path = os.path.join(checkpoint_dir, checkpoint_files[0])
            print(f"Found checkpoint: {checkpoint_path}")
            return checkpoint_path, True
        except Exception as e:
            self.log_error(__file__, "get_checkpoint_path", str(e))
            print(f"Exception in get_checkpoint_path: {str(e)}")
            return None, False

    def create_config(self):
        model_name = self.model_name
        action_type = self.action_type

        if action_type == "train":
            config_path = os.path.join(
                os.getcwd(), "configs", model_name, "train-config.json"
            )

            print(config_path)

            if os.path.exists(config_path):
                with open(config_path, "r") as config_file:
                    self.config = json.load(config_file)
                print(f"Loaded train config for model {model_name}: {self.config}")

                # Create model_config dictionary
                self.model_config = {}
                for config in self.config.get("actionConfig", []):
                    key_name = config.get("keyName")
                    default_value = config.get("defaultValue")
                    if key_name and default_value is not None:
                        self.model_config[key_name] = self.cast_value(
                            config.get("valueType"), default_value
                        )
                print(f"Model config: {self.model_config}")
            else:
                raise FileNotFoundError(
                    f"Train configuration file not found for model {model_name} at {config_path}"
                )

        elif action_type == "export":
            config_dir = os.path.join(
                os.path.dirname(os.getcwd()), "config", model_name
            )

            if os.path.exists(config_dir) and os.path.isdir(config_dir):
                self.export_configs = {}
                for file_name in os.listdir(config_dir):
                    if file_name.startswith("export-") and file_name.endswith(
                        "-config.json"
                    ):
                        export_format = file_name[len("export-") : -len("-config.json")]
                        export_config_path = os.path.join(config_dir, file_name)
                        with open(export_config_path, "r") as config_file:
                            self.export_configs[export_format] = json.load(config_file)
                        print(
                            f"Loaded export config for format {export_format}: {self.export_configs[export_format]}"
                        )
            else:
                raise FileNotFoundError(
                    f"Export Configuration directory not found for model {model_name} at {config_dir}"
                )
        else:
            raise ValueError(f"Unsupported action type: {action_type}")

    def cast_value(self, value_type, value):
        if value_type == "int32":
            return int(value)
        elif value_type == "float32":
            return float(value)
        elif value_type == "string":
            return str(value)
        elif value_type == "bool":
            return bool(value)
        else:
            return value

    def update_status(self, stepCode, status, status_description):
        print(f"Mock update status: {stepCode}, {status}, {status_description}")

    def upload_checkpoint(self, checkpoint_path, model_type="trained"):
        print(f"Mock upload checkpoint: {checkpoint_path}, {model_type}")
        return True

    def download_model(self, model_path, model_type="trained"):
        print(f"Mock download model to: {model_path}, {model_type}")
        local_model_file = os.path.join(
            self.local_model_path, f"{model_type}_model.pth"
        )
        with open(local_model_file, "rb") as src, open(model_path, "wb") as dest:
            dest.write(src.read())
        return True

    def get_job_params(self):
        # Return job params according to the requirements in train.py
        dataset_path = "dataset"
        model_config = dotdict(
            {
                "data": f"workspace/{dataset_path}/images",
                "val_ratio": 0.1,
                "test_ratio": 0.1,
                "batch_size": 1,
                "epochs": 1,
                "lr": 0.001,
                "momentum": 0.9,
                "weight_decay": 0.0001,
                "lr_step_size": 7,
                "lr_gamma": 0.1,
                "patience": 5,
                "min_delta": 0.001,
                "arch": self.model_arch,
                "pretrained": True,
                "gpu": 0,
                "dataset_path": dataset_path,
                "opt": "adamw",
                "model_key": self.model_arch,
                "lr_scheduler": "steplr",
                "checkpoint_path": self.checkpoint_path,
            }
        )

        return model_config

    def save_evaluation_results(self, list_of_result_dicts):
        print(f"Mock save evaluation results: {list_of_result_dicts}")

    def add_index_to_category(self, indexToCat):
        print(f"Mock add index to category: {indexToCat}")

    def get_index_to_category(self, is_exported=False):
        # Create a folder and save the data for the local run
        folder_path = os.path.join(self.local_model_path, "index_to_category")
        os.makedirs(folder_path, exist_ok=True)
        file_path = os.path.join(folder_path, "index_to_category.json")
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                return json.load(file)
        else:
            index_to_category = {}  # Example empty dictionary
            with open(file_path, "w") as file:
                json.dump(index_to_category, file)
            return index_to_category

    def log_epoch_results(self, epoch, epoch_result_list):
        try:
            model_log_payload = {
                "_idModel": self._idModel,
                "epoch": epoch,
                "epochDetails": epoch_result_list,
            }

            print(model_log_payload)

        except Exception as e:
            self.log_error(__file__, "log_epoch_results", str(e))
            print(f"Exception in log_epoch_results: {str(e)}")
            self.update_status("error", "error", "Failed to log epoch results")
            sys.exit(1)

    def get_metrics(data_loader, model, device, index_to_labels):
        all_outputs = []
        all_targets = []

        print(model)
        print(device)
        print(index_to_labels)

        # Set model to evaluation mode for inference
        model.eval()
        print("Model evaluating")

        # Accumulate predictions (detcetion)
        # with torch.no_grad():
        #     for images, targets in data_loader:
        #         images = [image.to(device) for image in images]
        #         targets = [{k: v.to(device) if isinstance(v, torch.Tensor) else v for k, v in t.items()} for t in targets]

        #         outputs = model(images)
        #         all_outputs.extend(outputs)
        #         all_targets.extend(targets)

        print("Model evaluated")
