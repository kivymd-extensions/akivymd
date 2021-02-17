from datetime import datetime

from kivy.lang import Builder
from kivy.properties import ListProperty, OptionProperty, StringProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivymd.theming import ThemableBehavior
from kivymd.uix.behaviors import RectangularRippleBehavior
from kivymd.uix.dialog import BaseDialog

Builder.load_string(
    """
<MDLabeltitle2@MDLabel>:
    theme_text_color: "Custom"
    text_color: 1, 1, 1, 1
    halign: "center"
    vlighn: "center"
    fon_style: "H5"


<MDLabeltitle@MDLabel>
    theme_text_color: "Primary"
    halign: "center"
    vlighn: "center"
    fon_style: "Caption"


<ButtonBase>
    size_hint_y: None
    height: dp(40)
    MDLabel:
        id: value
        text: root.text
        theme_text_color: "Primary"
        halign: "center"
        vlighn: "center"

<AKDatePicker>:
    size_hint: None, None
    size:
        (dp(302), dp(450)) \
        if root.theme_cls.device_orientation == "portrait" \
        else (dp(450), dp(350))

    BoxLayout:
        orientation: "vertical"
        canvas.before:
            Color:
                rgba: root.theme_cls.bg_normal
            RoundedRectangle:
                size: self.size
                pos: self.pos

        BoxLayout:
            size_hint_y: None
            height: dp(50)
            canvas.before:
                Color:
                    rgba: root.theme_cls.primary_color
                RoundedRectangle:
                    size: self.size
                    pos: self.pos
                    radius:[(10.0, 10.0), (10.0, 10.0), (0, 0), (0, 0)]

            MDLabeltitle2:
                text: root._year_title

            MDLabeltitle2:
                text: root._month_title

            MDLabeltitle2:
                text: root._day_title

        BoxLayout:
            size_hint_y: None
            height: dp(50)
            canvas.before:
                Color:
                    rgba: root.theme_cls.bg_dark
                Rectangle:
                    size: self.size
                    pos: self.pos

            MDLabeltitle:
                text: "Year"

            MDLabeltitle:
                text: "Month"

            MDLabeltitle:
                text: "Day"


        BoxLayout:
            ScrollView:
                MDBoxLayout:
                    id: year_view
                    orientation: "vertical"
                    adaptive_height: True
            ScrollView:
                MDBoxLayout:
                    id: month_view
                    orientation: "vertical"
                    adaptive_height: True
            ScrollView:
                MDBoxLayout:
                    id: day_view
                    orientation: "vertical"
                    adaptive_height: True
        BoxLayout:
            size_hint_y: None
            height: dp(40)
            padding: [dp(10), 0]
            spacing: dp(10)
            canvas.before:
                Color:
                    rgba: root.theme_cls.bg_dark
                RoundedRectangle:
                    size: self.size
                    pos: self.pos
                    radius: [(0.0, 10.0), (0.0, 10.0), (10, 10), (10, 10)]

            MDFlatButton:
                text: "Cancel"
                pos_hint: {"center_x": .5, "center_y": .5}
                on_release: root.cancel()

            MDFlatButton:
                text: "Select"
                pos_hint: {"center_x": .5, "center_y": .5}
                on_release: root._choose()
"""
)


class AKDatePicker(BaseDialog, ThemableBehavior):

    year_range = ListProperty([1930, 2021])
    month_type = OptionProperty("string", options=["string", "int"])
    _day_title = StringProperty("-")
    _month_title = StringProperty("-")
    _year_title = StringProperty("-")

    def __init__(self, callback=None, **kwargs):
        super(AKDatePicker, self).__init__(**kwargs)
        self.month_dic = {
            "1": "January",
            "2": "February",
            "3": "March",
            "4": "April",
            "5": "May",
            "6": "June",
            "7": "July",
            "8": "August",
            "9": "September",
            "10": "October",
            "11": "November",
            "12": "December",
        }

        self.callback = callback
        for x in reversed(range(self.year_range[0], self.year_range[1])):
            self.ids.year_view.add_widget(
                ButtonBase(text="%d" % x, on_release=self._set_year)
            )
        for x in reversed(range(1, 13)):
            if self.month_type == "string":
                month = self.month_dic[str(x)]
            else:
                month = str(x)

            self.ids.month_view.add_widget(
                ButtonBase(text=month, on_release=self._set_month)
            )
        for x in reversed(range(1, 32)):
            self.ids.day_view.add_widget(
                ButtonBase(text="%d" % x, on_release=self._set_day)
            )

    def _set_day(self, instance):
        self._day_title = instance.text

    def _set_month(self, instance):
        self._month_title = instance.text

    def _set_year(self, instance):
        self._year_title = instance.text

    def on_dismiss(self):
        self._year_title = "-"
        self._month_title = "-"
        self._day_title = "-"
        return

    def _choose(self):
        if not self.callback:
            return False

        if self.month_type == "string":
            for k, v in self.month_dic.items():
                if v == self._month_title:
                    self._month_title = k
                    break

        try:
            date = datetime(
                int(self._year_title),
                int(self._month_title),
                int(self._day_title),
            )
        except BaseException:
            date = False

        self.callback(date)
        self.cancel()

    def cancel(self):
        self.dismiss()


class ButtonBase(RectangularRippleBehavior, ButtonBehavior, BoxLayout):
    text = StringProperty()
