from kivy.lang.builder import Builder
from kivymd.uix.screen import MDScreen

Builder.load_string(
    """
<MyAKLineChart@AKLineChart>
    size_hint_y: None
    height: dp(180)
    x_values: [0, 5, 8, 15]
    y_values: [0, 10, 6, 8]
    label_size: dp(12)


<Linechart>
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

                MyAKLineChart:
                    id: chart1
                    labels: False
                    anim: True
                    bg_color: 0.6, 0, 0, 1
                    circles_color: [0.4, 0.4, 1, 1]
                    labels: True
                    on_select: root.set_text(args)

                MyAKLineChart:
                    id: chart2
                    labels: False
                    anim: True
                    on_select: root.set_text(args)

                MyAKLineChart:
                    id: chart3
                    labels: True
                    anim: True
                    lines: False
                    on_select: root.set_text(args)

                MyAKLineChart:
                    id: chart4
                    labels: True
                    anim: True
                    lines: False
                    x_labels: ["XYZ", "Second", "Third", "Last"]
                    y_labels: ["XYZ", "Second", "Third", "Last"]
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


class Linechart(MDScreen):
    def set_text(self, args):
        self.ids._label.text = f"{args[1]} [{args[2]},{args[3]}]"

    def update(self):
        chart1 = self.ids.chart1
        chart1.x_values = [2, 8, 12, 35, 40, 43, 56]
        chart1.y_values = [3, 2, 1, 16, 0, 1, 10]
        chart1.update()

        chart2 = self.ids.chart2
        chart2.x_values = [2, 8, 12, 35, 40, 43, 56]
        chart2.y_values = [3, 2, 1, 15, 0, 1, 10]
        chart2.update()

        chart3 = self.ids.chart3
        chart3.x_values = [2, 8, 12, 35, 40, 43, 56]
        chart3.y_values = [3, 2, 1, 15, 0, 1, 10]
        chart3.update()

        chart4 = self.ids.chart4
        chart4.x_labels = ["XYZ", "Second", "Third", "Last"]
        chart4.y_labels = ["XYZ", "Second", "Third", "Last"]
        chart4.update()
