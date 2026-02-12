import os
import sys
from PyQt6.QtCore import Qt
import requests
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton
SCREEN_SIZE = [1000, 1000]


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')
        self.inputx = QLineEdit(self)
        self.inputx.resize(SCREEN_SIZE[0] - 50, 30)
        self.inputx.move(40, 10)
        self.xlabel = QLabel("<h3>X</h3>", self)
        self.xlabel.move(20, 15)
        self.inputy = QLineEdit(self)
        self.inputy.resize(SCREEN_SIZE[0] - 50, 30)
        self.inputy.move(40, 50)
        self.ylabel = QLabel("<h3>Y</h3>", self)
        self.ylabel.move(20, 55)
        self.push_btn = QPushButton("Сгенерировать", self)
        self.push_btn.resize(SCREEN_SIZE[0] - 20, 30)
        self.push_btn.move(10, 95)
        self.push_btn.clicked.connect(self.getImage)
        self.image = QLabel(self)
        self.image.move(10, 105)
        self.image.resize(SCREEN_SIZE[0] - 20, SCREEN_SIZE[1] - 130)

    def getImage(self):
        server_address = 'https://static-maps.yandex.ru/v1?'
        api_key = 'f3a0fe3a-b07e-4840-a1da-06f18b2ddf13'
        ll_spn = f'll={self.inputx.text()},{self.inputy.text()}&spn=0.009,0.009'

        map_request = f"{server_address}{ll_spn}&apikey={api_key}"
        response = requests.get(map_request)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        # Запишем полученное изображение в файл.
        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)
        self.pixmap = QPixmap(self.map_file).scaled(self.image.width(), self.image.height(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.image.setPixmap(self.pixmap)

    def closeEvent(self, event):
        """При закрытии формы подчищаем за собой"""
        os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())