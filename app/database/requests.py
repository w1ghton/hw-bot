import sqlite3 as sql
from app.static.text import *
import ast


def create() -> None:
    """
    Создает 2 таблицы
    """
    with sql.connect("db.sqlite3") as db:
        cur = db.cursor()
        query = """
        CREATE TABLE IF NOT EXISTS users (
        id BIGINT NOT NULL PRIMARY KEY,
        class TEXT
        )
        """
        cur.execute(query)

        res = ["CREATE TABLE IF NOT EXISTS classes (name TEXT NOT NULL PRIMARY KEY"]
        for i in OBJECTS:
            res.append(f", {i} TEXT")
        res.append(")")
        query = "".join(res)
        cur.execute(query)
        db.commit()


def add_user(user_id: int, user_class: str) -> None:
    """
    Добавляет нового пользователя
    """
    with sql.connect("db.sqlite3") as db:
        cur = db.cursor()

        query = """
        SELECT * FROM users WHERE id = ?
        """
        cur.execute(query, [user_id])

        if cur.fetchone():
            query = """
                    UPDATE users
                    SET class = ?
                    WHERE id = ?
                    """
            cur.execute(query, [user_class, user_id])
        else:
            query = """
                    INSERT INTO users(id, class) VALUES(?, ?)
                    """
            cur.execute(query, [user_id, user_class])
        db.commit()


def add_class(user_class: str) -> None:
    """
    Добавляет новый класс
    """
    with sql.connect("db.sqlite3") as db:
        cur = db.cursor()
        query = """
        SELECT * FROM classes WHERE name = ?
        """
        cur.execute(query, [user_class])
        if not cur.fetchone():
            query = """
                    INSERT INTO classes(name) VALUES(?)
                    """
            cur.execute(query, [user_class])
        db.commit()


def get_hw(user_id: int, object_name: str) -> dict:
    """
    Получает домашнее задание
    """
    with sql.connect("db.sqlite3") as db:
        cur = db.cursor()
        query = """
        SELECT class FROM users WHERE id = ?
        """
        cur.execute(query, [user_id])
        user_class = "".join(cur.fetchone())
        cur.execute(f'SELECT {object_name} FROM classes WHERE name = "{user_class}"')
        db.commit()
        try:
            hwg = "".join(cur.fetchone())
        except TypeError:
            hwg = "{'text': 'Домашнее задание не найдено'}"
        return ast.literal_eval(hwg)


def add_hw(user_id: int, object_name: str, homework: dict) -> None:
    """
    Отправляет домашнее задание
    """
    with sql.connect("db.sqlite3") as db:
        cur = db.cursor()
        query = """
        SELECT class FROM users WHERE id = ?
        """
        cur.execute(query, [user_id])
        user_class = "".join(cur.fetchone())
        cur.execute(
            f'UPDATE classes SET "{object_name}" = "{homework}" WHERE name = "{user_class}"'
        )
        db.commit()
