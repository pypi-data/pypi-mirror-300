import os
import requests
import sys
import math
import traceback
from bson import ObjectId
from matrice.session import Session
from matrice.models import Model


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
        error_logging_route = "/internal/v1/system/log_error"

        try:
            self.rpc.post(url=error_logging_route, data=log_err)
        except Exception as e:
            print(f"Failed to log error: {e}")
        print(f"An exception occurred. Logging the exception information: {log_err}")


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
                print("Download failed")
                raise Exception("Failed to download model from presigned_url")
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
            url = "/v1/project/action"

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


            presigned_url = self.rpc.get(path="/v1/model/get_model_upload_path", params={
                "modelID": model_id,
                "modelType": model_type,
                "filePath": checkpoint_path.split("/")[-1],
                "expiryTimeInMinutes": 59
            })['data']


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

                presigned_url = self.rpc.post(path="/v1/model/get_model_download_path", payload={
                    "modelID": model_id,
                    "modelType": model_type,
                    "expiryTimeInMinutes": 59
                })['data']

            if model_type == "exported":
                presigned_url = self.rpc.post(path="/v1/model/get_model_download_path", payload={
                    "modelID": model_id,
                    "modelType": model_type,
                    "expiryTimeInMinutes": 59,
                    "exportFormat": self.action_details['runtimeFramework'],
                })['data']


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

            url = '/v1/model/add_eval_results'


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
            
    def get_model_train(self, is_exported=False):
        try:
            url = "/v1/model/model_train/" + str(self._idModel_str)
            if is_exported:
                url = f"/v1/model/get_model_train_by_export_id?exportId={self._idModel_str}"
            model_train_doc = self.rpc.get(url)['data']
            return model_train_doc
        
        except Exception as e:
            self.log_error(__file__, 'get_model_train', str(e))
            print(f"Exception in get_model_train: {str(e)}")
            self.update_status("error", "error", "Failed to get model train")
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
            model_train_doc = self.get_model_train(is_exported=is_exported)
            self.index_to_category = model_train_doc.get('indexToCat', {})
            return self.index_to_category
        except Exception as e:
            self.log_error(__file__, 'get_index_to_category', str(e))
            print(f"Exception in get_index_to_category: {str(e)}")
            self.update_status("error", "error", "Failed to get index to category")
            sys.exit(1)


class LocalActionTracker(ActionTracker): # TODO: remove it and use the TestingActionTracker in testing.py
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

