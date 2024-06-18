import sys
from PyQt6.QtWidgets import QMainWindow,QApplication,QWidget,QMessageBox,QDialog
# from UI import *
from spider2ui import danbooru_ui
from instance_manage import instanceui_danbooru_post,instanceui_main_window
from logger import my_logger

class MyUIManage(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()


    def init_ui(self):
        instanceui_main_window.setupUi(self)

        self.danbooru_post_win = QMainWindow(self)
        instanceui_danbooru_post.setupUi(self.danbooru_post_win)

        self.binding()


    def binding(self):
        # main window
        instanceui_main_window.PB_danbooru_post.clicked.connect(self.show_danbooru_post)
        instanceui_main_window.PB_danbooru_gallery.clicked.connect(self.show_danbooru_gallery)

        # danbooru post
        instanceui_danbooru_post.PB_getInfo.clicked.connect(lambda : danbooru_ui.slot_btn_getinfo_clicked())
        instanceui_danbooru_post.PB_download.clicked.connect(lambda : danbooru_ui.slot_btn_download_clicked())
        instanceui_danbooru_post.PB_close.clicked.connect(lambda : self.danbooru_post_win.close())

        my_logger.enable_qt_output(instanceui_danbooru_post.TE_log)

        # TODO:danbooru gallery


    def show_danbooru_post(self):
        self.danbooru_post_win.show()

    def show_danbooru_gallery(self):
        # TODO:
        pass

    def __del__(self):
        self.danbooru_post_win.close()


def show_ui():
    app = QApplication(sys.argv)
    mywin = MyUIManage()
    mywin.show()
    sys.exit(app.exec())