"""Todo widget library."""
from typing import Callable
from abc import ABCMeta
import os

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, Gio


class Widget(metaclass=ABCMeta):
    """Abstract class for Widget"""
    _widget = None

    def __init__(self):
        raise NotImplemented

    @property
    def render(self):
        return self._widget

    def on_click(self, method, *args):
        self._widget.connect("clicked", method, *args)


class HeaderBar(Widget):
    """Draw header for window"""

    def __init__(self, title: str, subtitle: str, buttons: dict):
        """Initialize HeaderBar class"""
        self._widget = Gtk.HeaderBar()
        self._widget.set_show_close_button(True)
        self._widget.props.title = title
        self._widget.set_subtitle(subtitle)
        if buttons:
            for button, position in buttons.items():
                if position == "left":
                    self._widget.pack_start(button.render)
                elif position == "right":
                    self._widget.pack_end(button.render)


class Window(Gtk.Window):
    """Draw window form"""

    def __init__(self, name: str, title: str, subtitle: str, width: int,
                 height: int, header_buttons: dict, is_parent: bool):
        """Initialize Window class"""
        super(Window, self).__init__(title=title)
        self._name = name
        self._title = title
        self._subtitle = subtitle
        self._width = width
        self._height = height
        self._on_resize_callback = None
        if header_buttons:
            self._header = HeaderBar(self._title, self._subtitle, header_buttons)
            self.set_titlebar(self._header.render)
        else:
            self._header = None
        self._is_parent = is_parent

        if self._is_parent:
            self.resize(self._width, self._height)
        else:
            self.set_size_request(self._width, self._height)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_border_width(10)
        self.set_name(self._name)

        self._scrolled = Gtk.ScrolledWindow()
        self._scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self._box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self._box.set_homogeneous(False)
        self.add(self._scrolled)
        self._scrolled.add(self._box)

        if self._is_parent:
            self.connect("delete-event", Gtk.main_quit)
            self.connect("size_allocate", self.on_size_allocate)

    def on_size_allocate(self, window, _) -> None:
        """Connector on size-allocate event."""
        if self._on_resize_callback:
            self._on_resize_callback("on_resize", {
                "height": window.get_allocated_height(),
                "width": window.get_allocated_width()
            })

    def delegate(self, event_name: str, callback: Callable) -> None:
        if event_name == "on_resize":
            self._on_resize_callback = callback

    def on_resize(self, method, *args):
        """Call method on window resize."""
        self.connect("configure-event", method, *args)

    def set_icon(self, icon_path: str):
        """Set icon to the main window."""
        self.set_default_icon_from_file(icon_path)

    def join(self, obj: object):
        """Add object into window"""
        if hasattr(obj, "render"):
            self._box.pack_start(obj.render, False, False, 0)

    def render(self):
        """Show all items"""
        self.show_all()

    def cleanup(self):
        """Remove all items in window box"""
        all_children = self._box.get_children()
        for i in all_children:
            i.destroy()


class Button(Widget):
    """Draw button"""

    def __init__(self, name: str, label: str):
        """Initialize Button class"""
        self._name = name
        self._label = label
        self._widget = Gtk.Button.new_with_label(self._label)
        self._widget.set_name(self._name)

    def set_label(self, value: str):
        """Set new value on button label"""
        self._widget.set_label(value)


class BigButton(Widget):
    """Draw big button"""

    def __init__(self, name: str, label: str):
        """Initialize BigButton class"""
        self._name = name
        self._label = Gtk.Label()
        self._label.set_markup(label)
        self._label.set_halign(Gtk.Align.START)
        self._widget = Gtk.Button()
        self._widget.set_name(self._name)
        self._widget.add(self._label)


class IconButton(Widget):
    """Draw button"""

    def __init__(self, name: str, icon_name: str):
        """Initialize Button class"""
        self._name = name
        self._icon_name = icon_name
        self._icon = Gio.ThemedIcon(name=icon_name)
        self._widget = Gtk.Button()
        self._widget.add(Gtk.Image.new_from_gicon(self._icon, Gtk.IconSize.BUTTON))
        self._widget.set_name(self._name)


class Input(Widget):
    """Draw input"""
    _is_modified = False

    def __init__(self, name: str, placeholder: str, multi_line: bool):
        """Initialize Input class"""
        self._name = name
        self._placeholder = placeholder
        self._multi_line = multi_line
        if self._multi_line is True:
            self._widget = Gtk.TextView()
            self._widget.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
            self._widget.set_size_request(400, 219)
            #placeholder
            self._widget.connect("focus-in-event", self._in_focus)
            self._widget.connect("focus-out-event", self._out_focus)
            self._widget.get_buffer().set_text(self._placeholder)
        else:
            self._widget = Gtk.Entry()
            self._widget.unset_state_flags(Gtk.StateFlags.FOCUSED)
            self._widget.set_placeholder_text(self._placeholder)

        self._widget.set_name(self._name)

    def _in_focus(self, widget, _):
        """When focused in input."""
        if self.get_text() == self._placeholder:
            self.set_text("")

    def _out_focus(self, widget, _):
        """When focused out of input."""
        if self.get_text() == "":
            self.set_text(self._placeholder)

    def set_text(self, value: str):
        """Set new value in input"""
        if value is not None:
            if self._multi_line:
                self._widget.get_buffer().set_text(value)
            else:
                self._widget.set_text(value)

    def get_text(self):
        """Get input value"""
        if self._multi_line:
            return self._widget.get_buffer().get_text(
                self._widget.get_buffer().get_start_iter(),
                self._widget.get_buffer().get_end_iter(),
                True
            )
        return self._widget.get_text()


class Box(Widget):
    def __init__(self, name: str, is_vertical: bool):
        self._name = name
        self._is_vertical = is_vertical
        if self._is_vertical is True:
            orientation = Gtk.Orientation.VERTICAL
        else:
            orientation = Gtk.Orientation.HORIZONTAL
        self._widget = Gtk.Box(orientation=orientation, spacing=10)
        self._widget.set_name(self._name)
        self._widget.set_homogeneous(False)

    def join(self, obj, expand=False, fill=False):
        """Add object into box"""
        if hasattr(obj, "render"):
            self._widget.pack_start(obj.render, expand, fill, 0)


class Switch(Widget):
    """Draw switch"""

    def __init__(self, name: str):
        """Initialize Switch class."""
        self._name = name
        self._widget = Gtk.Switch()
        self._widget.set_name(self._name)

    def get_value(self):
        """Get switch value."""
        if self._widget.get_active() == 1:
            return True
        return False

    def set_value(self, value):
        """Set switch value."""
        if value is not None:
            self._widget.set_active(1 if value is True else 0)


class Label(Widget):
    """Draw label"""

    def __init__(self, name: str, label: str):
        """Initialize Label class"""
        self._name = name
        self._label = label
        self._widget = Gtk.Label()
        self._widget.set_markup(self._label)
        self._widget.set_halign(Gtk.Align.START)
        self._widget.set_name(self._name)


class Alert(Widget):
    """Draw alert box"""

    def __init__(self, name: str, title: str, body: str):
        """Initialize Alert class"""
        self._name = name
        self._title = title
        self._body = body
        self._widget = Gtk.Label()
        self._widget.set_name(self._name)
        self._widget.set_markup("<big><b>{}</b></big>\n{}".format(self._title, self._body))
