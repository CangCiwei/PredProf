#! /usr/bin/env python3

import ipywidgets as widgets
from IPython.display import display
import sys

import matplotlib.pyplot as plt

sys.path.append("../data_miner/src")
import data_miner
# from database import DB

# need set path to file of data
"""
with open("/tmp/data.json") as fd:
    data = json.load(fd)
"""
data = {"x": [1, 2], "t": [10, 20]}


data_miner.initialize()


def create_dropdown(*, options=[], description=""):
    """Функция создает выпадающее меню."""
    return widgets.Dropdown(
        options=options,
        value=options[0],
        description=description,
        disabled=False,
        style={'description_width': 'initial'}
    )


class Node:
    """Класс описывает графический узел-контейнер."""
    def __init__(self, *, constructor=widgets.Box, nodes=[]):
        self.box = constructor([
            node.box if isinstance(node, Node) else node for node in nodes
        ])

    def add_child_node(self, node):
        """Метод добавляет дочерний узел к родительскому."""
        self.box.children = (
            *self.box.children,
            node.box if isinstance(node, Node) else node
        )


class Layout:

    """Main layout.
        +-----+
        |     |    upper pane includes ui widgets
        +-----+
        |     |    lower pane includes graph
        +-----+
    """
    def __init__(self):
        self.upper_pane = Node(constructor=widgets.HBox)
        self.lower_pane = Node(constructor=widgets.HBox)
        self.root = Node(
            constructor=widgets.VBox, nodes=[self.upper_pane, self.lower_pane]
        )

    def add_into_upper_pane(self, node):
        self.upper_pane.add_child_node(node)

    def add_into_lower_pane(self, node):
        self.lower_pane.add_child_node(node)

    def render(self):
        display(self.root.box)


class Translator:
    """Класс транслятор.
        Осуществляет трансляцию city_name -> city_id или city_id -> city_name
    """
    def __init__(self, cities=data_miner.ENV["cities"]):
        """Инициализатор."""
        self.dictionary = {}
        for city in data_miner.ENV["cities"]:
            self.dictionary[city["city_id"]] = city["city_name"]
            self.dictionary[city["city_name"]] = city["city_id"]

    def translate(self, word):
        """Метод трансляции.
            Осуществляет трансляцию city_name -> city_id или city_id -> city_name
        """
        return self.dictionary.get(word)


class CityMap():
    """Карта города."""
    def __init__(self, city_id):
        self.translator = Translator()
        self.__cities = data_miner.ENV["cities"]
        self.__city_id = self.__cities[0]["city_id"]
        self.__city_name = self.__cities[0]["city_name"]
        self.area_map = {}
        self.area_count = None
        self.__load_map()

    def get_cities_view(self):
        return [city["city_name"] for city in self.__cities]

    def get_areas_view(self):
        return list(range(1, self.area_count + 1))

    def get_houses_view(self, area_id):
        return list(self.area_map[area_id].keys())

    def get_apartment_view(self, area_id, house_id):
        return list(range(1, self.area_map[area_id][house_id] + 1))

    @property
    def city_name(self):
        return self.__city_name

    @city_name.setter
    def city_name(self, city_name):
        city_id = self.translator.translate(city_name)
        if city_id is not None:
            self.__city_id = city_id
            self.__city_name = city_name
            self.__load_map()

    def __load_map(self):
        url = f"{data_miner.ENV['url']}/{self.__city_id}"
        res = data_miner.load_data(url)
        if res["data"] is not None:
            data = res["data"]["data"]
            self.area_count = data["area_count"]
            self.area_map = {}
            for area_id in range(1, self.area_count + 1):
                self.area_map[area_id] = {}
                res2 = data_miner.load_data(f"{url}/{area_id}")
                for house in res2["data"]["data"]:
                    self.area_map[area_id][house["house_id"]] = house["apartment_count"]


class UITaskBase:

    def __init__(self):
        self.layout = Layout()

    def show(self):
        self.layout.render()


class UITask1(UITaskBase):
    """"""
    def __init__(self):
        super(UITask1).__init__()
        self.city_map = CityMap(1)
        self.cities = self.city_map.get_cities_view()

        self.select_city_wg = create_dropdown(options=self.cities, description="Город")
        self.input_area_wg = widgets.Text(
            value='',
            placeholder='',
            description='Район:',
            disabled=False
        )
        self.input_house_wg = widgets.Text(
            value='',
            placeholder='',
            description='Дом:',
            disabled=False
        )
        self.input_apartment_wg = widgets.Text(
            value='',
            placeholder='',
            description='Квартира:',
            disabled=False
        )

        self.show_btn = widgets.Button(
            description="Показать",
            disabled=False,
            button_style='info',
            tooltip='',
            icon='watch'
        )
        self.show_btn.on_click(self.on_click_show)
        self.layout.add_into_upper_pane(self.show_btn)
        self.layout.add_into_upper_pane(self.select_city_wg)

    def on_click_show(self, btn):
        
        
        self.input_area_wg.value
        
        x = data["x"]
        y = data["t"]
        plt.plot(x, y,)
        plt.xlabel('время')
        plt.ylabel('температура')
        plt.xlim(0, 356)
        plt.grid(True)


class UITask2(UITaskBase):

    def __init__(self):
        pass


class UITask3(UITaskBase):

    def __init__(self):
        pass


class UITask4(UITaskBase):

    def __init__(self):
        pass


def task1():
    UITask1().show()


def task2():
    UITask2().show()


def task3():
    UITask3().show()


def task4():
    UITask4().show()


def task5():
    pass
