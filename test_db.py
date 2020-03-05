BEGIN TRANSACTION;

CREATE TABLE city(
    city_id integer PRIMARY KEY, 
    city_name text
);

CREATE TABLE tempersture_city(
    id integer PRIMARY KEY, 
    city_id int,
    temperature int,
    time int
);

CREATE INDEX IF NOT EXISTS ixcity ON tempersture_city (city_id);
CREATE INDEX IF NOT EXISTS ixtime ON tempersture_city (time);
CREATE INDEX IF NOT EXISTS ixcitytime ON tempersture_city (city_id,time);

CREATE TABLE apartment(
    city_id int,
    area_id int,
    house_id int,
    apartment_id int,
    temperature int
);

CREATE TABLE temperature_apartment(
    time int,
    id int,
    temperature int
);
