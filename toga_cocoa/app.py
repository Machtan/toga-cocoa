from __future__ import print_function, absolute_import, division, unicode_literals

import signal
import sys

from .libs import *
from .window import Window
from .widgets.icon import Icon, TIBERIUS_ICON


class MainWindow(Window):
    def __init__(self, title=None, position=(100, 100), size=(640, 480)):
        super(MainWindow, self).__init__(title, position, size)

    def on_close(self):
        app = NSApplication.sharedApplication()
        app.terminate_(self._delegate)


class App(object):

    def __init__(self, name, app_id, icon=None, startup=None):
        self.name = name
        self.app_id = app_id

        # Set the icon for the app
        Icon.app_icon = Icon.load(icon, default=TIBERIUS_ICON)
        self.icon = Icon.app_icon

        self._startup_method = startup

    def _startup(self):
        self._impl = NSApplication.sharedApplication()
        self._impl.setActivationPolicy_(NSApplicationActivationPolicyRegular)

        self._impl.setApplicationIconImage_(self.icon._impl)

        app_name = sys.argv[0]

        self.menu = NSMenu.alloc().initWithTitle_('MainMenu')

        # App menu
        self.app_menuItem = self.menu.addItemWithTitle_action_keyEquivalent_(app_name, None, '')
        submenu = NSMenu.alloc().initWithTitle_(app_name)

        menu_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('About ' + app_name, None, '')
        submenu.addItem_(menu_item)

        menu_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('Preferences', None, '')
        submenu.addItem_(menu_item)

        submenu.addItem_(NSMenuItem.separatorItem())

        menu_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('Quit ' + app_name, get_selector('terminate:'), "q")
        submenu.addItem_(menu_item)

        self.menu.setSubmenu_forItem_(submenu, self.app_menuItem)

        # Help menu
        self.help_menuItem = self.menu.addItemWithTitle_action_keyEquivalent_('Apple', None, '')
        submenu = NSMenu.alloc().initWithTitle_('Help')

        menu_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('Visit homepage', None, '')
        submenu.addItem_(menu_item)

        self.menu.setSubmenu_forItem_(submenu, self.help_menuItem)

        # Set the menu for the app.
        self._impl.setMainMenu_(self.menu)

        # Create the main window
        self.main_window = MainWindow(self.name)
        self.main_window.app = self

        # Call user code to populate the main window
        self.startup()

        # Show the main window
        self.main_window.show()

    def startup(self):
        if self._startup_method:
            self.main_window.content = self._startup_method(self)

    def main_loop(self):
        # Stimulate the build of the app
        self._startup()

        # Modify signal handlers to make sure Ctrl-C is caught and handled.
        signal.signal(signal.SIGINT, signal.SIG_DFL)

        self._impl.activateIgnoringOtherApps_(True)
        self._impl.run()
