from kivy.lang.builder import Builder
from kivy.metrics import dp
from kivymd.uix.screen import MDScreen

from kivymd_extensions.akivymd.uix.piechart import AKPieChart

Builder.load_string(
    """
<Piechart>
    on_leave: root.remove_chart()

    MDBoxLayout:
        orientation: "vertical"

        MyToolbar:
            id: _toolbar

        ScrollView:

            MDBoxLayout:
                id: chart_box
                adaptive_height: True
                padding:dp(24)
                orientation: "vertical"

        MDBoxLayout:
            adaptive_height: True
            padding: dp(5)
            spacing: dp(4)

            MDRaisedButton:
                text: "Update"
                on_release: root.update_chart()
"""
)


class Piechart(MDScreen):
    items = [{"Python": 40, "Java": 30, "C++": 10, "PHP": 8, "Ruby": 12}]

    def __init__(self, **kw):
        super().__init__(**kw)

    def on_enter(self):
        self.piechart = AKPieChart(
            items=self.items,
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            size_hint=[None, None],
            size=(dp(300), dp(300)),
        )
        self.ids.chart_box.add_widget(self.piechart)

    def update_chart(self):
        self.piechart.items = [{"Python": 70, "Dart": 10, "C#": 10, "Css": 10}]

    def remove_chart(self):
        self.ids.chart_box.remove_widget(self.piechart)
