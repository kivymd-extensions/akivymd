from kivy.animation import Animation
from kivy.clock import Clock
from kivy.graphics import Color, Ellipse
from kivy.lang.builder import Builder
from kivy.properties import (
    BooleanProperty,
    ListProperty,
    NumericProperty,
    OptionProperty,
    StringProperty,
)
from kivy.uix.boxlayout import BoxLayout
from kivy.utils import get_color_from_hex
from kivymd.color_definitions import colors, palette
from kivymd.theming import ThemableBehavior
from kivymd.uix.label import MDLabel

from kivymd_extensions.akivymd.helper import point_on_circle

"""issues
color_mode
"""

Builder.load_string(
    """
<PieChartNumberLabel>
    size_hint: None, None
    size: dp(40), dp(30)
    text: "%s\\n%d%%" % (root.title, root.percent)
    font_size: dp(10)
    halign: "center"
    valign: "center"
    font_style: "Caption"
    theme_text_color: "Custom"
    text_color: 1, 1, 1, 1


<AKPieChart>:
"""
)


class PieChartNumberLabel(MDLabel):
    percent = NumericProperty(0)
    title = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(lambda x: self._update())

    def _update(self):
        self.x -= self.width / 2
        self.y -= self.height / 2


class AKPieChart(ThemableBehavior, BoxLayout):
    items = ListProperty()
    order = BooleanProperty(True)
    starting_animation = BooleanProperty(True)
    transition = StringProperty("out_cubic")
    duration = NumericProperty(1)
    color_mode = OptionProperty(
        "colors", options=["primary_color", "accent_color"]
    )  # not solved

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _format_items(self, items):
        percentage_sum = 0
        for k, v in items[0].items():
            percentage_sum += v

        if percentage_sum != 100:
            raise Exception("Sum of percenages must be 100")

        new_items = {}
        for k, v in items[0].items():
            new_items[k] = 360 * v / 100

        if self.order:
            new_items = {
                k: v
                for k, v in sorted(new_items.items(), key=lambda item: item[1])
            }

        return new_items

    def _make_chart(self, items):
        self.size = (min(self.size), min(self.size))
        if not items:
            raise Exception("Items cannot be empty.")

        items = self._format_items(items)
        angle_start = 0
        color_item = 0
        circle_center = [
            self.pos[0] + self.size[0] / 2,
            self.pos[1] + self.size[1] / 2,
        ]

        for title, value in items.items():
            with self.canvas.before:

                if self.starting_animation:
                    alpha = 0
                else:
                    alpha = 1

                if self.color_mode == "colors":
                    color = get_color_from_hex(
                        colors[palette[color_item]]["500"]
                    )

                c = Color(rgb=color, a=alpha)
                if self.starting_animation:
                    e = Ellipse(
                        pos=self.pos,
                        size=self.size,
                        angle_start=angle_start,
                        angle_end=angle_start + 0.01,
                    )

                    anim = Animation(
                        size=self.size,
                        angle_end=angle_start + value,
                        duration=self.duration,
                        t=self.transition,
                    )
                    anim_opcity = Animation(a=1, duration=self.duration * 0.5)

                    anim_opcity.start(c)
                    anim.start(e)
                else:
                    Ellipse(
                        pos=self.pos,
                        size=self.size,
                        angle_start=angle_start,
                        angle_end=angle_start + value,
                    )
            color_item += 1
            angle_start += value

        angle_start = 0
        for title, value in items.items():
            with self.canvas.after:
                label_pos = point_on_circle(
                    (angle_start + angle_start + value) / 2,
                    circle_center,
                    self.size[0] / 3,
                )
                number_anim = PieChartNumberLabel(
                    x=label_pos[0], y=label_pos[1], title=title
                )
                Animation(percent=value * 100 / 360).start(number_anim)

            angle_start += value

    def _clear_canvas(self):
        try:
            self.canvas.before.clear()
            self.canvas.after.clear()
        except BaseException:
            pass

    def on_pos(self, *args):
        self._clear_canvas()
        Clock.schedule_once(lambda x: self._make_chart(self.items))

    def on_items(self, *args):
        self._clear_canvas()
        Clock.schedule_once(lambda x: self._make_chart(self.items))
