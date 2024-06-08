from abc import ABCMeta,abstractmethod
import multiprocessing.synchronize
from .crawler import Crawler,USER_AGENTS,PROXIES

import multiprocessing
import threading


class MySpider(object):
    __metaclass__ = ABCMeta
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(MySpider, cls).__new__(cls)
        return cls._instance
    
    def __init__(self) -> None:
        self.crawler = Crawler(USER_AGENTS,PROXIES)
        self.items = {}
    
    @abstractmethod
    def start_crawling(self,terminate_event:multiprocessing.synchronize.Event |threading.Event):
        """爬虫启动函数

        Args:
            terminate_event (_type_): 进程终止标志
        """
        pass