import os
import sys

sys.path.append(os.path.dirname(__file__).split("akivymd")[0])

from kivy.factory import Factory
from kivymd.app import MDApp
from kivy.lang import Builder

from kivymd.uix.list import OneLineAvatarListItem

from akivymd.uix.statusbarcolor import change_statusbar_color

from screens import (
    bottomnavigation,
    spinners,
    dataloader,
    selectionlist,
    piechart,
    imageviewer,
    onboarding,
    progressbutton,
    silverappbar,
    badgelayout,
    addwidget,
    bottomappbar,
    labelanimation,
    statusbarcolor,
    datepicker,
    progresswidget,
    hintwidget,
    windows,
    navigationrail,
    dialogs,
    rating,
)


kv = """
<MyMenuItem@OneLineAvatarListItem>

    IconLeftWidget:
        icon: "language-python"


MDScreen:

    ScreenManager:
        id: sm

        MDScreen:
            name: "Home"

            Image:
                source: "assets/logo.png"
                opacity: .3

            MDBoxLayout:
                orientation: "vertical"

                MDToolbar:
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


class DemoApp(MDApp):

    screens = [
        "BottomNavigation",
        "Spinners",
        "Dataloader",
        "Selectionlist",
        "Piechart",
        "ImageViewer",
        "Onboarding",
        "ProgressButton",
        "SilverAppbar",
        "BadgeLayout",
        "AddWidgetBehavior",
        "BottomAppbar",
        "LabelAnimation",
        "StatusbarColor",
        "DatePicker",
        "ProgressWidget",
        "HintWidget",
        "Windows",
        "Navigationrail",
        "Dialogs",
        "Rating",
    ]
    screens.sort()
    intro = """Here is where you can find all of the widgets. take a look at 
    screens folder to find exmples of how to use them. I will gradually add 
    more and more Awesome widets to this project. Stay tuned!"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_cls.primary_palette = "Teal"
        self.title = "Awesome KivyMD"
        change_statusbar_color(self.theme_cls.primary_color)

    def build(self):
        self.mainkv = Builder.load_string(kv)
        return self.mainkv

    def on_start(self):
        for screen in self.screens:
            self.mainkv.ids.sm.add_widget(eval("Factory.%s()" % screen))

        for list_item in self.screens:
            self.mainkv.ids.menu_list.add_widget(
                MyMenuItem(text=list_item, on_release=self.list_menu_callback)
            )

    def list_menu_callback(self, instance):
        self.show_screen(instance.text)
        self.mainkv.ids.navdrawer.set_state("close")

    def show_screen(self, name, mode=""):
        if mode == "back":
            self.mainkv.ids.sm.transition.direction = "right"
        else:
            self.mainkv.ids.sm.transition.direction = "left"
        self.mainkv.ids.sm.current = name
        return True


class MyMenuItem(OneLineAvatarListItem):
    pass


DemoApp().run()
