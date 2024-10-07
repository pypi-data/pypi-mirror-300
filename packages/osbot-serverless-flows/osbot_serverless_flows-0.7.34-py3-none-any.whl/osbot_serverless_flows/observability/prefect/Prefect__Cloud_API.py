from osbot_utils.utils.Lists                                        import list_index_by
from osbot_utils.utils.Misc                                         import list_set
from osbot_serverless_flows.observability.prefect.Prefect__Rest_API import Prefect__Rest_API
from osbot_utils.base_classes.Type_Safe                             import Type_Safe


class Prefect__Cloud_API(Type_Safe):
    prefect_rest_api = Prefect__Rest_API()


    def flows(self, limit=5):
        return self.prefect_rest_api.filter(target='flows', limit=limit).get('data') or []

    def flows_ids(self, limit=5):                                       # todo: see if there is a way to get these IDs directly via a GraphQL query
        flows = self.flows(limit=limit)
        return list_set(list_index_by(values=flows, index_by='id'))

    def flow(self, flow_id):
        return self.prefect_rest_api.read(target='flows', target_id=flow_id).get('data') or {}
