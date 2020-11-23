from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen

from kivymd_extensions.akivymd.uix.datepicker import AKDatePicker

Builder.load_string(
    """
<DatePicker>:
    on_leave: date.text = ""

    MDBoxLayout:
        orientation: "vertical"

        MyToolbar:
            id: _toolbar

        MDFloatLayout:

            MDRaisedButton:
                text: "Open"
                on_release: root.open()
                pos_hint: {"center_x": .5, "center_y": .5}

            MDLabel:
                id: date
                text: ""
                halign: "center"
                valign: "center"
                size_hint_y: 0.2
                pos_hint: {"center_x": .5, "center_y": .3}
"""
)


class DatePicker(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.date = AKDatePicker(callback=self.callback)

    def callback(self, date):
        if not date:
            return

        self.ids.date.text = "%d / %d / %d" % (date.day, date.month, date.year)

    def open(self):
        self.date.open()
