from common import *

class Danbooru(MySpider):
    _referer ='https://danbooru.donmai.us/'
    _popular = 'https://danbooru.donmai.us/explore/posts/popular'

    def __init__(self):
        super().__init__()

    def start_crawling(self, terminate_event):
        print("Danbooru start_crawling")

        html = self.crawler.send_request(Danbooru._popular)
        # print(html)
        soup = self.crawler.parse(html)

        rules = {
            'imgs' : Rule('img.post-preview-image','src')
        }

        data = self.crawler.extract_data(soup, rules)
        print(data)

        downloader = Downloader(threads=10)
        downloader.download_files(data['imgs'], "downloads")