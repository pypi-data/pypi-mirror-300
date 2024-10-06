import requests

from osbot_utils.utils.Env              import get_env
from osbot_utils.base_classes.Type_Safe import Type_Safe

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
        return f"https://api.prefect.cloud/api/accounts/{self.account_id()}/workspaces/{self.workspace_id()}"

    def requests_post(self, path, data):
        headers  = {"Authorization": f"Bearer {self.api_key()}"}
        endpoint = f"{self.prefect_api_url()}{path}"
        response = requests.post(endpoint, headers=headers, json=data)
        return response

    # request helpers

    def filter(self, target, limit=5):
        path = f'/{target}/filter'
        data = { "sort" : "CREATED_DESC",
                 "limit": limit         }
        return self.requests_post(path, data)