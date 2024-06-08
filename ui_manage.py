
import sys
from PyQt6.QtWidgets import QMainWindow,QApplication,QWidget,QMessageBox,QDialog
from UI import *
from spider2ui import danbooru_ui

class MyUIManage(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.danbooru_post = Ui_DanbooruPost()

        self.init_ui()


    def init_ui(self):
        self.danbooru_post.setupUi(self)
        self.testFn()


    def testFn(self):
        # self.main_window.PB_getInfo.clicked.connect(lambda : QMessageBox.information(QDialog(), "信息提示", "你点击了我"))

        self.danbooru_post.PB_getInfo.clicked.connect(lambda :danbooru_ui.print_log(self.danbooru_post,danbooru_ui.get_post_url(self.danbooru_post)))
        


def show_ui():
    app = QApplication(sys.argv)
    mywin = MyUIManage()
    mywin.show()
    sys.exit(app.exec())