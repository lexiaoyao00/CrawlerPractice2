import os

from UI import Ui_DanbooruPost
from spiders import Danbooru,PostInfo
from instance_manage import instance_danbooru,instanceui_danbooru_post
from common import Downloader
from logger import my_logger


###  Post UI  ###
post_info:PostInfo = None

def slot_btn_getinfo_clicked():
    global post_info
    url = instanceui_danbooru_post.LE_url.text()
    #爬取post信息
    try:
        post_info = instance_danbooru.post_parse(url)
        # original_img,parent_posts_url,post_artists,post_copyright,post_tags,post_information
        if post_info is not None:
                instanceui_danbooru_post.LE_artist.setText(','.join(post_info.artists))
                instanceui_danbooru_post.LE_cop.setText(','.join(post_info.copyright))
                instanceui_danbooru_post.TE_tags.setText(','.join(post_info.tags))
                instanceui_danbooru_post.TE_Info.setText('\n'.join(post_info.post_information))
        else:
                # print('获取信息失败')
                my_logger.info('获取信息失败')
    except Exception as e:
        # print('slot_btn_getinfo_clicked error:', e)
        my_logger.error(e)

def slot_btn_download_clicked():
        global post_info

        if post_info is not None:
                media = post_info.original_post_url
                # print('test: ' + img)
                media_name = post_info.name
                directory = 'downloads'
                if not os.path.exists(directory):
                        os.makedirs(directory, exist_ok=True)

                # print('正在启用下载，请稍后。。。。。')
                my_logger.info('正在启用下载，请稍后。。。。。')
                try:
                        Downloader().download_file(media,os.path.join(directory,media_name) ,show_progress=False)
                except Exception as e:
                        # print('slot_btn_
                        # download_clicked error:', e)
                        my_logger.error(e)
                else:
                        # print(img_name + '下载完毕')
                        my_logger.info(media_name + '下载完毕')