import sys
from PyQt6.QtWidgets import QMainWindow,QApplication,QWidget,QMessageBox,QDialog
from UI import *
from spider2ui import danbooru_ui
from instance_manage import instanceui_danbooru_post

class TextEditLogger:
    def __init__(self, text_edit):
        self.text_edit = text_edit

    def write(self, message:str):
        self.text_edit.append(message.rstrip())

    def flush(self):
        pass

class MyUIManage(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()


    def init_ui(self):
        instanceui_danbooru_post.setupUi(self)
        self.binding()

        # 输出重定向到log文本框
        sys.stdout = TextEditLogger(instanceui_danbooru_post.TE_log)
        sys.stderr = TextEditLogger(instanceui_danbooru_post.TE_log)


    def binding(self):
        instanceui_danbooru_post.PB_getInfo.clicked.connect(lambda : danbooru_ui.slot_btn_getinfo_clicked())
        instanceui_danbooru_post.PB_download.clicked.connect(lambda : danbooru_ui.slot_btn_download_clicked())



def show_ui():
    app = QApplication(sys.argv)
    mywin = MyUIManage()
    mywin.show()
    sys.exit(app.exec())