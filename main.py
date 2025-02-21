import os
import sys

import requests
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton

SCREEN_SIZE = [600, 450]


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.geocode = 'Владивосток'
        self.spn = 0.01
        self.ll = [37.530887, 55.703118]
        self.theme = 'light'
        self.getImage()
        self.initUI()


    def getImage(self):
        server_address_map = 'https://static-maps.yandex.ru/v1?'
        api_key_map = 'f3a0fe3a-b07e-4840-a1da-06f18b2ddf13'
        ll = f'{str(self.ll[0])},{str(self.ll[1])}'
        spn = f'spn={self.spn},{self.spn}'
        geocode = self.geocode

        server_address = 'http://geocode-maps.yandex.ru/1.x/?'
        api_key = '8013b162-6b42-4997-9691-77b7074026e0'
        print(geocode)
        # Готовим запрос.
        geocoder_request = f'{server_address}apikey={api_key}&geocode={geocode}&format=json'
        print(geocoder_request)

        # Выполняем запрос.
        response = requests.get(geocoder_request)
        if response:
            # Преобразуем ответ в json-объект
            json_response = response.json()

            # Получаем первый топоним из ответа геокодера.
            # Согласно описанию ответа, он находится по следующему пути:
            toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
            # Полный адрес топонима:
            toponym_address = toponym["metaDataProperty"]["GeocoderMetaData"]["text"]
            # Координаты центра топонима:
            toponym_coodrinates = toponym["Point"]["pos"]
            print(toponym_coodrinates)
            l1, l2 = toponym_coodrinates.split()
            print(l1, l2)
            self.ll = [l1, l2]
            print(self.ll)

        else:
            print("Ошибка выполнения запроса:")
            print(geocoder_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")

        map_request = f"{server_address_map}ll={ll}&{spn}&theme={self.theme}&pt={ll},pm2rdm&apikey={api_key_map}"
        response_map = requests.get(map_request)

        if not response_map:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response_map.status_code, "(", response_map.reason, ")")
            sys.exit(1)

        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response_map.content)

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')
        self.pixmap = QPixmap(self.map_file)
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(600, 450)
        self.image.setPixmap(self.pixmap)
        self.line = QLineEdit(self)
        self.line.setGeometry(10, 10, 200, 20)
        self.btn_find = QPushButton('искать', self)
        self.btn_find.setGeometry(50, 40, 100, 40)
        self.btn_find.clicked.connect(self.findx)

    def findx(self):
        self.geocode = self.line.text()
        self.getImage()
        self.pixmap = QPixmap(self.map_file)
        self.image.setPixmap(self.pixmap)
        self.repaint()
        self.image.update()

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
                return e


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
