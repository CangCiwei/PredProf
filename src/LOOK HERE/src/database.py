"""Модуль работы с БД sqlite3."""
import sqlite3
import sys


class DB:
    """Класс-обертка над sqlite3."""

    def __init__(self, name: str):
        """Метод инициализации.
            name - имя БД
        """
        # открытие соединения с БД
        self.db_connection = sqlite3.connect(name)
        # создание таблиц в БД
        self._create_tables()

    def __del__(self):
        """Destructor."""
        # закрытие соединения с БД
        self.db_connection.close()


    def add_city_temperature(self, *, city_id, step, temperature):
        """Метод добавляет запись в таблицу city_temperature.
            city_id     - идентификатор (номер) города
            step        - шаг измерений
            temperature - значение температуры
        """
        try:
            self.db_connection.executescript(
                "\n".join([
                    "INSERT INTO city_temperature VALUES (",
                    f"{city_id},",
                    f"{step},",
                    f"{temperature}",
                    f");"
                ])
            )
        except Exception as err:
            # вывод сообщения об ошибке в стандартный поток ошибок
            print(err)

    def add_apartment_temperature(self, *, city_id, area_id, house_id, apartment_id, step, temperature):
        """Метод добавляет запись в таблицу apartment_temperature.
            city_id     - идентификатор (номер) города
            area_id     - идентификатор (номер) района
            house_id    - идентификатор (номер) дома
            step        - шаг измерений
            temperature - значение температуры
        """
        try:
            self.db_connection.executescript(
                "\n".join([
                    "INSERT INTO apartment_temperature VALUES (",
                    f"{city_id},",
                    f"{area_id},",
                    f"{house_id},",
                    f"{apartment_id},",
                    f"{step},",
                    f"{temperature}",
                    f");"
                ])
            )
        except Exception as err:
            # вывод сообщения об ошибке в стандартный поток ошибок
            sys.stderr.write(err)

    def get_apartment_temperature(self, *, city_id, area_id, house_id, apartment_id):
        """"""
        return self.db_connection.executescript(
            "\n".join([
                "SELECT * FROM apartment_temperature WHERE",
                f"city_id = {city_id} and",
                f"area_id = {area_id} and",
                f"house_id = {house_id} and",
                f"apartment_id = {apartment_id};"
            ])
        )

    def add_targets(self, targets):
        """Добавление целей для сбора данных."""
        sql = "INSERT INTO target VALUES"
        values = ""
        for target in targets:
            sql += f"\n\t({target['city_id']}, {target['area_id']}, {target['house_id']}, {target['apartment_id']}),"
        sql = f"{sql[0:-1]};"
        self.db_connection.executescript(sql)

    def add_cities(self, cities):
        """Добавление городов в БД"""
        sql = "".join([
            "INSERT INTO city VALUES\n\t",
            ',\n\t'.join([f'({city["city_id"]}, \'{city["city_name"]}\')' for city in cities]),
            ";"
        ])
        self.db_connection.executescript(sql)

    def _create_tables(self):
        """Создание таблицы БД"""
        SQL = """PRAGMA FOREIGN_KEYS = on;
            CREATE TABLE IF NOT EXISTS city(
                city_id int PRIMARY KEY NOT NULL,
                city_name text NOT NULL
            );

            CREATE TABLE IF NOT EXISTS city_temperature(
                city_id int NOT NULL,
                step int NOT NULL,
                temperature int NOT NULL,
                CONSTRAINT pk_city_temperature PRIMARY KEY (step, city_id),
                FOREIGN KEY (city_id) REFERENCES city(city_id)
            );
            CREATE INDEX IF NOT EXISTS idx_city_tmpr_cid ON city_temperature(city_id);

            CREATE TABLE IF NOT EXISTS target(
                city_id int NOT NULL,
                area_id int NOT NULL,
                house_id int NOT NULL,
                apartment_id int NOT NULL,
                CONSTRAINT pk_target PRIMARY KEY (city_id, area_id, house_id, apartment_id),
                FOREIGN KEY (city_id) REFERENCES city(city_id)
            );
            CREATE INDEX IF NOT EXISTS idx_target_cid ON target(city_id);
            CREATE INDEX IF NOT EXISTS idx_target_cid_aid ON target(city_id, area_id);
            CREATE INDEX IF NOT EXISTS idx_target_cid_aid_hid ON target(city_id, area_id, house_id);

            CREATE TABLE IF NOT EXISTS apartment_temperature(
                city_id int NOT NULL,
                area_id int NOT NULL,
                house_id int NOT NULL,
                apartment_id int,
                step int,
                temperature int
            );
            CREATE INDEX IF NOT EXISTS idx_aprtm_tmpr ON apartment_temperature(city_id, area_id, house_id, apartment_id);
        """
        self.db_connection.executescript(SQL)
