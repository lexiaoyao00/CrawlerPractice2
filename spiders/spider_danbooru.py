from common import *


class PostInfo():
    def __init__(self):
        self.name = ''
        self.original_img_url:str = ''
        self.parent_posts_url:str = ''
        self.artists = []
        self.copyright = []
        self.tags = []
        self.img_information = []

    def image_naming(self):
        if self.img_information ==[]:
            return ''
        else:
            name_obj = re.search(r'\d+',self.img_information[0])
            if name_obj:
                name = name_obj.group()
            else:
                name = self.original_img_url.rsplit('/',1)[1].rsplit('.',1)[0]

            ext_obj = re.search(r'.(jpg|jpeg|png|gif|bmp)',self.img_information[3])
            if ext_obj:
                ext = ext_obj.group()
            else:
                ext = '.jpg'
                
            return name+ext


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

        self.config = ConfigParser('spiders_config.yaml','yaml').config_data['danbooru']
    
    def get_blacklist(self):
        black_list = self.config['blacklist']
        return black_list

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
        if post_url is None or post_url == '':
            return None

        html = self.crawler.send_request(post_url)

        data = self.crawler.extract_data(self.crawler.parse(html), Danbooru._POST_RULES)
        post_info = PostInfo()

        try:
            original_img = data['original_img'][0]
        except :
            # print('当前帖子已经显示原画')
            original_img = self.crawler.extract_data(self.crawler.parse(html), {'original_img':Rule('picture source','srcset')})['original_img'][0]
        finally:
            post_info.original_img_url =  original_img

        try:
            parent_posts_url = Danbooru._ORIGIN +  data['parent_posts_url'][0]
        except :
            # print('this post has no parent posts')
            parent_posts_url = None
        finally:
            post_info.parent_posts_url =  parent_posts_url


        post_info.artists = data['artist_tag_list']
        post_info.copyright = data['copyright_tag_list']
        
        #TODO:过滤黑名单内容
        post_tags = self.merge_lists(data['character_tag_list'],
                                     data['general_tag_list'],
                                     data['meta_tag_list'],
                                     blacklist_tag_list=self.get_blacklist())
        post_info.tags = post_tags

        post_info.img_information = data['img_information']
        post_info.name = post_info.image_naming()

        print('解析完毕:' + post_url)
        return post_info




    def start_crawling(self, terminate_event):
        print("Danbooru start_crawling")

        test_post_url = 'https://danbooru.donmai.us/posts/7269895'
        data = self.post_parse(test_post_url)
        print(data)

        # downloader = Downloader(threads=10)
        # downloader.download_files(data['pre_imgs'], "downloads")