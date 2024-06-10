import os
from UI import Ui_DanbooruPost
from spiders import Danbooru,PostInfo
from instance_manage import instance_danbooru
from instance_manage import instanceui_danbooru_post
from common import Downloader


###  Post UI  ###
post_info:PostInfo = None

def slot_btn_getinfo_clicked():
    #TODO:一访问这个帖子就出错：https://danbooru.donmai.us/posts/7399943?q=ordfav%3Alexiaoyao
    global post_info
    url = instanceui_danbooru_post.LE_url.text()
    #爬取post信息
    try:
        post_info = instance_danbooru.post_parse(url)
        # original_img,parent_posts_url,post_artists,post_copyright,post_tags,img_information
        if post_info is not None:
                instanceui_danbooru_post.LE_artist.setText(','.join(post_info.artists))
                instanceui_danbooru_post.LE_cop.setText(','.join(post_info.copyright))
                instanceui_danbooru_post.TE_tags.setText(','.join(post_info.tags))
                instanceui_danbooru_post.TE_Info.setText('\n'.join(post_info.img_information))
        else:
                print('获取信息失败')
    except Exception as e:
        print('error:', e)

def slot_btn_download_clicked():
        global post_info

        if post_info is not None:
                img = post_info.original_img_url
                # print('test: ' + img)
                img_name = post_info.name
                directory = 'downloads'
                os.makedirs(directory, exist_ok=True)

                try:

                        Downloader().download_file(img,os.path.join(directory,img_name) ,show_progress=False)
                except Exception as e:
                        print('error:', e)
                else:
                        print(img_name + '下载完毕')