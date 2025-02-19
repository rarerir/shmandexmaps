import os
import sys

import requests
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QWidget, QLabel

SCREEN_SIZE = [600, 450]


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.spn = 0.01
        self.ll = [37.530887, 55.703118]
        self.theme = 'light'
        self.getImage()
        self.initUI()


    def getImage(self):
        server_address = 'https://static-maps.yandex.ru/v1?'
        api_key = 'f3a0fe3a-b07e-4840-a1da-06f18b2ddf13'
        ll = f'll={str(self.ll[0])},{str(self.ll[1])}'
        spn = f'spn={self.spn},{self.spn}'

        map_request = f"{server_address}{ll}&{spn}&theme={self.theme}&apikey={api_key}"
        response = requests.get(map_request)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')
        self.pixmap = QPixmap(self.map_file)
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(600, 450)
        self.image.setPixmap(self.pixmap)

    def closeEvent(self, event):
        """При закрытии формы подчищаем за собой"""
        os.remove(self.map_file)

    def keyPressEvent(self, event):
        key = event.key()
        if key:
            try:
                print(type(key), int(Qt.Key.Key_Down))
                if key == Qt.Key.Key_Tab:
                    if self.theme == 'light':
                        self.theme = 'dark'
                    elif self.theme == 'dark':
                        self.theme = 'light'
                if key == Qt.Key.Key_PageUp:
                    self.spn += 0.01
                if key == Qt.Key.Key_PageDown:
                    if self.spn - 0.01 > 0:
                        self.spn -= 0.01
                if key == int(Qt.Key.Key_Down):
                    self.ll[1] -= 0.0002
                # if key == Qt.Key.Key_left:
                #     self.ll[0] += 0.0002
                # if key == Qt.Key.Key_Up:
                #     self.ll[1] += 0.0002
                # if key == Qt.Key.Key_Right:
                #     self.ll[0] -= 0.0002
                self.getImage()
                self.pixmap = QPixmap(self.map_file)
                self.image.setPixmap(self.pixmap)
                self.repaint()
                self.image.update()
            except Exception as e:
                print(e)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
