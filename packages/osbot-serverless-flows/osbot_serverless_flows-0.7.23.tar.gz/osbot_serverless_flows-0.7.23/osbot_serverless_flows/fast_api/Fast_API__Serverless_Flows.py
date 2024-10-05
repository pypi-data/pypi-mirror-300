from osbot_fast_api.api.Fast_API import Fast_API

from osbot_serverless_flows.fast_api.routes.Routes__Debug import Routes__Debug
from osbot_serverless_flows.fast_api.routes.Routes__Info import Routes__Info
from osbot_serverless_flows.fast_api.routes.Routes__Browser import Routes__Browser


class Fast_API__Serverless_Flows(Fast_API):

    def setup_routes(self):
        self.add_routes(Routes__Info)
        self.add_routes(Routes__Debug)
        self.add_routes(Routes__Browser)