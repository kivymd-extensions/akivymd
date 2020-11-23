import ast
import sys
from os import path

sys.path.append(path.join(path.abspath(__file__).rsplit("examples", 1)[0]))
from kivy.factory import Factory  # noqa
from kivy.lang import Builder  # noqa
from kivy.properties import StringProperty  # noqa
from kivymd.app import MDApp  # noqa
from kivymd.uix.list import OneLineAvatarListItem  # noqa
from kivymd.uix.toolbar import MDToolbar  # noqa

from kivymd_extensions.akivymd.uix.statusbarcolor import (  # noqa
    change_statusbar_color,
)

kv = """
#: import StiffScrollEffect kivymd.stiffscroll.StiffScrollEffect

<IconListItem@OneLineAvatarListItem>:

    IconLeftWidget:
        icon: root.icon

<MyToolbar@MDToolbar>:
    elevation: 10
    left_action_items: [["arrow-left", lambda x: app.show_screen("Home", "back")]]


MDScreen:

    ScreenManager:
        id: screen_manager

        MDScreen:
            name: "Home"

            Image:
                source: "assets/logo.png"
                opacity: .3

            MDBoxLayout:
                orientation: "vertical"

                MyToolbar:
                    title: app.title
                    left_action_items:[["menu" , lambda x: navdrawer.set_state("open")]]

                BoxLayout:
                    padding:dp(20)

                    MDLabel:
                        text: app.intro
                        theme_text_color: "Primary"
                        halign: "center"

    MDNavigationDrawer:
        id: navdrawer

        ScrollView:
            # effect_cls: StiffScrollEffect
            MDBoxLayout:
                orientation: "vertical"
                adaptive_height: True

                MDRelativeLayout:
                    size_hint_y: None
                    height: title_box.height

                    FitImage:
                        source: "assets/texture_blur.png"

                    MDBoxLayout:
                        id: title_box
                        adaptive_height: True
                        padding: dp(24)

                        MDLabel:
                            text: "Awesome KivyMD"
                            font_style: "H5"
                            size_hint_y: None
                            height: self.texture_size[1]
                            shorten: True

                MDList:
                    id: menu_list
"""


class IconListItem(OneLineAvatarListItem):
    icon = StringProperty()


class DemoApp(MDApp):

    intro = """Here is where you can find all of the widgets. take a look at
    screens folder to find examples of how to use them. I will gradually add
    more and more Awesome widgets to this project. Stay tuned!"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_cls.primary_palette = "Teal"
        self.title = "Awesome KivyMD"
        change_statusbar_color(self.theme_cls.primary_color)

    def build(self):
        self.root = Builder.load_string(kv)

    def on_start(self):
        with open(
            path.join(path.dirname(__file__), "screens.json")
        ) as read_file:
            self.data_screens = ast.literal_eval(read_file.read())
            data_screens = list(self.data_screens.keys())
            data_screens.sort()

        for list_item in data_screens:
            self.root.ids.menu_list.add_widget(
                IconListItem(
                    text=list_item,
                    icon=self.data_screens[list_item]["icon"],
                    on_release=lambda x=list_item: self.load_screen(x),
                )
            )

    def load_screen(self, screen_name):
        manager = self.root.ids.screen_manager
        screen_details = self.data_screens[screen_name.text]

        if not manager.has_screen(screen_details["screen_name"]):
            exec("from screens import %s" % screen_details["import"])
            screen_object = eval("Factory.%s()" % screen_details["factory"])
            screen_object.name = screen_details["screen_name"]
            manager.add_widget(screen_object)

            if "_toolbar" in screen_object.ids:
                screen_object.ids._toolbar.title = screen_name.text

        self.root.ids.navdrawer.set_state("close")
        self.show_screen(screen_details["screen_name"])

    def show_screen(self, name, mode=""):
        if mode == "back":
            self.root.ids.screen_manager.transition.direction = "right"
        else:
            self.root.ids.screen_manager.transition.direction = "left"
        self.root.ids.screen_manager.current = name
        return True


DemoApp().run()
