# Form implementation generated from reading ui file 'e:\GIT_pros\CrawlerPractice2\UI\danbooru_post.ui'
#
# Created by: PyQt6 UI code generator 6.7.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_DanbooruPost(object):
    def setupUi(self, DanbooruPost):
        DanbooruPost.setObjectName("DanbooruPost")
        DanbooruPost.resize(742, 724)
        self.centralwidget = QtWidgets.QWidget(parent=DanbooruPost)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.widget_post = QtWidgets.QWidget(parent=self.centralwidget)
        self.widget_post.setObjectName("widget_post")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.widget_post)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_artist = QtWidgets.QLabel(parent=self.widget_post)
        self.label_artist.setObjectName("label_artist")
        self.gridLayout_2.addWidget(self.label_artist, 1, 0, 1, 1)
        self.LE_url = QtWidgets.QLineEdit(parent=self.widget_post)
        self.LE_url.setObjectName("LE_url")
        self.gridLayout_2.addWidget(self.LE_url, 0, 1, 1, 1)
        self.LE_artist = QtWidgets.QLineEdit(parent=self.widget_post)
        self.LE_artist.setReadOnly(True)
        self.LE_artist.setObjectName("LE_artist")
        self.gridLayout_2.addWidget(self.LE_artist, 1, 1, 1, 1)
        self.label_url = QtWidgets.QLabel(parent=self.widget_post)
        self.label_url.setObjectName("label_url")
        self.gridLayout_2.addWidget(self.label_url, 0, 0, 1, 1)
        self.label_cop = QtWidgets.QLabel(parent=self.widget_post)
        self.label_cop.setObjectName("label_cop")
        self.gridLayout_2.addWidget(self.label_cop, 2, 0, 1, 1)
        self.LE_cop = QtWidgets.QLineEdit(parent=self.widget_post)
        self.LE_cop.setText("")
        self.LE_cop.setReadOnly(True)
        self.LE_cop.setObjectName("LE_cop")
        self.gridLayout_2.addWidget(self.LE_cop, 2, 1, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout_2, 0, 0, 1, 1)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_tags = QtWidgets.QLabel(parent=self.widget_post)
        self.label_tags.setObjectName("label_tags")
        self.gridLayout_3.addWidget(self.label_tags, 0, 0, 1, 1)
        self.TE_tags = QtWidgets.QTextEdit(parent=self.widget_post)
        self.TE_tags.setReadOnly(True)
        self.TE_tags.setObjectName("TE_tags")
        self.gridLayout_3.addWidget(self.TE_tags, 0, 1, 1, 1)
        self.label_info = QtWidgets.QLabel(parent=self.widget_post)
        self.label_info.setObjectName("label_info")
        self.gridLayout_3.addWidget(self.label_info, 1, 0, 1, 1)
        self.TE_Info = QtWidgets.QTextEdit(parent=self.widget_post)
        self.TE_Info.setReadOnly(True)
        self.TE_Info.setObjectName("TE_Info")
        self.gridLayout_3.addWidget(self.TE_Info, 1, 1, 1, 1)
        self.label_log = QtWidgets.QLabel(parent=self.widget_post)
        self.label_log.setObjectName("label_log")
        self.gridLayout_3.addWidget(self.label_log, 2, 0, 1, 1)
        self.TE_log = QtWidgets.QTextEdit(parent=self.widget_post)
        self.TE_log.setReadOnly(True)
        self.TE_log.setObjectName("TE_log")
        self.gridLayout_3.addWidget(self.TE_log, 2, 1, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout_3, 1, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.PB_getInfo = QtWidgets.QPushButton(parent=self.widget_post)
        self.PB_getInfo.setObjectName("PB_getInfo")
        self.horizontalLayout.addWidget(self.PB_getInfo)
        self.PB_download = QtWidgets.QPushButton(parent=self.widget_post)
        self.PB_download.setObjectName("PB_download")
        self.horizontalLayout.addWidget(self.PB_download)
        self.PB_filter = QtWidgets.QPushButton(parent=self.widget_post)
        self.PB_filter.setObjectName("PB_filter")
        self.horizontalLayout.addWidget(self.PB_filter)
        self.gridLayout_4.addLayout(self.horizontalLayout, 2, 0, 1, 1)
        self.gridLayout.addWidget(self.widget_post, 0, 0, 1, 1)
        DanbooruPost.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=DanbooruPost)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 742, 22))
        self.menubar.setObjectName("menubar")
        DanbooruPost.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=DanbooruPost)
        self.statusbar.setObjectName("statusbar")
        DanbooruPost.setStatusBar(self.statusbar)

        self.retranslateUi(DanbooruPost)
        QtCore.QMetaObject.connectSlotsByName(DanbooruPost)

    def retranslateUi(self, DanbooruPost):
        _translate = QtCore.QCoreApplication.translate
        DanbooruPost.setWindowTitle(_translate("DanbooruPost", "danbooru"))
        self.label_artist.setText(_translate("DanbooruPost", "Artist"))
        self.label_url.setText(_translate("DanbooruPost", "post url"))
        self.label_cop.setText(_translate("DanbooruPost", "Copyright"))
        self.label_tags.setText(_translate("DanbooruPost", "tags"))
        self.label_info.setText(_translate("DanbooruPost", "info"))
        self.label_log.setText(_translate("DanbooruPost", "log"))
        self.PB_getInfo.setText(_translate("DanbooruPost", "get"))
        self.PB_download.setText(_translate("DanbooruPost", "download"))
        self.PB_filter.setText(_translate("DanbooruPost", "filter"))