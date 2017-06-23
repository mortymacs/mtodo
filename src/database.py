"""Database handler"""
import sqlite3 as sqlite


class Database:
    """Database handle class"""
    __instance = None
    _con = None
    _cur = None

    def __init__(self, db_path: str):
        """Initialize Database class"""
        self._db_path = db_path
        self._con = sqlite.connect(self._db_path)
        self._con.row_factory = sqlite.Row
        self._cur = self._con.cursor()

    def __new__(cls, *args, **kwargs):
        """Singletone implementation."""
        if cls.__instance is None:
            cls.__instance = super(Database, cls).__new__(cls)
        return cls.__instance

    def start(self):
        """Check that database which is ready or not"""
        try:
            self._cur.execute("SELECT * FROM todo_items")
        except sqlite.OperationalError:
            self.create_tables()
        return True

    def create_tables(self):
        """Create required tables"""
        self._cur.execute("CREATE TABLE todo_items("
                          "id            INT   PRIMARY KEY,"
                          "title         TEXT  NOT NULL,"
                          "description   TEXT  NOT NULL,"
                          "is_done       INT   NOT NULL,"
                          "is_important  INT   NOT NULL"
                          ")")
        self._con.commit()

    def check(self):
        """Check db connection and cursor"""
        return all((self._con, self._cur))

    def select_items(self, where: str="1"):
        """Select item(s) from db"""
        if not self.check():
            return False

        try:
            self._cur.execute("SELECT * FROM todo_items WHERE ?", (where, ))
        except sqlite.OperationalError:
            print("Database fetch item failed.")
            return None

        return self._cur.fetchall()

    def insert_item(self, title: str, description: str, is_done: bool, is_important: bool):
        """Insert new item in db"""
        if not self.check():
            return False

        is_done = 1 if is_done is True else 0
        is_important = 1 if is_important is True else 0

        self._cur.execute("INSERT INTO todo_items "
                          "(title, description, is_done, is_important) "
                          "VALUES "
                          "(?, ?, ?, ?)", (title, description, is_done, is_important))
        self._con.commit()
        return True
