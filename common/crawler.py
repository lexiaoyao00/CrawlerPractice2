import requests
from random import choice
from bs4 import BeautifulSoup
from typing import List,Dict
from tenacity import retry, stop_after_attempt, wait_exponential


USER_AGENTS = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
    ]

PROXIES = None

class Rule:
    """selector(必选)：CSS选择器,用于选择要提取的元素。
       attribute(可选): 如果提供了该键,则提取元素的指定属性值,而不是文本内容。
    """
    def __init__(self, selector:str, attribute:str|None=None):
        self.selector = selector
        self.attribute = attribute

class Crawler:
    max_retries = 3 #最大重试次数 
    retry_backoff = 2 #重试间隔的指数增长因子

    def __init__(self, user_agents=None, proxies=None):
        self.user_agents = user_agents or []
        self.proxies = proxies or []
        self.session = requests.Session()

    def get_headers(self):
        headers = {
            'User-Agent': choice(self.user_agents) if self.user_agents else 'Mozilla/5.0',
            'Accept-Language': 'en-US,en;q=0.5',
        }
        return headers

    def get_proxy(self):
        proxy = choice(self.proxies) if self.proxies else None
        return {'http': proxy, 'https': proxy}

    # @retry(stop=stop_after_attempt(max_retries), wait=wait_exponential(multiplier=retry_backoff))
    # def send_request(self, url, method='GET', data=None, headers=None, proxies=None):
    #     headers = headers or self.get_headers()
    #     proxies = proxies or self.get_proxy()
    #     try:
    #         response = requests.request(method, url, headers=headers, data=data, proxies=proxies, timeout=10)
    #         response.raise_for_status()
    #         return response.text
    #     except requests.exceptions.RequestException as e:
    #         print(f'Error: {e}')
    #         raise e
    @retry(stop=stop_after_attempt(max_retries), wait=wait_exponential(multiplier=retry_backoff))
    def send_request(self, url, method='GET', data=None, headers=None, proxies=None):
        headers = headers or self.get_headers()
        proxies = proxies or self.get_proxy()
        try:
            response = self.session.request(method, url, headers=headers, data=data, proxies=proxies, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print(f'Error: {e}')
            raise e

    def parse(self, html, parser='html.parser'):
        soup = BeautifulSoup(html, parser)
        return soup

    def extract_data(self, soup:BeautifulSoup, rules:Dict[str,Rule]):
        """根据rule，从soup提取数据

        Args:
            soup (BeautifulSoup): 页面的BeautifulSoup解析，可以使用parse函数返回值
            rules (Dict[str,Rule]): 提取规则，举例：
                    rules = {
                    'title': {'selector': 'h1'},
                    'paragraphs': {'selector': 'p'},
                    'links': {'selector': 'a', 'attribute': 'href'},
                    'images': {'selector': 'img', 'attribute': 'src'},
                    }
            rules的key为欲提取的内容；
            value是个Rule类型。


        Returns:
            dict: 以字典形式返回提取的内容，key对应rules的key，value为提取出来的内容
        """
        data = {}
        for key, rule in rules.items():
            elements = soup.select(rule.selector)
            if elements:
                if rule.attribute:
                    data[key] = [element[rule.attribute] for element in elements]
                else:
                    data[key] = [element.get_text(strip=True) for element in elements]
            else:
                data[key] = []
        return data

# 使用示例
# if __name__ == "__main__":

#     crawler = Crawler(user_agents=USER_AGENTS,proxies = PROXIES)
#     url = 'https://www.baidu.com/'
#     html = crawler.send_request(url)
#     soup = crawler.parse(html)

#     # rules = {
#     #     'title': 'h1',
#     #     'news': 'span[class="title-content-title"]',
#     # }

#     # rules = {
#     #     'title': {'selector': 'h1'},
#     #     'news' : {'selector': 'span[class="title-content-title"]'},
#     # }

#     rules = {
#             'links': Rule('a.mnav','href'),
#         }

#     data = crawler.extract_data(soup, rules)
#     print(data)
