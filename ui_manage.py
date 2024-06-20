import sys
from PyQt6.QtWidgets import QMainWindow,QApplication,QWidget,QMessageBox,QDialog
# from UI import *
from spider2ui import danbooru_ui
from instance_manage import instanceui_danbooru_post,instanceui_main_window,instanceui_danbooru_gallery
from logger import my_logger

class MyUIManage(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()


    def init_ui(self):
        instanceui_main_window.setupUi(self)

        self.init_of_ui()

        self.binding()

        # instanceui_danbooru_gallery.setupUi(self)

        # 显示第一批图片
        # image_urls_batch1 = ["https://cdn.donmai.us/360x360/b7/37/b737b9bfe5009d0a5be0b87f3ab91841.jpg", 
        #                     "https://cdn.donmai.us/360x360/15/0e/150e22b6195e6e940a7bfb471c238f53.jpg",
        #                     "https://cdn.donmai.us/360x360/fc/36/fc36d31c9522a44ab0de7815f21a64e4.jpg",
        #                     "https://cdn.donmai.us/360x360/5b/e7/5be77cae21d97630a9606d68f56e859d.jpg",
        #                     "https://cdn.donmai.us/360x360/2a/df/2adf6e5d64dd0ad291f506bc94218bf6.jpg",
        #                     "https://cdn.donmai.us/360x360/99/09/99090acd4d6930c79fa8c56b61a079d3.jpg",
        #                     "https://cdn.donmai.us/360x360/df/5f/df5f4e41ceb7636539786ec47c863f6c.jpg"
        #                     ]
        # instanceui_danbooru_gallery.show_images(image_urls_batch1)

    def binding(self):
        # main window
        instanceui_main_window.PB_danbooru_post.clicked.connect(self.show_danbooru_post)
        instanceui_main_window.PB_danbooru_gallery.clicked.connect(self.show_danbooru_gallery)

        # danbooru post
        instanceui_danbooru_post.PB_getInfo.clicked.connect(lambda : danbooru_ui.slot_btn_getinfo_clicked())
        instanceui_danbooru_post.PB_download.clicked.connect(lambda : danbooru_ui.slot_btn_download_clicked())
        instanceui_danbooru_post.PB_close.clicked.connect(lambda : self.danbooru_post_win.close())
        # TODO:danbooru gallery

    def show_danbooru_post(self):
        self.danbooru_post_win.show()

    def show_danbooru_gallery(self):
        self.danbooru_gallery_win.show()


    def init_of_ui(self):
        # danbooru post
        self.danbooru_post_win = QMainWindow(self)
        instanceui_danbooru_post.setupUi(self.danbooru_post_win)

        my_logger.enable_qt_output(instanceui_danbooru_post.TE_log)

        # danbooru gallery
        self.danbooru_gallery_win = QMainWindow(self)
        instanceui_danbooru_gallery.setupUi(self.danbooru_gallery_win)



def show_ui():
    app = QApplication(sys.argv)
    mywin = MyUIManage()
    mywin.show()
    sys.exit(app.exec())