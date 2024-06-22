import sys

from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QGridLayout,QMainWindow,QSizePolicy
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
import requests

from UI.Ui_danbooru_gallery_fixed import Ui_DanbooruGalleryFixed

class Ui_DanbooruGallery(Ui_DanbooruGalleryFixed):
    # def __init__(self):
    def setupUi(self,parent=None):
        # super().__init__()
        # self.setupUi(self)
        super().setupUi(parent)

        # 创建一个新的 QWidget 来容纳图像
        self.image_widget = QWidget()

        # self.image_widget.setStyleSheet("background-color: red;") #显示背景色，调试时使用

        self.image_layout = QGridLayout()
        self.image_widget.setLayout(self.image_layout)

        # 将 image_widget 添加到主窗口布局中
        self.verticalLayout.addWidget(self.image_widget)

        self.image_labels = []  # 用于存储所有 QLabel 对象

    def show_images(self, prev_image_urls,post_urls):
        if prev_image_urls is None or len(prev_image_urls) == 0:
            return

        self.clear_images()  # 清空当前显示的图片

        for i, image_url in enumerate(prev_image_urls):
            label = QLabel(self.image_widget)

            label.setStyleSheet("border: 1px solid black;") #显示黑边框
            label.setFixedSize(150,150) #设置大小

            label.setAlignment(Qt.AlignmentFlag.AlignCenter)

            if post_urls is not None and len(post_urls) == len(prev_image_urls):
                label.mousePressEvent = lambda event, url=post_urls[i]: self.on_image_clicked(event, url)
            
            self.load_image(label, image_url)
            row = i // 5  # 每行显示 5 个图像
            col = i % 5
            self.image_layout.addWidget(label, row, col)
            self.image_labels.append(label)

            # 立即显示
            QApplication.processEvents()

    def clear_images(self):
        for label in self.image_labels:
            self.image_layout.removeWidget(label)
            label.deleteLater()
        self.image_labels.clear()

    def load_image(self, label:QLabel, image_url):
        pixmap = QPixmap()
        pixmap.loadFromData(self.fetch_image_data(image_url))
        scaled_pixmap = pixmap.scaled(label.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation) #按比例缩放图片适应label大小
        label.setPixmap(scaled_pixmap)


    def fetch_image_data(self, image_url):
        response = requests.get(image_url)
        return response.content

    def on_image_clicked(self, event, url):
        # TODO：跳转帖子解析界面
        print(f"Image clicked: {url}")
