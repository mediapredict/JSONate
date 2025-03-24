from django.http import Http404
from django.core.exceptions import ValidationError


class APIReqHandler:
    """
    The APIReqHandler class provides a wrapper that adds
    a message parameter to a function that returns a dictionary.
    Combine with the jsonate_response decorator to use with
    clients expecting json.

    If the view raised no errors, the message content is 'ok'.
    Http404 and validation errors return the error message to the client,
    all other exceptions are raised.

    Example:
        @jsonate_response
        def my_view(request, some_arg)
            return APIReqHandler(my_func).handle(some_arg)

    Parameters:
     - view_f (function): A function that returns a dictionary.
     - resp_ok (function, optional): A function to execute if no errors are raised.
     - resp_err (function, optional): A function to execute if errors are raised.

    Methods:
        - handle(*args, **kwargs) -- return the function with added message.
    """
    def __init__(self, view_f, resp_ok=None, resp_err=None):
        self.view_f = view_f
        self.resp_ok = resp_ok or self._resp_ok
        self.resp_err = resp_err or self._resp_error

    @staticmethod
    def _resp_ok(extra):
        extra_data = extra or {}
        return {
            "message": "ok",
            **{k: v for k, v in extra_data.items()}
        }

    @staticmethod
    def _resp_error(err):
        return {"message": f"{err.__class__.__name__}: {err}"}

    def handle(self, *args, **kwargs):
        try:
            return self.resp_ok(self.view_f(*args, **kwargs))
        except (Http404, ValidationError) as err:
            return self.resp_err(err)
        except Exception:
            raise
