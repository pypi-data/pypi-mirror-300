"""
Module for interacting with the Model Prediction API.
"""

class ModelPrediction:
    """
    Class for handling model prediction requests and monitoring metrics.

    This class provides methods to interact with the Model Prediction API,
    including monitoring request totals, counts, latencies, and making predictions.

    Attributes:
    -----------
    project_id : str
        The ID of the project for which predictions are being made.
    deployment_id : str
        The ID of the model deployment used for predictions.
    rpc : object
        The RPC client that facilitates communication with the API server.

    Methods:
    --------
    __init__(session, deployment_id=None):
        Initializes the ModelPrediction instance with the project and deployment details.
        
    _handle_response(response, success_message, failure_message):
        Standardizes the API response for easy processing.

    request_total_monitor(deployment_id=None):
        Monitors the total number of requests made to a given deployment.

    request_count_monitor(start_date, end_date, granularity="second", deployment_id=None):
        Monitors the count of requests in a specific time frame and with a specified granularity.

    request_latency_monitor(start_date, end_date, granularity="second", deployment_id=None):
        Monitors the request latency over a specified period.

    get_model_prediction(image_path, auth_key):
        Fetches model predictions for a given image.

    get_model_test(model_train_id, image_path):
        Tests a trained model with a given image.
    
    Parameters:
    -----------
    session : object
        A session object containing project ID and authentication details.
    deployment_id : str, optional
        The ID of the model deployment, by default None.
    
    Example:
    --------
    >>> session = Session(project_id="project123")
    >>> model_prediction = ModelPrediction(session, deployment_id="deploy456")
    """

    def __init__(self, session, deployment_id=None):
        """
        Initializes the ModelPrediction class with a session and optional deployment ID.

        Parameters:
        -----------
        session : object
            The session object containing project ID and authentication details.
        deployment_id : str, optional
            The ID of the deployment to monitor, by default None.

        Example:
        --------
        >>> session = Session(project_id="project123")
        >>> model_prediction = ModelPrediction(session, deployment_id="deploy456")
        """
        self.project_id = session.project_id
        self.deployment_id = deployment_id
        self.rpc = session.rpc

    def _handle_response(self, response, success_message, failure_message):
        """
        Handles API response by returning a standardized tuple with the result, error, and message.

        Parameters:
        -----------
        response : dict
            The API response to process.
        success_message : str
            The message to return in case of success.
        failure_message : str
            The message to return in case of failure.

        Returns:
        --------
        tuple:
            A tuple consisting of (result, error, message).

        Example:
        --------
        >>> response = {"success": True, "data": {"count": 100}}
        >>> result, error, message = model_prediction._handle_response(response, "Success", "Failure")
        >>> print(result, error, message)
        {'count': 100} None Success
        """
        if response.get("success"):
            result = response.get("data")
            error = None
            message = success_message
        else:
            result = None
            error = response.get("message")
            message = failure_message
        print(response)
        return result, error, message

    def request_total_monitor(self, deployment_id=None):
        """
        Monitors the total number of requests for a given deployment.

        Parameters:
        -----------
        deployment_id : str, optional
            The ID of the deployment to monitor. If not provided, the instance's deployment ID will be used.

        Returns:
        --------
        tuple:
            A tuple consisting of (result, error, message) containing the total number of requests.

        Example:
        --------
        >>> result, error, message = model_prediction.request_total_monitor()
        >>> print(result)
        {'total_requests': 1000}
        """
        deployment_id_url = deployment_id if deployment_id else self.deployment_id
        path = f"/v1/model_prediction/monitor/req_total/{deployment_id_url}?projectId={self.project_id}"
        headers = {"Content-Type": "application/json"}
        body = {}

        resp = self.rpc.post(path=path, headers=headers, payload=body)
        return self._handle_response(
            resp,
            "Request total monitored successfully",
            "An error occurred while monitoring the request total.",
        )

    def request_count_monitor(self, start_date, end_date, granularity="second", deployment_id=None):
        """
        Monitors the count of requests for a specific time range and granularity.

        Parameters:
        -----------
        start_date : str
            The start date of the monitoring period in ISO format.
        end_date : str
            The end date of the monitoring period in ISO format.
        granularity : str, optional
            The time granularity for the count (e.g., second, minute). Default is "second".
        deployment_id : str, optional
            The ID of the deployment to monitor.

        Returns:
        --------
        tuple:
            A tuple consisting of (result, error, message) containing request counts.

        Example:
        --------
        >>> start = "2024-01-28T18:30:00.000Z"
        >>> end = "2024-02-29T10:11:27.000Z"
        >>> result, error, message = model_prediction.request_count_monitor(start, end)
        >>> print(result)
        {'counts': [{'timestamp': '2024-01-28T18:30:00Z', 'count': 50}, ...]}
        """
        path = f"/v1/model_prediction/monitor/request_count"
        headers = {"Content-Type": "application/json"}
        body = {
            "granularity": granularity,
            "startDate": start_date,
            "endDate": end_date,
            "status": "REQ. COUNT",
            "deploymentId": deployment_id if deployment_id else self.deployment_id,
        }
        resp = self.rpc.post(path=path, headers=headers, payload=body)

        return self._handle_response(
            resp,
            "Request count monitored successfully",
            "An error occurred while monitoring the request count.",
        )

    def request_latency_monitor(self, start_date, end_date, granularity="second", deployment_id=None):
        """
        Monitors the request latency for a specific time range and granularity.

        Parameters:
        -----------
        start_date : str
            The start date of the monitoring period in ISO format.
        end_date : str
            The end date of the monitoring period in ISO format.
        granularity : str, optional
            The time granularity for latency tracking (e.g., second, minute). Default is "second".
        deployment_id : str, optional
            The ID of the deployment to monitor.

        Returns:
        --------
        tuple:
            A tuple consisting of (result, error, message) containing latency information.

        Example:
        --------
        >>> start = "2024-01-28T18:30:00.000Z"
        >>> end = "2024-02-29T10:11:27.000Z"
        >>> result, error, message = model_prediction.request_latency_monitor(start, end)
        >>> print(result)
        {'latencies': [{'timestamp': '2024-01-28T18:30:00Z', 'avg_latency': 0.05}, ...]}
        """
        path = f"/v1/model_prediction/monitor/latency"
        headers = {"Content-Type": "application/json"}
        body = {
            "granularity": granularity,
            "startDate": start_date,
            "endDate": end_date,
            "status": "AVG. LATENCY",
            "deploymentId": deployment_id if deployment_id else self.deployment_id,
        }
        resp = self.rpc.post(path=path, headers=headers, payload=body)

        return self._handle_response(
            resp,
            "Latency count monitored successfully",
            "An error occurred while monitoring the latency count.",
        )

    def get_model_prediction(self, image_path, auth_key):
        """
        Fetches model predictions for a given image.

        Parameters:
        -----------
        image_path : str
            The path to the image for which predictions are to be made.
        auth_key : str
            The authentication key for authorizing the prediction request.

        Returns:
        --------
        tuple:
            A tuple consisting of (result, error, message) with the model's predictions.

        Example:
        --------
        >>> result, error, message = model_prediction.get_model_prediction("/path/to/image.jpg", "auth123")
        >>> print(result)
        {'predictions': [{'class': 'cat', 'confidence': 0.95}, ...]}
        """
        url = f"/v1/model_prediction/deployment/{self.deployment_id}/predict"
        files = {"image": open(image_path, "rb")}
        data = {"authKey": auth_key}
        headers = {"Authorization": f"Bearer {self.rpc.AUTH_TOKEN.bearer_token}"}

        resp = self.rpc.post(url, headers=headers, data=data, files=files)
        return self._handle_response(
            resp,
            "Model prediction fetched successfully",
            "An error occurred while fetching the model prediction.",
        )

    def get_model_test(self, model_train_id, image_path):
        """
        Tests a trained model with a given image.

        Parameters:
        -----------
        model_train_id : str
            The ID of the trained model to test.
        image_path : str
            The path to the image for testing the model.

        Returns:
        --------
        tuple:
            A tuple consisting of (result, error, message) with the test results.

        Example:
        --------
        >>> result, error, message = model_prediction.get_model_test("model123", "/path/to/test_image.jpg")
        >>> print(result)
        {'test_result': 'success', 'confidence': 0.85}
        """
        url = f"/v1/model_prediction/model_test/{model_train_id}?projectId={self.project_id}"
        files = {"image": open(image_path, "rb")}
        resp = self.rpc.post(url, files=files)
        return self._handle_response(
            resp, "Model test successfully", "An error occured while testing the model."
        )
