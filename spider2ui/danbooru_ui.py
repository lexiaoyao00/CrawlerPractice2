from UI import Ui_DanbooruPost
from spiders import Danbooru,PostInfo
from instance_manage import instance_danbooru
from instance_manage import instanceui_danbooru_post
from common import Downloader


###  Post UI  ###
post_info:PostInfo = None

def slot_btn_getinfo():
        url = instanceui_danbooru_post.LE_url.text()

        #爬取post信息
        post_info = instance_danbooru.post_parse(url)
        # original_img,parent_posts_url,post_artists,post_copyright,post_tags,img_information

        instanceui_danbooru_post.LE_artist.setText(','.join(post_info.artists))
        instanceui_danbooru_post.LE_cop.setText(','.join(post_info.copyright))
        instanceui_danbooru_post.TE_tags.setText(','.join(post_info.tags))
        instanceui_danbooru_post.TE_Info.setText('\n'.join(post_info.img_information))

def slot_btn_download():
        #TODO
        pass