from kivy.lang.builder import Builder
from kivymd.uix.screen import MDScreen

from kivymd_extensions.akivymd.uix.statusbarcolor import change_statusbar_color

Builder.load_string(
    """
<StatusbarColor>
    on_leave: root.change_color( app.theme_cls.primary_color , "Light" )

    MDBoxLayout:
        orientation: "vertical"

        MyToolbar:
            id: _toolbar

        MDFloatLayout:

            MDRaisedButton:
                text: "Red"
                on_release: root.change_color((1, 0, 0, 1), "Light")
                pos_hint: {"center_x": .5, "center_y": .1}

            MDRaisedButton:
                text: "Green"
                on_release: root.change_color((0, .7, 0, 1), "Light")
                pos_hint: {"center_x": .5, "center_y": .3}

            MDRaisedButton:
                text: "Blue"
                on_release: root.change_color((0, 0, 1, 1), "Light")
                pos_hint: {"center_x": .5, "center_y": .5}

            MDRaisedButton:
                text: "Yellow"
                on_release: root.change_color((1, 1, 0, 1), "Dark")
                pos_hint: {"center_x": .5, "center_y": .7}

            MDRaisedButton:
                text: "White"
                on_release: root.change_color((1, 1, 1, 1), "Dark")
                pos_hint: {"center_x": .5, "center_y": 0.9}
"""
)


class StatusbarColor(MDScreen):
    def change_color(self, color, mode):
        return change_statusbar_color(color, mode)
