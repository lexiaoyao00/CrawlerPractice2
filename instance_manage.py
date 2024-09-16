from spiders import *
from UI import *
from common import *

### UI ###
instanceui_danbooru_post = Ui_DanbooruPost()
instanceui_main_window = Ui_MainWindow()
instanceui_danbooru_gallery = Ui_DanbooruGallery()

### UI info ###
instanceInfo_danbooru_post_info = PostInfo()
instanceInfo_danbooru_gallery_info = GalleryInfo()

### Spiders ###
instance_baidu = BaiDu()
instance_danbooru = Danbooru()

### automation ###
instanceAuto_sstm = SSTM_Auto()