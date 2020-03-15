#! /usr/bin/env python3.7

import json
import os

# пути
PATH = {"file": "./storage"}

# хранилище
storage = {}


def __init_storage():
    """Функция инициализации хранилища."""
    if not os.path.isfile(PATH["file"]):
        # если файл хранилища данных нет
        schedule = {}
        for i in range(1, 8):
            schedule[i] = {}
        storage.update({"schedule": schedule, "note": {}})
        # запись файла на диск
        __dump()
    else:
        # загрузка файла
        __load()


def __load():
    """Функция загрузки данных из файла."""
    with open(PATH["file"]) as file:
        storage.update(json.load(file))


def __dump():
    """Функция записывает данные в файл."""
    with open(PATH["file"], "w") as file:
        # ensure_ascii - для того чтобы кириллица не кодировалась в ascii
        json.dump(storage, file, ensure_ascii=False)


def crypt_db():
    pass


def decrypt_db():
    pass


def get_schedule(day=None):
    """на всю неделю, при day != None на день, day in range(1, 8)"""
    if day is None:
        return storage["schedule"]
    else:
        return storage["schedule"].get(str(day), {})


def change_schedule(day, schedule):
    """Изменение расписания на день day in range(1, 8), type(schedule) == dict"""
    storage["schedule"][str(day)] = schedule
    __dump()


def add_note(day, event, text, *, todo=None):
    """Добавление "заметки" к "событию"
        Если задан аргумент is_done, заметка становится "задачей".
    """

    # если в хранилище нет заметки с ключом (день,событие)
    if storage["note"].get(f"({day},{event})") is None:
        storage["note"][f"({day},{event})"] = {}

    # индекс события (задачи)
    id = len(storage["note"][f"({day},{event})"].keys()) + 1

    storage["note"][f"({day},{event})"][id] = {
        "id": id, "content": text, "is_done": None if todo is None else False
    }
    __dump()


def get_notes(day, event):
    """Функция возвращает заметки (задачи) для конкретного дня и события"""
    return storage["note"][f"({day},{event})"]


def get_all_notes():
    return storage["note"]


def get_notes_by_key(key):
    """Функция возвращает заметки (задачи) по ключ: "день" или "событие"
        Если нужно использовать "день" и "событие":
            key = f"{day},{event}"
    """
    notes = {}
    for dkey in storage["note"].keys():
        if key in dkey:
            notes[dkey] = storage["note"][dkey]
    return notes


def done(day, event, id):
    """Функция помечает задачу выполненной """
    if storage["note"].get(f"({day},{event})") is not None:
        # если существует заметки для (день, событие)
        if storage["note"][f"({day},{event})"].get(f"{id}") is not None:
            # если существует заметка с id
            note = storage["note"][f"({day},{event})"][f"{id}"]
            if note["is_done"] is not None:
                note["is_done"] = True
                __dump()


# это дополнительная функция
# Для удаления "старых" заметок (задач)
def delete_note(day, event, id):
    """Удаление "заметки" ("задачи") из """
    if storage["note"].get(f"({day},{event})") is not None:
        # если существует заметки для (день, событие)
        if storage["note"][f"({day},{event})"].get(str(id)) is not None:
            # если существует заметка с id
            storage["note"][f"({day},{event})"].pop(str(id))
            if len(storage["note"][f"({day},{event})"].keys()) == 0:
                storage["note"].pop(f"({day},{event})")
            __dump()


#  инициализация хранилища
__init_storage()
