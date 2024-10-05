from osbot_utils.utils.Misc import bytes_to_base64

from osbot_utils.utils.Objects import obj_info

from osbot_utils.utils.Dev import pprint

from osbot_serverless_flows.playwright.Playwright__Serverless   import Playwright__Serverless
from osbot_utils.helpers.flows.decorators.task                  import task
from playwright.async_api                                       import Browser
from osbot_utils.helpers.flows.Flow                             import Flow
from osbot_utils.helpers.flows.decorators.flow                  import flow
from osbot_utils.base_classes.Type_Safe                         import Type_Safe

class Flow__Playwright__Get_Page_Screenshot(Type_Safe):             # refactor with Flow__Playwright__Get_Page_Html since 90% of the code is the same

    playwright_serverless : Playwright__Serverless
    url                   : str = 'https://httpbin.org/get'

    @task()
    def check_config(self) -> Browser:
        print('checking config')

    @task()
    async def launch_browser(self) -> Browser:
        await self.playwright_serverless.launch()
        print('launched playwright')

    @task()
    async def new_page(self) -> Browser:
        await self.playwright_serverless.new_page()

    @task()
    async def open_url(self) -> Browser:
        print(f"opening url: {self.url}")
        await self.playwright_serverless.goto(self.url)

    @task()
    async def capture_screenshot(self, flow_data: dict) -> Browser:
        screenshot_bytes = await self.playwright_serverless.page.screenshot()
        flow_data['screenshot_bytes'] = screenshot_bytes
        print(f"got screenshot_bytes with size: {len(screenshot_bytes)}")

    @task()
    def convert_to_base64(self, flow_data: dict) -> Browser:
        screenshot_bytes               = flow_data['screenshot_bytes']
        screenshot_base64              = bytes_to_base64(screenshot_bytes)
        flow_data['screenshot_base64'] = screenshot_base64
        print(f"converted to base64 with size: {len(screenshot_base64)}")

    @flow()
    async def flow(self) -> Flow:
        self.check_config()
        await self.launch_browser    ()
        await self.new_page          ()
        await self.open_url          ()
        await self.capture_screenshot()
        self.convert_to_base64       ()
        return 'all done'

    def run(self):
        with self.flow() as _:
            _.execute_flow()
            return _.data