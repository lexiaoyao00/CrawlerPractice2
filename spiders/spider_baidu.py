from common import *

class BaiDu(MySpider):
    _referer = "https://www.baidu.com/"

    def __init__(self):
        super().__init__()

    def start_crawling(self, terminate_event):
        print("BaiDu start_crawling")

        html = self.crawler.send_request(BaiDu._referer)
        # print(html)
        soup = self.crawler.parse(html)

        rules = {
            'links': Rule('a.mnav','href'),
            'imgs' : Rule('img','src')
        }

        data = self.crawler.extract_data(soup, rules)
        print(data)

        # downloader = Downloader(threads=10)
        # downloader.download_files(data['imgs'], "downloads")
