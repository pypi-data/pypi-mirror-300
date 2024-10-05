from osbot_fast_api.api.Fast_API_Routes import Fast_API_Routes

from osbot_serverless_flows.flows.browser_based.Flow__Playwright__Get_Page_Html import Flow__Playwright__Get_Page_Html
from osbot_serverless_flows.flows.browser_based.Flow__Playwright__Get_Page_Screenshot import \
    Flow__Playwright__Get_Page_Screenshot
from osbot_serverless_flows.playwright.Playwright__Serverless                   import Playwright__Serverless

ROUTES__EXPECTED_PATHS__BROWSER = ['/browser/install-browser' ,
                                   '/browser/url-html'        ]

class Routes__Browser(Fast_API_Routes):
    tag : str = 'browser'

    # def launch_browser(self):
    #     with sync_playwright() as p:
    #         browser = p.chromium.launch(args=["--disable-gpu", "--single-process"])
    #         return f'browser launched: {browser}'
    #
    # def new_page(self):
    #     with sync_playwright() as p:
    #         browser = p.chromium.launch(args=["--disable-gpu", "--single-process"])
    #         page   = browser.new_page()
    #         return f'new page: {page}'
    #
    # def html(self, url='https://dev.cyber-boardroom.com/config/version'):
    #     try:
    #         with sync_playwright() as p:
    #             #browser = p.chromium.launch(args=["--disable-gpu", "--single-process"])
    #             browser = p.chromium.launch(args=["--disable-gpu", "--single-process"])
    #             page    = browser.new_page()
    #             page.goto(url)
    #             html_content = page.content()
    #             return HTMLResponse(content=html_content, status_code=200)
    #     except Exception as error:
    #         return f'{error}'
    #
    # def html_2(self, url='https://dev.cyber-boardroom.com/config/version'):
    #     try:
    #         playwright  = sync_playwright().start()
    #         browser     = playwright.chromium.launch(args=["--disable-gpu", "--single-process"])
    #         page        = browser.new_page()
    #         page.goto(url)
    #         html_content = page.content()
    #         #page.screenshot(path="example.png")
    #         browser.close()
    #         playwright.stop()
    #         return html_content
    #
    #     except Exception as error:
    #         return f'{error}'
    #
    # async def html_async(self, url='https://dev.cyber-boardroom.com/config/version'):
    #     try:
    #         async with async_playwright() as p:
    #             browser = await p.chromium.launch(args=["--disable-gpu", "--single-process"])
    #             page    = await browser.new_page()
    #             await page.goto(url)
    #             html_content = await page.content()
    #             return HTMLResponse(content=html_content, status_code=200)
    #     except Exception as error:
    #         return f'{error}'

    def install_browser(self):
        playwright_browser = Playwright__Serverless()
        result             = playwright_browser.browser__install()
        return dict(status=result)

    def url_html(self, url="https://httpbin.org/get"):
        with Flow__Playwright__Get_Page_Html() as _:
            _.url = url
            result = _.run()
            return result

    def url_screenshot(self, url="https://httpbin.org/get"):
        with Flow__Playwright__Get_Page_Screenshot() as _:
            _.url = url
            screenshot_base64 = _.run().get('screenshot_base64')
            result = {'screenshot_base64': screenshot_base64}
            return result

    def setup_routes(self):
        self.add_route_get(self.url_html        )
        self.add_route_get(self.url_screenshot  )
        self.add_route_get(self.install_browser )

        # self.add_route_get(self.launch_browser)
        # self.add_route_get(self.new_page      )

        # self.add_route_get(self.html_2        )
        # self.add_route_get(self.html_async    )