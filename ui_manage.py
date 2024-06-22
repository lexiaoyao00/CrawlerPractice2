import sys
from PyQt6.QtWidgets import QMainWindow,QApplication,QWidget,QMessageBox,QDialog,QDateEdit
from PyQt6.QtCore import Qt,QDate

from spider2ui import danbooru_ui
from instance_manage import instanceui_danbooru_post,instanceui_main_window,instanceui_danbooru_gallery
from instance_manage import instanceInfo_danbooru_gallery_info
from logger import my_logger

class MyUIManage(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()


    def init_ui(self):
        instanceui_main_window.setupUi(self)

        self.init_of_ui()

        self.binding()

    def binding(self):
        ### main window
        instanceui_main_window.PB_danbooru_post.clicked.connect(self.show_danbooru_post)
        instanceui_main_window.PB_danbooru_gallery.clicked.connect(self.show_danbooru_gallery)

        ### danbooru post
        instanceui_danbooru_post.PB_getInfo.clicked.connect(self._slot_danbooru_post_btn_getinfo_clicked)
        instanceui_danbooru_post.PB_download.clicked.connect(self._slot_danbooru_post_btn_download_clicked)
        instanceui_danbooru_post.PB_close.clicked.connect(self.danbooru_post_win.close)
        
        ### TODO:danbooru gallery
        #修改
        instanceui_danbooru_gallery.dateEdit.dateChanged.connect(self._slot_danbooru_gallery_update_url)
        instanceui_danbooru_gallery.dateEdit.dateChanged.connect(self._slot_danbooru_gallery_change_date_section)

        instanceui_danbooru_gallery.comboBox_scale.currentIndexChanged.connect(self._slot_danbooru_gallery_update_url)
        instanceui_danbooru_gallery.LE_page.textChanged.connect(self._slot_danbooru_gallery_update_url)

        # 按钮
        instanceui_danbooru_gallery.RB_hot.clicked.connect(lambda : self._slot_danbooru_gallery_btn_clicked('hot'))
        instanceui_danbooru_gallery.RB_popular.clicked.connect(lambda : self._slot_danbooru_gallery_btn_clicked('popular'))

        instanceui_danbooru_gallery.PB_obtain.clicked.connect(lambda : self._slot_danbooru_gallery_btn_clicked('obtain'))

        instanceui_danbooru_gallery.PB_firstPg.clicked.connect(lambda : self._slot_danbooru_gallery_btn_clicked('firstPg'))
        instanceui_danbooru_gallery.PB_prevPg.clicked.connect(lambda : self._slot_danbooru_gallery_btn_clicked('prevPg'))
        instanceui_danbooru_gallery.PB_nextPg.clicked.connect(lambda : self._slot_danbooru_gallery_btn_clicked('nextPg'))
        instanceui_danbooru_gallery.PB_lastPg.clicked.connect(lambda : self._slot_danbooru_gallery_btn_clicked('lastPg'))




    def init_of_ui(self):
        # danbooru post
        self.danbooru_post_win = QMainWindow(self)
        instanceui_danbooru_post.setupUi(self.danbooru_post_win)

        # my_logger.enable_qt_output(instanceui_danbooru_post.TE_log)
        my_logger.enable_console_output()

        # danbooru gallery
        self.danbooru_gallery_win = QMainWindow(self)
        instanceui_danbooru_gallery.setupUi(self.danbooru_gallery_win)

        self._init_danbooru_gallery()

    def show_danbooru_post(self):
        self.danbooru_post_win.show()

    def show_danbooru_gallery(self):
        self._slot_danbooru_gallery_update_url()
        self.danbooru_gallery_win.show()

    def _init_danbooru_gallery(self):
        instanceui_danbooru_gallery.dateEdit.setDate(QDate.currentDate()) # 当前日期
        instanceui_danbooru_gallery.LE_page.setText('1') # 第一页

        if instanceui_danbooru_gallery.RB_hot.isChecked():
            danbooru_ui.slot_danbooru_gallery_radioBtn_hot_clicked()
        elif instanceui_danbooru_gallery.RB_popular.isChecked():
            danbooru_ui.slot_danbooru_gallery_radioBtn_popular_clicked()

################################ post slots
    def _slot_danbooru_post_btn_getinfo_clicked(self):
        danbooru_ui.slot_danbooru_post_btn_getinfo_clicked()

    def _slot_danbooru_post_btn_download_clicked(self):
        danbooru_ui.slot_danbooru_post_btn_download_clicked()


################################ gallery slots
    def _slot_danbooru_gallery_update_url(self):
        danbooru_ui.slot_danbooru_gallery_update_url()

    def _slot_danbooru_gallery_btn_clicked(self,button:str):
        if button == 'obtain':
            danbooru_ui.slot_danbooru_gallery_btn_obtain_clicked()
        elif button == 'firstPg':
            danbooru_ui.slot_danbooru_gallery_btn_firstPg_clicked()
        elif button == 'prevPg':
            danbooru_ui.slot_danbooru_gallery_btn_prevPg_clicked()
        elif button == 'nextPg':
            danbooru_ui.slot_danbooru_gallery_btn_nextPg_clicked()
        elif button == 'lastPg':
            danbooru_ui.slot_danbooru_gallery_btn_lastPg_clicked()
        elif button == 'hot':
            danbooru_ui.slot_danbooru_gallery_radioBtn_hot_clicked()
        elif button == 'popular':
            danbooru_ui.slot_danbooru_gallery_radioBtn_popular_clicked()


        else:
            my_logger.debug('按钮绑定错误')
            danbooru_ui.slot_danbooru_gallery_btn_firstPg_clicked()

    def _slot_danbooru_gallery_change_date_section(self):
        current_select = instanceui_danbooru_gallery.comboBox_scale.currentText()

        if current_select == 'day':
            instanceui_danbooru_gallery.dateEdit.setCurrentSection(QDateEdit.Section.DaySection)
        elif current_select == 'week':
            instanceui_danbooru_gallery.dateEdit.setCurrentSection(QDateEdit.Section.DaySection)
        elif current_select == 'month':
            instanceui_danbooru_gallery.dateEdit.setCurrentSection(QDateEdit.Section.MonthSection)

        else:
            pass


def show_ui():
    app = QApplication(sys.argv)
    mywin = MyUIManage()
    mywin.show()
    sys.exit(app.exec())