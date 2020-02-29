# -*- coding: utf-8 -*-
import requests
import time

ENV = {
   "targets": [
     {"city_id": 1, "area_id": 2, "house_id": 6, "apartment_id": 1},
     {"city_id": 2, "area_id": 2, "house_id": 6, "apartment_id": 1},
     {"city_id": 3, "area_id": 2, "house_id": 6, "apartment_id": 1},
     {"city_id": 4, "area_id": 2, "house_id": 6, "apartment_id": 1},
     {"city_id": 5, "area_id": 2, "house_id": 6, "apartment_id": 1},
     {"city_id": 6, "area_id": 2, "house_id": 6, "apartment_id": 1},
     {"city_id": 7, "area_id": 2, "house_id": 6, "apartment_id": 1},
     {"city_id": 8, "area_id": 2, "house_id": 6, "apartment_id": 1},
     {"city_id": 9, "area_id": 2, "house_id": 6, "apartment_id": 1},
     {"city_id": 10, "area_id": 2, "house_id": 6, "apartment_id": 1}
     
   ],
    "url": "http://dt.miet.ru/ppo_it/api",
    "token": None,
    "number": 10
}


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

def get_cities():
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
    data_set = []
    for target in ENV["targets"]:
        #"city_id": 1, "area_id": 2, "house_id": 6, "apartment_id": 1
        url = f"{ENV['url']}/{target['city_id']}/{target['area_id']}/{target['house_id']}/{target['apartment_id']}"
        print(url)
        data = load_data(url, ENV["token"])
        data_set.append(data)
    return data_set
        
def main():
    read_token("../token.txt")
    for i in range(ENV["number"]):
        data = get_data_set()
        time.sleep(1)
        print(data)
        

if __name__ == "__main__":    
    main()
