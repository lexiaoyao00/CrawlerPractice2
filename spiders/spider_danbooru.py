from common import *


class PostInfo():
    def __init__(self):
        self.original_img_url:str = ''
        self.parent_posts_url:str = ''
        self.artists = []
        self.copyright = []
        self.tags = []
        self.img_information = []


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
        'img_information': Rule('section#post-information ul li'),
    }
    def __init__(self):
        super().__init__()
    

    def merge_lists(self, *args: list, blacklist_tag_list:list|None=None ):
        result = []
        for lst in args:
            result.extend(lst)
        
        if blacklist_tag_list:
            result = [tag for tag in result if tag not in blacklist_tag_list]

        return result



    def post_parse(self,post_url:str):
        """post页面解析，主要获取 原图地址、父亲画廊地址、图像标签、图像信息

        Args:
            post_url (str): post url

        Returns:
            dict: 返回字典，包含 original_img,parent_posts_url,post_artists,post_copyright,post_tags,img_information
        """
        html = self.crawler.send_request(post_url)

        data = self.crawler.extract_data(self.crawler.parse(html), Danbooru._POST_RULES)
        post_info = PostInfo()

        original_img = data['original_img'][0]
        post_info.original_img_url =  original_img
        print('original_img get')

        try:
            parent_posts_url = Danbooru._ORIGIN +  data['parent_posts_url'][0]
        except :
            print('this post has no parent posts')
            parent_posts_url = None
        post_info.parent_posts_url =  parent_posts_url
        print('parent_posts_url get')


        post_info.artists = data['artist_tag_list']
        post_info.copyright = data['copyright_tag_list']
        
        #TODO:过滤黑名单内容
        post_tags = self.merge_lists(data['character_tag_list'],data['general_tag_list'],data['meta_tag_list'],blacklist_tag_list=None)
        post_info.tags = post_tags
        print('tags get')

        post_info.img_information = data['img_information']
        print('img_information get')


        return post_info




    def start_crawling(self, terminate_event):
        print("Danbooru start_crawling")

        test_post_url = 'https://danbooru.donmai.us/posts/7269895'
        data = self.post_parse(test_post_url)
        print(data)

        # downloader = Downloader(threads=10)
        # downloader.download_files(data['pre_imgs'], "downloads")