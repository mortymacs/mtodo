"""Action handler for events and signals."""
from database import Database
from config import Config


class Action:
    """Action handler class."""
    def __init__(self):
        self.__config = Config()
        self.__database = Database(self.__config.database_path)

    def add_new_item(self, _, interface, action_type, title=None, description=None, is_done=None, is_important=None):
        """Add new item (todo)."""
        if action_type == "new":
            interface.new_item()
        elif action_type == "save":
            action = self.__database.insert_item(title.get_text(),
                                                 description.get_text(),
                                                 is_done.get_value(),
                                                 is_important.get_value())
            if action is True:
                interface.refresh(interface.get_window("main_window"))
