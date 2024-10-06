from osbot_serverless_flows.observability.prefect.Prefect__Rest_API import Prefect__Rest_API
from osbot_utils.base_classes.Type_Safe import Type_Safe


class Prefect__Cloud_API(Type_Safe):
    prefect_rest_api = Prefect__Rest_API()

    def make_request(self):
        path = '/flows/filter'
        data = {
            "sort": "CREATED_DESC",
            "limit": 5,
        }
        return self.prefect_rest_api.requests_post(path, data)