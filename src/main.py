"""Main library to generate window forms."""
from interface import Interface
from database import Database
from config import Config


def start():
    """Start progress."""
    config = Config()
    config.start()

    database = Database(config.database_path)
    database.start()

    interface = Interface()
    interface.start()
