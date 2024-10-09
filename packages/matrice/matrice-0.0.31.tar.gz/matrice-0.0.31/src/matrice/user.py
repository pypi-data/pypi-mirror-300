import sys
from matrice.rpc import RPC

class User:
    """
    A class to represent the user and manage user-related API operations.

    Attributes:
    ----------
    rpc : RPC
        The RPC session object to perform HTTP requests.

    Methods:
    ----------
    handle_response(response, success_message, failure_message)
        Handles the API response and returns a standardized tuple.

    get_account_subscription(account_number)
        Fetches account subscription details for a given account number.

    list_invites()
        Fetches the list of invites.

    list_project_invites(project_id)
        Fetches the list of project invites for a given project ID.

    list_collaborators(project_id)
        Fetches the list of collaborators for a specific project.

    invite_user(project_id, user_id, project_name, permissions)
        Invites a user to a project.

    accept_invite(invite_id)
        Accepts an invite to a project.

    update_permissions(project_id, collaborator_id, permissions)
        Updates the permissions of a collaborator in a project.

    delete_invite(project_id)
        Deletes a project invite.

    delete_collaborator(project_id, collaborator_id)
        Removes a collaborator from a project.
    """

    def __init__(self, session):
        """
        Initialize User object with an RPC session.

        Parameters:
        ----------
        session : object
            The session object containing the RPC instance.

        Example:
        ----------
        >>> user = User(session)
        """
        self.rpc = session.rpc

    def handle_response(self, response, success_message, failure_message):
        """
        Handles the API response and returns a standardized tuple.

        Parameters:
        ----------
        response : dict
            The API response to handle.
        success_message : str
            The message to return if the request is successful.
        failure_message : str
            The message to return if the request fails.

        Returns:
        ----------
        tuple : (result, error, message)
            A tuple containing:
            - result : The data if the request is successful, otherwise None.
            - error : The error message if the request fails, otherwise None.
            - message : Success or failure message.

        Example:
        ----------
        >>> result, error, message = self.handle_response(response, "Success", "Failure")
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

    def get_account_subscription(self, account_number):
        """
        Fetches account subscription details.

        Parameters:
        ----------
        account_number : str
            The account number to fetch subscription details for.

        Returns:
        ----------
        tuple : (result, error, message)
            The subscription details or error message.

        Example:
        ----------
        >>> result, error, message = self.get_account_subscription("12345")
        """
        path = f"/v1/user/get_account_subscription/{account_number}"
        resp = self.rpc.get(path=path)

        return self.handle_response(
            resp,
            "Account subscription details fetched successfully",
            "Could not fetch account subscription details",
        )

    def list_invites(self):
        """
        Fetches the list of invites.

        Returns:
        ----------
        tuple : (result, error, message)
            The list of invites or error message.

        Example:
        ----------
        >>> result, error, message = self.list_invites()
        """
        path = "/v2/user/project/invite"
        resp = self.rpc.get(path=path)

        return self.handle_response(
            resp, "Invites list fetched successfully", "Could not fetch invite list"
        )

    def list_project_invites(self, project_id):
        """
        Fetches the list of project invites for a specific project.

        Parameters:
        ----------
        project_id : str
            The project ID for which to fetch invites.

        Returns:
        ----------
        tuple : (result, error, message)
            The list of project invites or error message.

        Example:
        ----------
        >>> result, error, message = self.list_project_invites("project123")
        """
        path = f"/v2/user/project/{project_id}/invites?projectId={project_id}"
        resp = self.rpc.get(path=path)

        return self.handle_response(
            resp,
            "Project invites list fetched successfully",
            "Could not fetch project invite list",
        )

    def list_collaborators(self, project_id):
        """
        Fetches the list of collaborators for a specific project.

        Parameters:
        ----------
        project_id : str
            The project ID for which to fetch collaborators.

        Returns:
        ----------
        tuple : (result, error, message)
            The list of collaborators or error message.

        Example:
        ----------
        >>> result, error, message = self.list_collaborators("project123")
        """
        path = f"/v2/user/project/{project_id}/collaborators?projectId={project_id}"
        resp = self.rpc.get(path=path)

        return self.handle_response(
            resp, "Collaborators fetched successfully", "Could not fetch collaborators"
        )

    def invite_user(self, project_id, user_id, project_name, permissions):
        """
        Invites a user to a project.

        Parameters:
        ----------
        project_id : str
            The project ID.
        user_id : str
            The ID of the user to invite.
        project_name : str
            The name of the project.
        permissions : list
            A list of permissions to assign to the user.

        Returns:
        ----------
        tuple : (result, error, message)
            The invite response or error message.

        Example:
        ----------
        >>> result, error, message = self.invite_user("project123", "user456", "Test Project", ["admin"])
        """
        path = f"/v2/user/project/invite?projectId={project_id}"
        headers = {"Content-Type": "application/json"}
        body = {
            "_idProject": project_id,
            "_idUser": user_id,
            "projectName": project_name,
            "permissions": permissions,
        }
        resp = self.rpc.post(path=path, headers=headers, payload=body)

        return self.handle_response(
            resp,
            "User invited to the project successfully",
            "Could not invite user to the project",
        )

    def accept_invite(self, invite_id):
        """
        Accepts an invite to a project.

        Parameters:
        ----------
        invite_id : str
            The ID of the invite.

        Returns:
        ----------
        tuple : (result, error, message)
            The invite acceptance response or error message.

        Example:
        ----------
        >>> result, error, message = self.accept_invite("invite789")
        """
        path = f"/v2/user/project/invite/{invite_id}/accept"
        resp = self.rpc.post(path=path)

        return self.handle_response(
            resp, "Invite accepted successfully", "Could not accept invite"
        )

    def update_permissions(self, project_id, collaborator_id, permissions):
        """
        Updates the permissions of a collaborator in a project.

        Parameters:
        ----------
        project_id : str
            The project ID.
        collaborator_id : str
            The ID of the collaborator.
        permissions : list
            A list containing the updated permissions.

        Returns:
        ----------
        tuple : (result, error, message)
            The permission update response or error message.

        Example:
        ----------
        >>> permissions = ["v1", True, True, False, True, False, True, False]
        >>> result, error, message = self.update_permissions("project123", "collab789", permissions)
        """
        path = f"/v2/user/project/{project_id}/collaborators/{collaborator_id}?projectId={project_id}"
        headers = {"Content-Type": "application/json"}
        body = {
            "version": permissions[0],
            "isProjectAdmin": permissions[1],
            "datasetsService": permissions[2],
            "modelsService": permissions[3],
            "annotationService": permissions[4],
            "byomService": permissions[5],
            "deploymentService": permissions[6],
            "inferenceService": permissions[7],
        }
        resp = self.rpc.put(path=path, headers=headers, payload=body)

        return self.handle_response(
            resp,
            "Collaborator permissions updated successfully",
            "Could not update collaborator permissions",
        )

    def delete_invite(self, project_id):
        """
        Deletes a project invite.

        Parameters:
        ----------
        project_id : str
            The project ID associated with the invite.

        Returns:
        ----------
        tuple : (result, error, message)
            The invite deletion response or error message.

        Example:
        ----------
        >>> result, error, message = self.delete_invite("project123")
        """
        path = f"/v2/user/project/invite/{project_id}"
        resp = self.rpc.delete(path=path)

        return self.handle_response(
            resp, "Invite deleted successfully", "Could not delete invite"
        )

    def delete_collaborator(self, project_id, collaborator_id):
        """
        Removes a collaborator from a project.

        Parameters:
        ----------
        project_id : str
            The project ID.
        collaborator_id : str
            The ID of the collaborator to remove.

        Returns:
        ----------
        tuple : (result, error, message)
            The collaborator removal response or error message.

        Example:
        ----------
        >>> result, error, message = self.delete_collaborator("project123", "collab789")
        """
        path = f"/v2/user/project/{project_id}/delete-collaborator/{collaborator_id}"
        resp = self.rpc.delete(path=path)

        return self.handle_response(
            resp, "Collaborator removed successfully", "Could not remove collaborator"
        )
