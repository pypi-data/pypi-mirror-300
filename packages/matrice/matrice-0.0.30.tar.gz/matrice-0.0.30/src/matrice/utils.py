import traceback
from matrice.rpc import RPC

def log_error(self, filename, function_name, error_message):
    """ "This function logs error to be-system."""
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
        r = RPC()
        r.post(url=error_logging_route, data=log_err)
    except Exception as e:
        print(f"Failed to log error: {e}")
    print(f"An exception occurred. Logging the exception information: {log_err}")

def handle_response(response, success_message, failure_message):

    if response.get("success"):
        result = response.get("data")
        error = None
        message = success_message
    else:
        result = None
        error = response.get("message")
        message = failure_message

    return result, error, message