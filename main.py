import os
import pprint
import sys
import requests
import arcade
from to_rec import spn_sizes
from to_scale import scale_map
from move_map import to_move
from arcade.gui import UIManager, UIFlatButton, UIInputText, UILabel
from arcade.gui.widgets.layout import UIAnchorLayout, UIBoxLayout

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "MAP"
MAP_FILE = "map.png"


class GameView(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.manager = UIManager()
        self.manager.enable()
        self.anchor_layout = UIAnchorLayout(x=-310, y=-135)
        self.box_layout = UIBoxLayout(vertical=True, space_between=10)
        self.setup_widgets()
        self.anchor_layout.add(self.box_layout)
        self.manager.add(self.anchor_layout)
        self.points = ""

    def setup_widgets(self):
        flat_button = UIFlatButton(text="Сменить тему", width=600, height=20)
        flat_button.on_click = lambda event: self.theme_change()
        self.box_layout.add(flat_button)
        box = UIBoxLayout(vertical=False)
        self.input_text = UIInputText(width=400, height=30, text="Введите адрес объекта",
                                      border_color=(62, 70, 121, 255),
                                      text_color=(62, 70, 121, 255))
        box.add(self.input_text)
        flat_button1 = UIFlatButton(text="Искать", width=200, height=30)
        flat_button1.on_click = lambda event: self.get_coords(self.input_text.text)
        box.add(flat_button1)
        self.box_layout.add(box)
        self.label = UILabel(text="", font_size=14, width=600, align="left", text_color=(62, 70, 121, 255))
        self.box_layout.add(self.label)

    def setup(self):
        self.x, self.y, self.spn = 0, 0, 0
        self.theme = ""
        self.get_coords("Казань")

    def theme_change(self):
        if self.theme == "": self.theme="&theme=dark"
        else: self.theme = ""
        self.get_image()

    def on_draw(self):
        self.clear()
        arcade.draw_lbwh_rectangle_filled(
            0, 0, self.width, self.height, (238, 232, 231)
        )
        arcade.draw_texture_rect(
            self.background,
            arcade.LBWH(
                30,
                (self.height - self.background.height - 30),
                self.background.width,
                self.background.height
            ),
        )
        self.manager.draw()

    def get_image(self):
        server_address = 'https://static-maps.yandex.ru/v1?'
        api_key = 'f3a0fe3a-b07e-4840-a1da-06f18b2ddf13'
        ll_spn = f'll={self.x},{self.y}&spn={self.spn},{self.spn}{self.theme}'
        map_request = f"{server_address}{ll_spn}{self.points}&apikey={api_key}"
        response = requests.get(map_request)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        with open(MAP_FILE, "wb") as file:
            file.write(response.content)

        self.background = arcade.load_texture(MAP_FILE)

    def get_coords(self, town):
        server_address = 'http://geocode-maps.yandex.ru/1.x/?'
        api_key = '8013b162-6b42-4997-9691-77b7074026e0'
        geocoder_request = f'{server_address}apikey={api_key}&geocode={town}&format=json'
        response = requests.get(geocoder_request)
        try:
            json_response = response.json()
            toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
            self.x, self.y, self.spn =  [float(n) for n in toponym["Point"]["pos"].split(" ")] + [spn_sizes(toponym["boundedBy"]["Envelope"])]
            self.points = f"&pt={self.x},{self.y},pm2ntl"
            self.label.text = ""
            self.get_image()

        except Exception:
            self.label.text = "Ничего не найдено"

    def on_key_press(self, key, modifiers):
        spn, x, y = self.spn, self.x, self.y
        if key == arcade.key.PAGEUP:
            self.spn = scale_map(self.spn, "+")
        if key == arcade.key.PAGEDOWN:
            self.spn = scale_map(self.spn, "-")
        if key == arcade.key.UP:
            self.x, self.y = to_move(0, 0, 1, 0, self.x, self.y)
        if key == arcade.key.DOWN:
            self.x, self.y = to_move(0, 0, 0, 1, self.x, self.y)
        if key == arcade.key.RIGHT:
            self.x, self.y = to_move(1, 0, 0, 0, self.x, self.y)
        if key == arcade.key.LEFT:
            self.x, self.y = to_move(0, 1, 0, 0, self.x, self.y)
        if key == arcade.key.ENTER:
            self.get_coords(self.input_text.text)
        if (spn, x, y) != (self.spn, self.x, self.y):
            self.get_image()
def main():
    gameview = GameView(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    gameview.setup()
    arcade.run()
    os.remove(MAP_FILE)


if __name__ == "__main__":
    main()
