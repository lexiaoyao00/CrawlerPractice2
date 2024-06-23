from common import *
from logger import my_logger


class GalleryInfo():
    _POPULAR = 'https://danbooru.donmai.us/explore/posts/popular'
    _HOT = 'https://danbooru.donmai.us/posts?tags=order:rank'

    def __init__(self):
        self.pre_imgs = []
        self.post_hrefs = []
        self.tail_page:str = ""

class PostInfo():
    def __init__(self):
        self.name = ''
        self.post_preview_src:str = ''
        self.original_post_url:str = ''
        self.parent_posts_url:str = ''
        self.artists = []
        self.copyright = []
        self.tags = []
        self.post_information = []

    def post_naming(self):
        if self.post_information ==[] or self.original_post_url == '':
            raise '该函数要在提取到帖子信息后使用'
        else:
            name_obj = re.search(r'\d+',self.post_information[0])
            if name_obj:
                name = name_obj.group()
            else:
                name = self.original_post_url.rsplit('/',1)[1].rsplit('.',1)[0]

            # ext_obj = re.search(r' .(jpg|jpeg|png|gif|bmp|mp4|zip|)',self.post_information[3])
            # ext_obj = re.search(r' \..{3}',self.post_information[3])
            ext_obj = re.search(r'\.\w{3,4}$',self.original_post_url)
            if ext_obj:
                ext = ext_obj.group()
            else:
                ext = '.jpg'
            
            my_logger.debug(name + ext)

            return name+ext


class Danbooru(MySpider):
    _ORIGIN ='https://danbooru.donmai.us'

    _GALLERY_RULES = {
            'pre_imgs' : Rule('img.post-preview-image','src'),
            'post_hrefs' : Rule('a.post-preview-link','href'),
            'tail_page' : Rule('span.paginator-ellipsis + a.paginator-page')
        }

    _POST_RULES = {
        'post_preview': Rule('#image.fit-width','src'),
        # 'original_post': Rule('li#post-option-view-original a.image-view-original-link','href'),# 最常见的帖子URL：缩小显示图片
        'original_download': Rule('li#post-option-download a','href'),
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
            dict: 返回字典，包含 original_download,parent_posts_url,post_artists,post_copyright,post_tags,post_information
        """
        if post_url is None or post_url == '':
            return None

        html = self.crawler.send_request(post_url)

        data = self.crawler.extract_data(self.crawler.parse(html), Danbooru._POST_RULES)
        post_info = PostInfo()

        if data['post_preview']:
            post_pre_url = data['post_preview'][0]
    
        post_info.post_preview_src = post_pre_url


        if  data['original_download']:
            original_url = data['original_download'][0].split(r'?')[0]
            my_logger.debug('下载网址：' + original_url)
        else:
            my_logger.error('下载链接未获取到，请检查'+post_url)
            original_url=None
        post_info.original_post_url = original_url

        try:
            parent_posts_url = Danbooru._ORIGIN +  data['parent_posts_url'][0]
        except :
            parent_posts_url = None
        finally:
            post_info.parent_posts_url =  parent_posts_url


        post_info.artists = data['artist_tag_list']
        post_info.copyright = data['copyright_tag_list']
        
        post_tags = self.merge_lists(data['character_tag_list'],
                                     data['general_tag_list'],
                                     data['meta_tag_list'],
                                     blacklist_tag_list=self.get_blacklist())
        post_info.tags = post_tags

        post_info.post_information = data['post_information']
        post_info.name = post_info.post_naming()

        # print('解析完毕:' + post_url)
        my_logger.info('解析完毕:' + post_url)
        return post_info

    def gallery_parse(self,gallery_url:str):
        if gallery_url is None or gallery_url == '':
            return None
        
        html = self.crawler.send_request(gallery_url)

        data = self.crawler.extract_data(self.crawler.parse(html), Danbooru._GALLERY_RULES)
        gallery_info = GalleryInfo()


        gallery_info.pre_imgs = data['pre_imgs']
        
        post_hrefs = [ Danbooru._ORIGIN+href for href in data['post_hrefs']]
        gallery_info.post_hrefs =  post_hrefs

        if data['tail_page']:
            gallery_info.tail_page = data['tail_page'][0]

        return gallery_info


    def start_crawling(self, terminate_event):
        # print("Danbooru start_crawling")

        test_post_url = 'https://danbooru.donmai.us/posts/7269895'
        data = self.post_parse(test_post_url)
        # print(data)

        # downloader = Downloader(threads=10)
        # downloader.download_files(data['pre_imgs'], "downloads")