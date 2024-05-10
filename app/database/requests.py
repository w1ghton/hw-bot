import sqlite3 as sql

objects = {
    "rus": "Русский",
    "literature": "Литература",
    "math": "Математика",
    "geometry": "Геометрия",
    "informatics": "Информатика",
    "history": "История",
    "history_spb": "История и культура СПБ",
    "social": "Обществознание",
    "geography": "География",
    "biology": "Биология",
    "physics": "Физика",
    "chemistry": "Химия",
    "obj": "ОБЖ",
    "technology": "Технология",
    "eng": "Английский",
    "foreign_language": "Вт. иностранный",
}


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
        for i in objects:
            res.append(f", {i} TEXT")
        res.append(")")
        query = "".join(res)
        print(query)
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
                    """
            cur.execute(query, [user_class])
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


def get_hw(user_id: int, object_name: str) -> str:
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
        print(object_name)
        cur.execute(f'SELECT {object_name} FROM classes WHERE name = "{user_class}"')
        db.commit()
        try:
            hw = "".join(cur.fetchone())
        except TypeError:
            hw = "Домашнее задание не найдено"
        return hw
