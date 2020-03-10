#! /usr/bin/env python3
u"""Модуль сбора данных."""
import os
import json
import requests
from stimer import STimer
from random import shuffle
from database import DB

ENV = {
    "token_path": "../token",
    "cache": ".cache.json",
    "targets": [],
    "url": "http://dt.miet.ru/ppo_it/api",
    "dbname": "../database.db",
    "delay": 60,
    "end": 24 * 3600
}

with open(ENV["token_path"]) as file:
    ENV["token"] = file.read().strip()


def init_random(size, max_val):
    """Генерация диапазона случайных значений."""
    keys = list(range(1, max_val + 1))
    shuffle(keys)
    return dict.fromkeys(keys[0:size])


def gen_random_targets(cities):
    """Генерация целей для сбора данных."""
    targets = {}
    for city in cities:
        # случайные номера значения районов
        areas = init_random(4, city["area_count"])
        for i, area_id in enumerate(areas.keys()):
            # список для хранения номеров домов для текущего города и района
            # запрос данных для
            res = load_data(f"{ENV['url']}/{city['city_id']}/{area_id}")
            houses = init_random(2, len(res["data"]["data"]))
            for j, house_id in enumerate(houses.keys()):
                url = f"{ENV['url']}/{city['city_id']}/{area_id}/{house_id}"
                res2 = load_data(url)
                size = 1
                if i == 3 and j == 1:
                    size += 2
                apartments = init_random(
                    size, res2["data"]["data"]["apartment_count"]
                )
                houses[house_id] = list(apartments.keys())
            areas[area_id] = houses
        targets[city["city_id"]] = areas
    return targets


def make_targets(cities):
    """Создание списка целей."""
    targets_map = gen_random_targets(cities)
    targets = []
    for city_id in targets_map.keys():
        target = {}
        target["city_id"] = city_id
        for area_id in targets_map[city_id]:
            target["area_id"] = area_id
            for house_id in targets_map[city_id][area_id]:
                target["house_id"] = house_id
                for apartment_id in targets_map[city_id][area_id][house_id]:
                    target["apartment_id"] = apartment_id
                    targets.append(target.copy())
    return targets


def load_data(url=ENV["url"], token=ENV["token"]):
    """Функция загрузки данных."""
    result = {"data": None, "error": None}
    try:
        print(f">>> REQ: {url} ")
        res = requests.get(url, headers={"X-Auth-Token": token})
        print(f"<<< RES: {res.status_code}\n\t{res.text}")
        if res.status_code == 200:
            result["data"] = res.json()
        else:
            result["error"] = res.text
    except Exception as error:
        print(error)
    return result


def get_cities():
    res = load_data()
    cities = []
    if res["data"] is not None:
        cities = res["data"]["data"]
    return cities


def get_cities_data(cities=None):
    """ извлечение подробных данных о каждом городе """
    if cities is None:
        cities = get_cities()
    for city in cities:
        res = load_data(f"{ENV['url']}/{city['city_id']}")
        if res["data"] is not None:
            city.update(res["data"]["data"])
    return cities


def get_apatments_data(targets):
    """сбор данных о каждой цели"""
    data_set = []
    for target in targets:
        url = f"{ENV['url']}/{target['city_id']}/{target['area_id']}/{target['house_id']}/{target['apartment_id']}"
        res = load_data(url, ENV["token"])
        dataset = {
            "city_id": target['city_id'],
            "area_id": target['area_id'],
            "house_id": target['house_id'],
            "apartment_id": target['apartment_id'],
            "temperature": None
        }
        if res["data"] is not None:
            dataset["temperature"] = res["data"]["data"]["temperature"]
        else:
            dataset["temperature"] = -273
        data_set.append(dataset)
    return data_set


def get_one_target(city, area, house, apartment):
    """Сбор данных об одной цели в реальном времени"""
    data = load_data(f"{ENV['url']}/{city}/{area}/{house}/{apartment}")
    return data

def read_cache():
    """Чтение закэшированных значений городов и целей"""
    data = None
    if os.path.isfile(ENV["cache"]):
        with open(ENV["cache"]) as fd:
            data = json.load(fd)
    return data

def write_cache():
    with open(ENV["cache"], "w") as fd:
        json.dump({"cities": ENV["cities"], "targets": ENV["targets"]}, fd)

def initialize():
    """Функция инициализации."""
    data = read_cache()
    if data is not None:
        ENV["cities"] = data["cities"]
        ENV["targets"] = data["targets"]
    else:
        # получение списка городов
        ENV["cities"] = get_cities()
        # генерация списка целей
        ENV["targets"] = make_targets(get_cities_data(ENV["cities"]))
        write_cache()


def main():
    """Главная функция."""
    initialize()
    if os.path.isfile(ENV["dbname"]):
        os.remove(ENV["dbname"])
    db = DB(ENV["dbname"])
    db.add_cities(ENV["cities"])
    db.add_targets(ENV["targets"])
    timer = STimer(ENV["end"])
    count = 0
    while not timer.is_stop():
        # Главный цикл сбора данных
        cities_data = get_cities_data(ENV["cities"])
        targets_data = get_apatments_data(ENV["targets"])
        print(f"Received {len(cities_data) + len(targets_data)} out of {len(ENV['cities'])+len(ENV['targets'])} objects")
        print("Saving...")
        for city in get_cities_data(ENV["cities"]):
            db.add_city_temperature(
                city_id=city["city_id"],
                step=count,
                temperature=city["temperature"]
            )
        for target in get_apatments_data(ENV["targets"]):
            db.add_apartment_temperature(
                city_id=target["city_id"],
                area_id=target["area_id"],
                house_id=target["house_id"],
                apartment_id=target["apartment_id"],
                step=count,
                temperature=target["temperature"]
           )
        count += 1
        print(f"Timeout {ENV['delay']}s.")
        timer.sleep(ENV['delay'])

if __name__ == "__main__":
    main()
