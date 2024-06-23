import os

import requests
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

from UI import Ui_DanbooruPost
from spiders import Danbooru,PostInfo,GalleryInfo
from instance_manage import instance_danbooru,instanceui_danbooru_post,instanceui_danbooru_gallery
from instance_manage import instanceInfo_danbooru_post_info,instanceInfo_danbooru_gallery_info
from common import Downloader
from logger import my_logger


post_info:PostInfo = instanceInfo_danbooru_post_info
gallery_info:GalleryInfo = instanceInfo_danbooru_gallery_info

###  Post UI  ###
def scale_image(pixmap:QPixmap, max_size):
        width = pixmap.width()
        height = pixmap.height()

        if width > max_size or height > max_size:
            if width > height:
                scaled_pixmap = pixmap.scaledToWidth(max_size)
            else:
                scaled_pixmap = pixmap.scaledToHeight(max_size)
        else:
            scaled_pixmap = pixmap

        return scaled_pixmap

def slot_danbooru_post_btn_getinfo_clicked():
    global post_info
    url = instanceui_danbooru_post.LE_url.text()
    #爬取post信息
    try:
        post_info = instance_danbooru.post_parse(url)
        if post_info is not None:
            pixmap = QPixmap()
            pixmap.loadFromData(requests.get(post_info.post_preview_src).content)
            scaled_pixmap = scale_image(pixmap,500)
            instanceui_danbooru_post.label_img_preview.setPixmap(scaled_pixmap)

            instanceui_danbooru_post.LE_artist.setText(','.join(post_info.artists))
            instanceui_danbooru_post.LE_cop.setText(','.join(post_info.copyright))
            instanceui_danbooru_post.TE_tags.setText(','.join(post_info.tags))
            instanceui_danbooru_post.TE_Info.setText('\n'.join(post_info.post_information))
        else:
            my_logger.info('获取信息失败')
    except Exception as e:
        my_logger.error(e)

def slot_danbooru_post_btn_download_clicked():
    global post_info

    if post_info is not None:
        media = post_info.original_post_url
        media_name = post_info.name
        directory = 'downloads'
        if not os.path.exists(directory):
                os.makedirs(directory, exist_ok=True)

        my_logger.info('正在启用下载，请稍后。。。。。')
        try:
                Downloader().download_file(media,os.path.join(directory,media_name) ,show_progress=False)
        except Exception as e:
                my_logger.error(e)
        else:
                my_logger.info(media_name + '下载完毕')


###  Gallery UI  ###
def slot_danbooru_gallery_btn_lastPg_clicked():
    global gallery_info

    if gallery_info.tail_page == "":
        gallery_info = instance_danbooru.gallery_parse(GalleryInfo._HOT)

    instanceui_danbooru_gallery.LE_page.setText(gallery_info.tail_page)

def slot_danbooru_gallery_btn_firstPg_clicked():
        instanceui_danbooru_gallery.LE_page.setText('1')

def slot_danbooru_gallery_btn_prevPg_clicked():
        current_page = int(instanceui_danbooru_gallery.LE_page.text())
        current_page -= 1
        
        if current_page < 1:
            current_page = 1
        new_page = f'{current_page}'

        instanceui_danbooru_gallery.LE_page.setText(new_page)


def slot_danbooru_gallery_btn_nextPg_clicked():
        current_page = int(instanceui_danbooru_gallery.LE_page.text())
        current_page += 1
        new_page = f'{current_page}'

        instanceui_danbooru_gallery.LE_page.setText(new_page)

def slot_danbooru_gallery_btn_obtain_clicked():
    global gallery_info

    try:
        url = instanceui_danbooru_gallery.LE_url.text()
        gallery_info = instance_danbooru.gallery_parse(url)
        # my_logger.debug(gallery_info.pre_imgs)
        instanceui_danbooru_gallery.show_images(gallery_info.pre_imgs,gallery_info.post_hrefs)
    except Exception as e:
        my_logger.error(e)

def slot_danbooru_gallery_radioBtn_hot_clicked():
    instanceui_danbooru_gallery.PB_lastPg.setEnabled(True)

    # hot 画廊无日期和规模
    instanceui_danbooru_gallery.dateEdit.setEnabled(False)
    instanceui_danbooru_gallery.comboBox_scale.setEnabled(False)

    slot_danbooru_gallery_update_url()

def slot_danbooru_gallery_radioBtn_popular_clicked():
    instanceui_danbooru_gallery.dateEdit.setEnabled(True)
    instanceui_danbooru_gallery.comboBox_scale.setEnabled(True)

    instanceui_danbooru_gallery.PB_lastPg.setEnabled(False) # popular 画廊无尾页

    slot_danbooru_gallery_update_url()

def slot_danbooru_gallery_update_url():
    global gallery_info

    # 获取三个控件的值
    str_date = instanceui_danbooru_gallery.dateEdit.date().toString("yyyy-MM-dd")
    str_scale = instanceui_danbooru_gallery.comboBox_scale.currentText()
    str_page = instanceui_danbooru_gallery.LE_page.text()

    parameter = {
            'date': str_date,
            'scale': str_scale,
            'page': str_page
    }

    if instanceui_danbooru_gallery.RB_hot.isChecked():
        new_url = GalleryInfo._HOT + '&page=' + str_page
        instanceui_danbooru_gallery.LE_url.setText(new_url)
    elif instanceui_danbooru_gallery.RB_popular.isChecked():
        lt = []
        for k,v in parameter.items():
                lt.append(k+'='+str(v))
        query_str = "&".join(lt)
        new_url = GalleryInfo._POPULAR + '?' + query_str
        instanceui_danbooru_gallery.LE_url.setText(new_url)
    else:
        my_logger.error("画廊选项出错")