import sys



class Action:
    """
    Represents an action within the system.

    This class provides an interface to interact with a specific action identified by its `action_id`. It retrieves 
    the action's details such as type, project, user, status, creation time, and associated service from the API.

    Attributes
    ----------
    action_id : str
        The unique identifier for this action.
    action_type : str
        The type of action (retrieved from the API response).
    project_id : str
        The unique ID of the project associated with this action.
    user_id : str
        The unique ID of the user who triggered the action.
    step_code : str
        A code representing the current step of the action process.
    status : str
        The current status of the action (e.g., "pending", "completed").
    created_at : str
        The timestamp when the action was initiated.
    service_name : str
        The name of the service handling this action.

    Methods
    -------
    __init__(session, action_id)
        Initializes the Action object and fetches the action details from the API.

    get_action_details(session, action_id)
        A static method that fetches action details from the API.

    Examples
    --------
    >>> session = RPCSession()  # Assuming `RPCSession` is an existing session class
    >>> action = Action(session, "action_id_1234")
    >>> print(action.action_type)  # Output the type of action
    
    
    """

    def __init__(self, session, action_id):
        """
        Initializes the Action object and fetches the action details from the API.

        Parameters
        ----------
        session : RPCSession
            An active session object that is used to make API calls.
        action_id : str
            The unique identifier for the action whose details need to be fetched.

        Notes
        -----
        This constructor calls the `get_action_details` function to retrieve the action details, 
        which are then set as attributes of the Action object.

        If an error occurs while fetching the action details, an error message will be printed.
        """
        self.action_id = action_id
        data, error = get_action_details(session, action_id)
        if error is not None:
            print(f"An error occured while fetching action details: \n {error}")
        else:
            self.action_type = data["action"]
            self.project_id = data["_idProject"]
            self.user_id = data["_idUser"]
            self.step_code = data["stepCode"]
            self.status = data["status"]
            self.created_at = data["createdAt"]
            self.service_name = data["serviceName"]
            # TODO: Add other fields such as action_details, job_params, credit and other fields, ref - https://github.com/matrice-ai/golang-common/blob/prod/entities/action-record.go



def get_action_details(session, action_id):
    """
        Fetches action details from the API.

        Parameters
        ----------
        session : RPCSession
            An active session object used to perform API requests.
        action_id : str
            The unique identifier of the action whose details are being fetched.

        Returns
        -------
        tuple
            A tuple containing two elements:
            - A dictionary with the action details if the request is successful.
            - An error message (str) if the request fails, otherwise `None`.

        Raises
        ------
        ConnectionError
            Raised when there's a failure in communication with the API.

        Examples
        --------
        >>> session = RPCSession()
        >>> data, error = Action.get_action_details(session, "action_id_1234")
        >>> if error is None:
        >>>     print(data)
        """
    path = f"/v1/project/action/{action_id}/details"
    resp = session.rpc.get(path=path)
    if resp.get("success"):
        return resp.get("data"), None
    else:
        return resp.get("data"), resp.get("message")
