import requests
from osbot_utils.utils.Http             import url_join_safe
from osbot_utils.utils.Env              import get_env
from osbot_utils.base_classes.Type_Safe import Type_Safe
from osbot_utils.utils.Status           import status_ok, status_error

ENV_NAME__PREFECT_CLOUD__API_KEY      = 'PREFECT_CLOUD__API_KEY'
ENV_NAME__PREFECT_CLOUD__ACCOUNT_ID   = 'PREFECT_CLOUD__ACCOUNT_ID'
ENV_NAME__PREFECT_CLOUD__WORKSPACE_ID = 'PREFECT_CLOUD__WORKSPACE_ID'

class Prefect__Rest_API(Type_Safe):

    # raw request methods
    def api_key(self):
        return get_env(ENV_NAME__PREFECT_CLOUD__API_KEY)

    def account_id(self):
        return get_env(ENV_NAME__PREFECT_CLOUD__ACCOUNT_ID)

    def workspace_id(self):
        return get_env(ENV_NAME__PREFECT_CLOUD__WORKSPACE_ID)

    def prefect_api_url(self):
        return f"https://api.prefect.cloud/api/accounts/{self.account_id()}/workspaces/{self.workspace_id()}/"

    def get_headers(self):
        return {"Authorization": f"Bearer {self.api_key()}"}                            # Create headers dictionary including authorization token

    def requests__for_method(self, method, path, data=None):
        headers  = self.get_headers()

        endpoint = url_join_safe(self.prefect_api_url(), path)                          # Construct the full endpoint URL by joining the base URL with the path

        if method == requests.get:                                                      # For GET requests, pass data as query parameters
            response = method(endpoint, headers=headers, params=data)
        elif method == requests.head:                                                   # For HEAD requests, no payload or parameters are needed
            response = method(endpoint, headers=headers)
        elif method == requests.post:                                                   # For POST and other requests, pass data as JSON in the request body
            response = method(endpoint, headers=headers, json=data)
        else:
            return status_error("Unsupported request method")                           # Return an error if the method is not supported

        status_code = response.status_code                                              # Handle the response and return an appropriate result
        if status_code == 200:
            if method == requests.head:                                                 # For HEAD requests, return the headers as the response data
                return status_ok(data=response.headers)
            return status_ok(data=response.json())                                      # For other successful requests, return the JSON data

        return status_error(message=f"{method.__name__.upper()} request to {path}, failed with status {status_code}", error=response.text) # For failed requests, return an error message with status and response text

    def requests__get(self, path, params=None):                                         # Wrapper for executing GET requests
        return self.requests__for_method(requests.get, path, data=params)

    def requests__post(self, path, data):                                               # Wrapper for executing POST requests
        return self.requests__for_method(requests.post, path, data=data)

    def requests__head(self, path):                                                     # Wrapper for executing HEAD requests
        return self.requests__for_method(requests.head, path)

    # request helpers

    def read(self, target, target_id):
        path = f'/{target}/{target_id}'
        return self.requests__get(path)

    def filter(self, target, limit=5):          # todo: add support for fetching all items
        path = f'/{target}/filter'
        data = { "sort" : "CREATED_DESC",
                 "limit": limit         }
        return self.requests__post(path, data)