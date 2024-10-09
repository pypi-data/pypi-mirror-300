import sys


class Compute:
    """
    A class to handle compute operations such as fetching instance types, managing accounts' compute resources,
    and performing CRUD operations for compute instances using an RPC service.

    Attributes
    ----------
    project_id : str
        The project ID associated with the current session.
    rpc : object
        The RPC object used to make HTTP requests.

    Parameters
    ----------
    session : object
        The session object containing the project ID and RPC client.

    Example
    -------
    >>> session = Session(project_id="12345", rpc=rpc_client)
    >>> compute = Compute(session)
    """

    def __init__(self, session):
        self.project_id = session.project_id
        self.rpc = session.rpc

    def _handle_response(self, response, success_message, failure_message):
        """
        Handle the API response and return a standardized tuple.

        Parameters
        ----------
        response : dict
            The response returned from the API call.
        success_message : str
            The message to return if the response is successful.
        failure_message : str
            The message to return if the response fails.

        Returns
        -------
        tuple
            A tuple containing (result, error, message).
            - result : dict or None
                The data if the response is successful.
            - error : str or None
                The error message if the response failed.
            - message : str
                The success or failure message.

        Example
        -------
        >>> result, error, message = self._handle_response(response, "Success!", "Failure.")
        """
        if response.get("success"):
            result = response.get("data")
            error = None
            message = success_message
        else:
            result = None
            error = response.get("message")
            message = failure_message

        return result, error, message
    
    ## TODO: rename to get_all_instance_types
    def get_all_instance_type(self):
        """
        Fetch a list of all instance types available for use currently.

        Returns
        -------
        tuple
            A tuple containing (result, error, message).
            - result : list or None
                A list of instance types if the request is successful.
            - error : str or None
                The error message if the request fails.
            - message : str
                The success or failure message.

        Example
        -------
        >>> result, error, message = compute.get_all_instance_type()
        """
        path = f"/v1/scaling/getAllInstancesType"
        resp = self.rpc.get(path=path)

        return self._handle_response(
            resp, "Instance list fetched successfully", "Could not fetch instance list"
        )

    def get_all_account_compute(self, account_number):
        """
        Fetch all compute instances associated with a specific account.

        Parameters
        ----------
        account_number : str
            The account number for which compute instances should be retrieved.

        Returns
        -------
        tuple
            A tuple containing (result, error, message).
            - result : list or None
                A list of compute instances if the request is successful.
            - error : str or None
                The error message if the request fails.
            - message : str
                The success or failure message.

        Example
        -------
        >>> result, error, message = compute.get_all_account_compute("123456")
        """
        path = f"/v1/scaling/getAllAccountCompute/{account_number}"
        resp = self.rpc.get(path=path)

        return self._handle_response(
            resp,
            f"Instance list fetched successfully for the account number: {account_number}",
            f"Could not fetch instance list for the account number: {account_number}",
        )

    def get_threshold_details(self, account_number, compute_alias):
        """
        Fetch threshold details for a specific compute instance.

        Parameters
        ----------
        account_number : str
            The account number associated with the compute instance.
        compute_alias : str
            The alias for the compute instance.

        Returns
        -------
        tuple
            A tuple containing (result, error, message).
            - result : dict or None
                The threshold details if the request is successful.
            - error : str or None
                The error message if the request fails.
            - message : str
                The success or failure message.

        Example
        -------
        >>> result, error, message = compute.get_threshold_details("123456", "compute-1")
        """
        path = f"/v1/scaling/get_threshold_details/{account_number}/{compute_alias}"
        resp = self.rpc.get(path=path)

        return self._handle_response(
            resp,
            "Instance threshold detailed fetched successfully",
            "Could not fetch instance threshold detailed",
        )

    def add_account_compute(
        self,
        account_number,
        compute_alias,
        user_id,
        service_provider,
        instance_type,
        shutdown_time,
        launch_duration,
        lease_type="",
    ):
        """
        Add a compute instance to a specific account.

        Parameters
        ----------
        account_number : str
            The account number for which the compute instance will be added.
        compute_alias : str
            The alias for the new compute instance.
        user_id : str
            The user ID of the account owner.
        service_provider : str
            The name of the cloud service provider.
        instance_type : str
            The type of compute instance (e.g., "t2.micro").
        shutdown_time : str
            The time at which the instance should shut down.
        launch_duration : str
            The total duration for which the instance should run.
        lease_type : str, optional
            The lease type for the instance (default is an empty string).

        Returns
        -------
        tuple
            A tuple containing (result, error, message).
            - result : dict or None
                The details of the newly added compute instance if the request is successful.
            - error : str or None
                The error message if the request fails.
            - message : str
                The success or failure message.

        Example
        -------
        >>> result, error, message = compute.add_account_compute(
        >>>     "123456", "compute-1", "user123", "AWS", "t2.micro", "18:00", "24 hours"
        >>> )
        """

        path = f"/v1/scaling/addAccountCompute"
        headers = {"Content-Type": "application/json"}
        body = {
            "accountNumber": account_number,
            "alias": compute_alias,
            "projectID": self.project_id,
            "userID": user_id,
            "serviceProvider": service_provider,
            "instanceType": instance_type,
            "shutDownTime": shutdown_time,
            "leaseType": lease_type,
            "launchDuration": launch_duration,
        }
        resp = self.rpc.post(path=path, headers=headers, payload=body)

        return self._handle_response(
            resp,
            f"Compute added successfully for the account number: {account_number}",
            f"Could not add compute for the account number: {account_number}",
        )

    def update_account_compute(
        self, account_number, compute_alias, launch_duration, shutdown_threshold
    ):
        """
        Update the configuration of an existing compute instance.

        Parameters
        ----------
        account_number : str
            The account number associated with the compute instance.
        compute_alias : str
            The alias of the compute instance to be updated.
        launch_duration : str
            The new launch duration for the compute instance.
        shutdown_threshold : str
            The new shutdown threshold for the compute instance.

        Returns
        -------
        tuple
            A tuple containing (result, error, message).
            - result : dict or None
                The details of the updated compute instance if the request is successful.
            - error : str or None
                The error message if the request fails.
            - message : str
                The success or failure message.

        Example
        -------
        >>> result, error, message = compute.update_account_compute("123456", "compute-1", "12 hours", "17:00")
        """

        path = f"/v1/scaling/updateAccountCompute"
        headers = {"Content-Type": "application/json"}
        body = {
            "accountNumber": account_number,
            "computeAlias": compute_alias,
            "launchDuration": launch_duration,
            "shutDownTime": shutdown_threshold,
        }

        resp = self.rpc.put(path=path, headers=headers, payload=body)

        return self._handle_response(
            resp,
            f"Successfully updated the given compute",
            "Error updating the given compute",
        )

    def delete_account_compute(
        self,
        account_number,
        compute_alias,
    ):
        """
        Delete a compute instance associated with a specific account.

        Parameters
        ----------
        account_number : str
            The account number associated with the compute instance.
        compute_alias : str
            The alias of the compute instance to be deleted.

        Returns
        -------
        tuple
            A tuple containing (result, error, message).
            - result : dict or None
                The details of the deleted compute instance if the request is successful.
            - error : str or None
                The error message if the request fails.
            - message : str
                The success or failure message.

        Example
        -------
        >>> result, error, message = compute.delete_account_compute("123456", "compute-1")
        """

        path = f"/v1/scaling/deleteAccountCompute/{account_number}/{compute_alias}"
        headers = {"Content-Type": "application/json"}
        resp = self.rpc.put(path=path, headers=headers)

        return self._handle_response(
            resp,
            f"Successfully deleted the given compute",
            "Error deleting the given compute",
        )
