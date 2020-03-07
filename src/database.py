# -*- coding: utf-8 -*-

import sqlite3



class DB:

    def __init__(self, name):
        self.database = sqlite3.connect(name)
        

    def add_apartment_temperature(self, *, city_id, area_id, house_id, apartment_id, count, temperature):
        try:
            self.database.executescript(f"INSERT INTO apartment_temperature VALUES ({city_id}, {area_id}, {house_id}, {apartment_id}, {count}, {temperature})")
        except Exeption:    
            pass

    def get_apartment_temperature(self, *, city_id, area_id, house_id, apartment_id):
        return self.database.executescript(f"""
        SELECT * FROM apartment_temperature WHERE
        city_id = {city_id} and 
        area_id = {area_id} and
        house_id = {house_id} and
        apartment_id = {apartment_id};                       
        """)
   
    def _create_tables(sql):
        database.executescript(sql)
   
    def add_cities(self, cities):
        for city in cities:
            id = city.get("city_id", -1)
            name = city.get("name", "")
            self.database.executescript(
                f"INSERT INTO city VALUES ({id}, '{name}')"
            )
        

SQL = """
PRAGMA FOREIGN_KEYS = on;

CREATE TABLE city(
    city_id int PRIMARY KEY,
    city_name text
);

CREATE TABLE city_temperature(
    city_id int PRIMARY KEY,
    time int,
    temperature int,
    FOREIGN KEY (city_id) REFERENCES city(city_id)
);

CREATE TABLE apartment_temperature(
    city_id int,
    area_id int,
    house_id int,
    apartment_id int,
    count int,
    temperature int,
    FOREIGN KEY (city_id) REFERENCES city(city_id)
);

CREATE TABLE target_temperature(
    city_id int PRIMARY KEY,
    time int,
    apartment_id int,
    temperature int,
    FOREIGN KEY (city_id) REFERENCES city(city_id)
);

"""

for i in range(1,17):
    city_name = (load_data(f"{ENV['url']}/{i}", read_token("../token.txt")))["data"]["city_name"]
    database.executescript(f"INSERT INTO city VALUES ({i}, '{city_name}')")
    
database.commit()

cursor = database.cursor()`

database.close()
