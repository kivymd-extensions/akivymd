from kivy.lang.builder import Builder
from kivymd.uix.label import MDIcon, MDLabel
from kivymd.uix.screen import MDScreen

from kivymd_extensions.akivymd.uix.behaviors.labelanimation import (
    AKAnimationIconBehavior,
    AKAnimationTextBehavior,
)

Builder.load_string(
    """
<LabelAnimation>:

    MDBoxLayout:
        orientation: "vertical"

        MyToolbar:
            id: _toolbar

        MDFloatLayout:

            MyMDIcon:
                id: icon
                icon: "arrow-left"
                pos_hint: {"center_x": .5, "center_y": .4}
                halign: "center"
                font_size: dp(100)
                size_hint: None, None
                size: dp(100), dp(100)
                theme_text_color: "Primary"

            MyMDLabel:
                id: text
                text: "arrow-left"
                pos_hint: {"center_x": .5, "center_y": .6}
                halign: "center"
                font_size: dp(20)
                size_hint: None, None
                size: dp(100), dp(100)
                theme_text_color: "Primary"

            MDRaisedButton:
                text: "Press"
                pos_hint: {"center_x": .5, "center_y": .1}
                on_release:
                    if text.text== "menu":  text.text="arrow-left"
                    else: text.text="menu"
                    if icon.icon== "menu":  icon.icon="arrow-left"
                    else: icon.icon="menu"
"""
)


class LabelAnimation(MDScreen):
    pass


class MyMDIcon(MDIcon, AKAnimationIconBehavior):
    pass


class MyMDLabel(MDLabel, AKAnimationTextBehavior):
    pass
