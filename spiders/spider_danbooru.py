from common import *

class Danbooru(MySpider):
    _ORIGIN ='https://danbooru.donmai.us/'
    _POPULAR = 'https://danbooru.donmai.us/explore/posts/popular'
    _RULES = {
            'pre_imgs' : Rule('img.post-preview-image','src')
        }

    def __init__(self):
        super().__init__()

    def start_crawling(self, terminate_event):
        print("Danbooru start_crawling")

        html = self.crawler.send_request(Danbooru._POPULAR)

        data = self.crawler.extract_data(self.crawler.parse(html), Danbooru._RULES)
        print(data)

        # downloader = Downloader(threads=10)
        # downloader.download_files(data['pre_imgs'], "downloads")