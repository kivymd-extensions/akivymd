from kivy.lang.builder import Builder
from kivymd.uix.screen import MDScreen

Builder.load_string(
    """
<MyAKBarChart@AKBarChart>
    size_hint_y: None
    height: dp(180)
    x_values: [0, 5, 8, 15]
    y_values: [0, 10, 6, 8]
    label_size: dp(12)


<Barchart>
    on_leave: pass

    MDBoxLayout:
        orientation: "vertical"

        MyToolbar:
            id: _toolbar

        ScrollView:

            MDBoxLayout:
                orientation: "vertical"
                spacing: dp(25)
                padding: dp(25)
                adaptive_height: True

                MyAKBarChart:
                    id: chart1
                    labels: True
                    anim: True
                    lines: False
                    on_select: root.set_text(args)

                MyAKBarChart:
                    id: chart2
                    labels: False
                    anim: True
                    lines_color: [0, 0, 0.4, 1]
                    bars_color: [0, 0, 0.4, 1]
                    on_select: root.set_text(args)

                MyAKBarChart:
                    id: chart3
                    labels: True
                    anim: True
                    x_labels: ["XYZ", "Second", "Third", "Last"]
                    y_labels: ["XYZ", "Second", "Third", "Last"]
                    bars_color: 0.6, 0, 0, 1
                    labels_color: 0.6, 0, 0, 1
                    lines_color: 0.6, 0, 0, 1
                    on_select: root.set_text(args)


        MDBoxLayout:
            adaptive_height: True

            MDRaisedButton:
                text: "update"
                on_release: root.update()

            MDLabel:
                id: _label
                halign: "center"
                valign: "center"
"""
)


class Barchart(MDScreen):
    def set_text(self, args):
        self.ids._label.text = f"{args[1]} [{args[2]},{args[3]}]"

    def update(self):
        chart1 = self.ids.chart1
        chart1.x_values = [2, 8, 12, 35, 40, 43, 56]
        chart1.y_values = [3, 2, 1, 20, 0, 1, 10]
        chart1.update()

        chart2 = self.ids.chart2
        chart2.x_values = [2, 8, 12, 35, 40, 43, 56]
        chart2.y_values = [3, 2, 1, 20, 0, 1, 10]
        chart2.update()

        chart3 = self.ids.chart3
        chart3.x_labels = ["XYZ", "Second", "Third", "Last"]
        chart3.y_labels = ["XYZ", "Second", "Third", "Last"]
        chart3.update()
