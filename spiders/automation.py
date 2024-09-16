from common import ControlBrowser,SingletonMeta


class Automation(metaclass=SingletonMeta):

    def __init__(self):
        self.browser_driver = ControlBrowser()


    def SignIn(self, **kwargs):
        pass