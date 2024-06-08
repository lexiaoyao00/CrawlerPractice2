from UI import Ui_DanbooruPost
from spiders import Danbooru
from spiders_manage import instance_danbooru

def get_post_url(ui_post:Ui_DanbooruPost):
        url = ui_post.LE_url.text()
        return url


def print_log(ui_post:Ui_DanbooruPost,log:str):
        ui_post.TE_log.append(log)