import ipywidgets as widgets
from ipywidgets import HTML, Button, Layout, jslink, IntText, IntSlider, Label, Dropdown
from IPython.display import display
import sys

import matplotlib
import numpy as np
import matplotlib.pyplot as plt


sys.path.append("../data_miner/src")
import data_miner
from database import DB
import json

# need set path to file of data
"""
with open("/tmp/data.json") as fd:
    data = json.load(fd)
"""
data = {"x": [1,2], "t": [10, 20]}


data_miner.initialize()

def create_dropdown(*, options=[], description=""):
    return widgets.Dropdown(
        options=options,
        value=options[0],
        description=description,
        disabled=False,
        style={'description_width': 'initial'}
    )

class Node:
    """"""
    def __init__(self, *, constructor=widgets.Box, nodes=[]):
        self.box = constructor([
            node.box if isinstance(node, Node) else node for node in nodes
        ])

    def add_child_node(self, node):
        """"""
        self.box.children = (
            *self.box.children,
            node.box if isinstance(node, Node) else node
        )


class Layout:

    """Main layout"""
    def __init__(self):
        self.left_pane = Node(constructor=widgets.HBox)
        self.right_pane = Node(constructor=widgets.HBox)
        self.root = Node(constructor=widgets.VBox, nodes=[self.left_pane, self.right_pane])

    def add_to_left_pane(self, node):
        self.left_pane.add_child_node(node)

    def add_to_right_pane(self, node):
        self.right_pane.add_child_node(node)

    def render(self):
        display(self.root.box)

class Translator:
    def __init__(self):
        """"""
        self.dictionary = {}
        for city in data_miner.ENV["cities"]:
            self.dictionary[city["city_id"]] = city["city_name"]
            self.dictionary[city["city_name"]] = city["city_id"]
    def translate(self, word):
        return self.dictionary.get(word)
            
class CityMap():
    """"""
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
        return list(range(1, self.area_count+1))
    
    def get_houses_view(self, area_id):
        return list(self.area_map[area_id].keys())
    
    def get_apartment_view(self, area_id, house_id):
        return list(range(1, self.area_map[area_id][house_id]+1))

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
            for area_id in range(1, self.area_count+1):
                self.area_map[area_id] = {}
                res2 = data_miner.load_data(f"{url}/{area_id}")
                for house in res2["data"]["data"]:
                    self.area_map[area_id][house["house_id"]] = house["apartment_count"]
    
    
class UITask1:
    """"""
    def __init__(self):
        self.layout = Layout()
        self.city_map = CityMap(1)
        self.cities = self.city_map.get_cities_view()
        self.areas = self.city_map.get_areas_view()
        self.house = self.city_map.get_houses_view(1)
        self.apartments = self.city_map.get_apartment_view(1,1)

        
        self.select_city_wg = create_dropdown(options=self.cities, description="Город")
        self.select_area_wg = create_dropdown(options=self.areas, description="Район")
        self.select_hose_wg = create_dropdown(options=self.house, description="Дом")
        self.select_apartment_wg = create_dropdown(options=self.apartments, description="Квартира")
        
        self.show_btn = Button(
            description="Показать",
            disabled=False,
            button_style='info',
            tooltip='',
            icon='watch'
        )
        self.show_btn.on_click(self.on_click_show)
        self.layout.add_to_left_pane(self.show_btn)
        self.layout.add_to_left_pane(self.select_city_wg)


    def on_click_show(self, btn):
        x = data["x"]
        y = data["t"]
        plt.plot(x, y,)
        plt.xlabel('время')
        plt.ylabel('температура')
        plt.xlim(0, 356)
        plt.grid(True)
     
    def show(self):
        self.layout.render()



def task1():
    UITask1().show()

task1()
