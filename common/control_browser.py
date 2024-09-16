from playwright.sync_api import sync_playwright

class ControlBrowser:
    def __init__(self, browser_type="chromium", headless=False):
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
        self.browser_type = browser_type
        self.headless = headless

    def launch_browser(self):
        self.playwright = sync_playwright().start()
        browser_types = {
            "chromium": self.playwright.chromium.launch,
            "firefox": self.playwright.firefox.launch,
            "webkit": self.playwright.webkit.launch,
        }
        launch_browser = browser_types.get(self.browser_type, self.playwright.chromium.launch)
        self.browser = launch_browser(headless=self.headless)
        self.context = self.browser.new_context()
        self.page = self.context.new_page()

    def close_browser(self):
        self.context.close()
        self.browser.close()
        self.playwright.stop()