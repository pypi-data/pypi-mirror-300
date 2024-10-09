from osbot_fast_api.api.Fast_API import Fast_API

from osbot_serverless_flows.fast_api.routes.Routes__Debug import Routes__Debug
from osbot_serverless_flows.fast_api.routes.Routes__Info import Routes__Info
from osbot_serverless_flows.fast_api.routes.Routes__Browser import Routes__Browser


class Fast_API__Serverless_Flows(Fast_API):


    def setup(self):
        super().setup()
        return self


    def setup_routes(self):
        self.add_routes(Routes__Info)
        self.add_routes(Routes__Debug)
        self.add_routes(Routes__Browser)



    # todo: BUG: chrome is not being picked up from the install folder from the docker image
    #       the code below on start up was not consistently installing ok chrome (in some cases the processes would not unzip all the files, I think this is because of the LWA and Lambdas boot timeout)
    # def ensure_browser_is_installed(self):
    #     from osbot_serverless_flows.playwright.Playwright__Serverless import Playwright__Serverless
    #     playwright_browser = Playwright__Serverless()
    #     result = playwright_browser.browser__install()
    #     print(f"*****************************************")
    #     print(f"*****    Chrome installed:  { result }    *****")
    #     print(f"*****************************************")