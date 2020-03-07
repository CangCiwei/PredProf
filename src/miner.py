# -*- coding: utf-8 -*-
import requests
import time
import sqlite3

ENV = {"targets": [], 
       "url": "http://dt.miet.ru/ppo_it/api", 
       "token": None, 
       "end_time": 5
       }

def make_targets():
    """создание целей"""
    for city in range(16):
        for area in range(4):
            for house in range(2):
                for apartment in range(5):
                    ENV["targets"].append({"city_id": city+1, "area_id": area+1, "house_id": house+1, "apartment_id": apartment+1})

def read_token(path):
    """ извлечение токена """
    with open(path) as fd:
        ENV["token"] = fd.read()
    return ENV["token"]


def load_data(url, token):
    """ извлечение данных """
    data = None
    try:
        res=requests.get(url, headers={"X-Auth-Token": token})
        if res.status_code == 200:
            data = res.json()
    except Exeption:
        pass
    return data


def get_cities(url):
    data = load_data(url)
    

def get_cities_data():
    """ извлечение подробных данных о каждом городе """
    url = "http://dt.miet.ru/ppo_it/api"
    token = read_token("../token.txt")
    cities = load_data("http://dt.miet.ru/ppo_it/api", token)
    if cities is not None:
        for idd, city in enumerate(cities.get("data", [])):
            ch = load_data(f"{url}/{city['city_id']}", token)
            if ch is not None:
                cities["data"][idd].update(ch.get("data", {}))
    else:
        cities = {}
    return cities.get("data", [])

def get_data_set():
    """сбор данных о каждой цели"""
    data_set = []
    for target in ENV["targets"]:
        url = f"{ENV['url']}/{target['city_id']}/{target['area_id']}/{target['house_id']}/{target['apartment_id']}"
        data = load_data(url, ENV["token"])
        data_set.append(data)
    return data_set
        
def get_one_target(city, area, house, apartment):
    """сбор данных об одной цели в реальном времени"""
    read_token("../token.txt")
    url = f"{ENV['url']}/{city}/{area}/{house}/{apartment}"
    data = load_data(url, ENV["token"])
    return data

def main():
    """основная функция"""
    read_token("../token.txt")
    make_targets()
    start_time = int(time.time())
    while int(time.time()) - start_time <= ENV["end_time"]:
        data = get_cities()
        print(data)
        print(" ")
        time.sleep(1)

def save_data(data):
    pass

if __name__ == "__main__":
    data = (load_data(f"{ENV['url']}/{i}", read_token("../token.txt")))["data"]["city_name"]
    print(data)
