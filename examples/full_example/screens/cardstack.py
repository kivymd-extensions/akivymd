from kivy.lang import Builder
from kivymd.uix.screen import MDScreen

Builder.load_string(
"""
<CardStack>:
    AKCardStack:
        id:cardstack
        pos_hint:{'center_x':.5, 'center_y':.5}
        size: 800,800
        transition: 'in_out_circ'
    MDRaisedButton:
        text:'change cards'
        on_press:root.change()
        pos_hint: {"center_x": .1, "center_y": .5}
""")

class CardStack(MDScreen):
    def change(self):
        self.ids.cardstack.change()
