from kivy.lang import Builder
from kivymd.uix.screen import MDScreen

Builder.load_string(
    """
<CardStack>:

    MyToolbar:
        id: _toolbar
        pos_hint: {"top": 1}

    AKCardStack:
        id: cardstack
        pos_hint: {"center_x": .5, "center_y": .5}
        size: dp(800), dp(800)
        transition: "in_out_circ"
        card_out_direction: "left"
        card_in_direction: "bottom"

    MDRaisedButton:
        text: "change cards"
        on_press: root.change()
        pos_hint: {"center_x": .5, "y": .05}
"""
)


class CardStack(MDScreen):
    def change(self):
        self.ids.cardstack.change()
