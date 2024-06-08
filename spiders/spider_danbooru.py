from common import *

class Danbooru(MySpider):
    _ORIGIN ='https://danbooru.donmai.us'
    _POPULAR = 'https://danbooru.donmai.us/explore/posts/popular'
    _GALLERY_RULES = {
            'pre_imgs' : Rule('img.post-preview-image','src'),
            'post_hrefs' : Rule('a.post-preview-link','href'),
        }

    _POST_RULES = {
        'original_img': Rule('li#post-option-view-original a.image-view-original-link','href'),
        'parent_posts_url' : Rule('div.notice a[rel="nofollow"]','href'),
        'artist_tag_list': Rule('ul.artist-tag-list a.search-tag'),
        'copyright_tag_list': Rule('ul.copyright-tag-list a.search-tag'),
        'character_tag_list': Rule('ul.character-tag-list a.search-tag'),
        'general_tag_list': Rule('ul.general-tag-list a.search-tag'),
        'meta_tag_list': Rule('ul.meta-tag-list a.search-tag'),
        'post_information': Rule('section#post-information ul li'),
    }
    def __init__(self):
        super().__init__()
    

    def organize_post_tags(self,artist_tag_list, 
                           copyright_tag_list, 
                           character_tag_list, 
                           general_tag_list, 
                           meta_tag_list, 
                           blacklist_tag_list:list|None=None):
        tags = artist_tag_list + copyright_tag_list + character_tag_list + general_tag_list + meta_tag_list
        if blacklist_tag_list:
            tags = [tag for tag in tags if tag not in blacklist_tag_list]

        return tags



    def post_parse(self,post_url):
        html = self.crawler.send_request(post_url)

        data = self.crawler.extract_data(self.crawler.parse(html), Danbooru._POST_RULES)
        res = {}

        original_img = data['original_img'][0]
        res.update({'original_img': original_img})

        parent_posts_url = Danbooru._ORIGIN +  data['parent_posts_url'][0]
        res.update({'parent_posts_url': parent_posts_url})

        post_tags = self.organize_post_tags(data['artist_tag_list'],
                                            data['copyright_tag_list'],
                                            data['character_tag_list'],
                                            data['general_tag_list'],
                                            data['meta_tag_list']
                                            )
        res.update({'post_tags': post_tags})

        # print(data['post_information'])
        post_information = '\n'.join(data['post_information'])
        res.update({'post_information' : post_information})

        return res




    def start_crawling(self, terminate_event):
        print("Danbooru start_crawling")

        test_post_url = 'https://danbooru.donmai.us/posts/7269895'
        data = self.post_parse(test_post_url)
        # print(data['post_tags'])
        # print(data['parent_posts_url'])
        # print(data['original_img'])
        print(data['post_information'])

        # downloader = Downloader(threads=10)
        # downloader.download_files(data['pre_imgs'], "downloads")