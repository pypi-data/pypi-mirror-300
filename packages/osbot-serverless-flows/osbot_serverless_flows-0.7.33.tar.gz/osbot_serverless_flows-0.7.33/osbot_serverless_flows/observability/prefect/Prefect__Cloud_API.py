from osbot_serverless_flows.observability.prefect.Prefect__Rest_API import Prefect__Rest_API
from osbot_utils.base_classes.Type_Safe import Type_Safe


class Prefect__Cloud_API(Type_Safe):
    prefect_rest_api = Prefect__Rest_API()


    def flows(self, limit=5):
        return self.prefect_rest_api.filter(target='flows', limit=limit)