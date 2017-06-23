"""User interface handler."""
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

import lib
import widget
from database import Database
from config import Config
from action import Action


class Interface:
    """Interface class."""

    # windows variable structure: {"<WINDOW NAME>": "<WIDGET OBJECT>"}
    __windows = {}
    __database = None
    _is_done_btn = None
    
    def __init__(self):
        """Initialize UserInterface class."""
        self.__config = Config()
        self.__action = Action()
        self.__database = Database(self.__config.database_path)

    def start(self):
        """Start user interface by generating widgets and objects."""
        add_new_btn = widget.Button("button_normal", "New")
        is_done_btn = widget.Button("button_light", "0")
        self._is_done_btn = is_done_btn
        main_window = widget.Window("Main", "Todo", 500, 400, {add_new_btn: "left", is_done_btn: "left"}, True)
        self.__windows.update({"main_window": main_window})
        add_new_btn.on_click(self.__action.add_new_item, *(self, "new"))
        self.refresh(main_window)
        self.render()

    def refresh(self, window):
        """Refresh main window widgets and objects."""
        db_rows = self.__database.select_items()
        if db_rows is None:
            return False

        window.cleanup()

        if len(db_rows) == 0:
            not_item_alert = widget.Alert("alert_normal",
                                          "No Todo Found.",
                                          "Click on 'Add New' button on your top-left side.")
            window.join(not_item_alert)
        else:
            is_done_counter = 0
            for item in db_rows:
                name = "todo_item_normal"
                if item["is_important"] == 1:
                    name = "todo_item_important"
                if item["is_done"] == 1:
                    is_done_counter += 1
                    self._is_done_btn.set_label(str(is_done_counter))
                    continue

                item_button = widget.BigButton(name, "<big><b>{}</b></big>\n{}".format(item["title"], item["description"]))
                window.join(item_button)

        self.load_style()
        window.render()

    def new_item(self):
        """New item window."""
        save_btn = widget.Button("button_blue", "Save")
        window = widget.Window("Main", "Todo - New Item", 500, 480, {save_btn: "left"}, False)
        box = widget.Box("new_data", True)
        switch_box = widget.Box("switch_data", True)
        title = widget.Input("title", "Title", False)
        description = widget.Input("description", "Description", True)
        is_done = widget.Switch("is_done")
        is_done_label = widget.Label("is_done_label", "Is done")
        is_done_box = widget.Box("is_done_data", False)
        
        is_important = widget.Switch("is_important")
        is_important_label = widget.Label("is_important_label", "Is Important")
        is_important_box = widget.Box("is_important_data", False)

        is_done_box.join(is_done_label, True, True)
        is_done_box.join(is_done)

        is_important_box.join(is_important_label, True, True)
        is_important_box.join(is_important)
        
        box.join(title)
        box.join(description)
        switch_box.join(is_important_box)
        switch_box.join(is_done_box)
        
        save_btn.on_click(self.__action.add_new_item, *(self, "save", title, description, is_done, is_important))
        window.join(box)
        window.join(switch_box)
        window.render()

    def get_window(self, window_name):
        return self.__windows[window_name]

    def render(self):
        """Run software GUI."""
        Gtk.main()

    def load_style(self):
        """Load CSS theme."""
        style = Gtk.CssProvider()
        style.load_from_path(self.__config.software_style_file)

        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            style,
            Gtk.STYLE_PROVIDER_PRIORITY_USER
        )
