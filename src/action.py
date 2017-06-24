"""Action handler for events and signals."""
from database import Database
from config import Config


class Action:
    """Action handler class."""
    def __init__(self):
        self.__config = Config()
        self.__database = Database(self.__config.database_path)

    def add_item(self, _, interface, action_type, title=None, description=None, is_done=None, is_important=None):
        """Add new item (todo)."""
        if action_type == "new":
            interface.todo_item()
        elif action_type == "save":
            action = self.__database.insert_item(title.get_text(),
                                                 description.get_text(),
                                                 is_done.get_value(),
                                                 is_important.get_value())
            if action is True:
                interface.refresh(interface.get_window("main_window"))
                interface.destroy("todo_item")

    def edit_item(self, _, interface, action_type, todo_id=None, title=None, description=None, is_done=None, is_important=None):
        """Edit todo item."""
        if action_type == "edit":
            # here we get input values
            interface.todo_item(todo_id,
                                title,
                                description,
                                is_done,
                                is_important)
        elif action_type == "save":
            # here we get input objects
            action = self.__database.update_item(todo_id,
                                                 title.get_text(),
                                                 description.get_text(),
                                                 is_done.get_value(),
                                                 is_important.get_value())
            if action is True:
                interface.refresh(interface.get_window("main_window"))
                interface.destroy("todo_item")

    def del_item(self, _, interface, action_type, todo_id):
        """Delete todo item."""
        if action_type == "del":
            action = self.__database.delete_item(todo_id)
            if action is True:
                interface.refresh(interface.get_window("main_window"))
                interface.destroy("todo_item")

    def all_items(self, _, interface, action_type):
        """Show items based on mode."""
        if action_type == "show":
            if interface.get_show_all_mode() is True:
                interface.set_show_all_mode(False)
                interface.refresh(interface.get_window("main_window"))
            else:
                interface.set_show_all_mode(True)
                interface.refresh(interface.get_window("main_window"))
