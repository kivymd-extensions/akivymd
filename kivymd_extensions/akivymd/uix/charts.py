from kivy.animation import Animation
from kivy.clock import Clock
from kivy.graphics import Color, Ellipse
from kivy.lang.builder import Builder
from kivy.properties import (
    BooleanProperty,
    ColorProperty,
    ListProperty,
    NumericProperty,
    ObjectProperty,
    OptionProperty,
    StringProperty,
)
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.utils import get_color_from_hex
from kivymd.color_definitions import colors, palette
from kivymd.theming import ThemableBehavior
from kivymd.uix.label import MDLabel

from kivymd_extensions.akivymd.helper import point_on_circle
from kivymd_extensions.akivymd.utils.draw_tools import DrawTools

"""issues
color_mode
"""

__all__ = (
    "AKPieChart",
    "AKLineChart",
    "AKBarChart",
)

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


<AKChartLabel>
    theme_text_color: "Custom"
    text_color: root._owner.labels_color if root._owner else [1, 1, 1, 1]
    halign: "center"
    valign: "center"
    adaptive_width: True
    size_hint_y: None


<AKChartBase>
    padding: dp(30)
    _labels_y_box: _labels_y_box
    _labels_x_box: _labels_x_box
    _canvas: _canvas
    target_canvas: _canvas.canvas.after

    # Layout to draw main shapes
    BoxLayout:
        id: _canvas
        canvas.before:
            Color:
                rgba: root.bg_color if root.bg_color else root.theme_cls.primary_color
            RoundedRectangle:
                pos: self.pos
                size: root.size
                radius: root.radius if root.radius else [dp(5), ]

    # Y axis labels
    RelativeLayout:
        id: _labels_y_box

    # X axis labels
    RelativeLayout:
        id: _labels_x_box


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
        for item in items:                          #Adding all Percentage Values
            for k, v in item.items():
                percentage_sum += v

        if percentage_sum != 100:
            raise Exception("Sum of percenages must be 100")

        new_items = {}
        for item in items:                          #Adding all items in new_items Dict
            for k, v in item.items():
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


class AKChartLabel(MDLabel):
    _owner = ObjectProperty()
    _mypos = ListProperty([0, 0])


class AKChartBase(DrawTools, ThemableBehavior, RelativeLayout):
    x_values = ListProperty([])
    x_labels = ListProperty([])
    y_values = ListProperty([])
    y_labels = ListProperty([])
    bg_color = ColorProperty(None, allownone=True)
    radius = ListProperty(None, alllownone=True)
    anim = BooleanProperty(True)
    d = NumericProperty(1)
    t = StringProperty("out_quad")
    labels = BooleanProperty(True)
    labels_color = ColorProperty([1, 1, 1, 1])
    label_size = NumericProperty("15dp")
    bars_color = ColorProperty([1, 1, 1, 1])
    line_width = NumericProperty("2dp")
    lines_color = ColorProperty([1, 1, 1, 1])
    lines = BooleanProperty(True)
    trim = BooleanProperty(True)
    _loaded = NumericProperty(1)
    _labels_y_box = ObjectProperty()
    _labels_x_box = ObjectProperty()
    _canvas = ObjectProperty()

    def __init__(self, **kw):
        super().__init__(**kw)
        self._myinit = True
        self.bind(
            _loaded=lambda *args: self._update(anim=True),
        )
        Clock.schedule_once(self.update)

    def _get_normalized_cor(self, val, mode, f_update=1):
        x_values = self.x_values
        y_values = self.y_values
        trim = self.trim
        padding = self.padding
        size = self.size
        min_x = min(x_values) if trim else 0
        max_x = max(x_values)
        min_y = min(y_values) if trim else 0
        max_y = max(y_values)
        x_distance = (max_x - min_x) if trim else max_x
        y_distance = (max_y - min_y) if trim else max_y

        if mode == "x":
            _min = min_x
            _distance = x_distance
            _size = size[0]
            f_update = 1
        else:
            _min = min_y
            _distance = y_distance
            _size = size[1]

        res = ((val - _min) / _distance) * (
            _size - self._bottom_line_y() - padding
        )
        return f_update * res + self._bottom_line_y()

    def do_layout(self, *args, **kwargs):
        super().do_layout(*args, **kwargs)
        self._update()

    def update(self, *args):
        self._myinit = True
        if self.anim:
            self._loaded = 0
            anim = Animation(_loaded=1, t=self.t, d=self.d)
            anim.start(self)
        else:
            self._update()
            self._update()

    def _update(self, anim=False, *args):
        x_values = self.x_values
        y_values = self.y_values
        x_labels = self.x_labels
        y_labels = self.y_labels
        canvas = self._canvas.canvas
        canvas.clear()
        canvas.after.clear()
        if self._myinit:
            self._labels_y_box.clear_widgets()
            self._labels_x_box.clear_widgets()

        dis = self._bottom_line_y()
        self.draw_shape(
            "line",
            shape_name="line",
            canvas=canvas,
            points=[
                [dis, dis],
                [self.width - dis, dis],
            ],
            line_width=self.line_width,
            color=self.lines_color,
        )

        if not x_values or not y_values:
            raise Exception("x_values and y_values cannot be empty")

        if len(x_values) != len(y_values):
            raise Exception("x_values and y_values must have equal length")

        if (
            ((len(x_labels) != len(y_values)) and len(x_labels) > 0)
            or (len(y_labels) != len(y_values))
            and len(y_labels) > 0
        ):
            raise Exception(
                "x_values and y_values and x_labels must have equal length"
            )

    def _bottom_line_y(self):
        return self.label_size * 2

    def draw_label(self, text_x, text_y, center_pos_x, center_pos_y, idx):
        labels_y_box = self._labels_y_box
        labels_x_box = self._labels_x_box
        if self._myinit:
            label_y = AKChartLabel(
                text=text_y,
                center=center_pos_y,
                _owner=self,
                height=self.label_size * 2,
            )
            label_y.font_size = self.label_size
            label_x = AKChartLabel(
                text=text_x,
                center=center_pos_x,
                _owner=self,
                height=self.label_size * 2,
            )
            label_x.font_size = self.label_size
            labels_y_box.add_widget(label_y)
            labels_x_box.add_widget(label_x)
        else:
            child_y = labels_y_box.children[idx]
            child_x = labels_x_box.children[idx]
            child_y.center_x = center_pos_y[0]
            child_y.y = center_pos_y[1]
            child_x.center_x = center_pos_x[0]
            child_x.y = center_pos_x[1]


class AKLineChart(AKChartBase):
    circles_color = ColorProperty([1, 1, 1, 1])
    circles_radius = NumericProperty("15dp")
    circles = BooleanProperty(True)

    def _update(self, anim=False, *args):
        super()._update()
        x_values = self.x_values
        y_values = self.y_values
        canvas = self._canvas.canvas
        f_update = self._loaded if anim else 1
        drawer = self.draw_shape
        last_point = False

        for i in range(0, len(x_values)):
            x = x_values[i]
            x_label = self.x_labels[i] if self.x_labels else False
            y_label = self.y_labels[i] if self.y_labels else False
            y = y_values[i]
            new_x = self._get_normalized_cor(x, "x", f_update)
            new_y = self._get_normalized_cor(y, "y", f_update)
            if self.circles:
                drawer(
                    "circle",
                    shape_name="circle",
                    canvas=canvas.after,
                    color=self.circles_color,
                    size=[self.circles_radius, self.circles_radius],
                    center_pos=[new_x, new_y],
                )
            if last_point and self.lines:
                drawer(
                    "line",
                    shape_name="line",
                    canvas=canvas,
                    points=[last_point, [new_x, new_y]],
                    line_width=self.line_width,
                    color=self.lines_color,
                )
            last_point = [new_x, new_y]

            if self.labels:
                y_pos = [
                    new_x,
                    new_y + self.circles_radius / 2,
                ]
                x_pos = [new_x, 0]
                self.draw_label(
                    text_x=x_label if x_label else str(x),
                    text_y=y_label if y_label else str(y),
                    center_pos_x=x_pos,
                    center_pos_y=y_pos,
                    idx=len(x_values) - i - 1,
                )
        self._myinit = False


class AKBarChart(AKChartBase):
    max_bar_width = NumericProperty("80dp")
    min_bar_width = NumericProperty("10dp")
    bars_spacing = NumericProperty("10dp")
    bars_radius = NumericProperty("5dp")
    bars_color = ColorProperty([1, 1, 1, 1])

    def _update(self, anim=False, *args):
        super()._update()
        x_values = self.x_values
        y_values = self.y_values
        canvas = self._canvas.canvas
        drawer = self.draw_shape
        # bottom line
        bottom_line_y = self._bottom_line_y()
        count = len(self.y_values)
        bars_x_list = self.get_bar_x(count)
        bar_width = self.get_bar_width()
        f_update = self._loaded if anim else 1
        for i in range(0, count):
            x = x_values[i]
            x_label = self.x_labels[i] if self.x_labels else False
            y_label = self.y_labels[i] if self.y_labels else False
            y = y_values[i]
            new_x = bars_x_list[i]
            new_y = self._get_normalized_cor(y, "y", f_update)
            drawer(
                "bars",
                shape_name="roundedRectangle",
                canvas=canvas.after,
                color=self.bars_color,
                radius=[self.bars_radius, self.bars_radius, 0, 0],
                size=[bar_width, new_y - bottom_line_y],
                pos=[new_x, bottom_line_y],
            )

            if self.labels:
                y_pos = [new_x + bar_width / 2, new_y]
                x_pos = [new_x + bar_width / 2, 0]
                self.draw_label(
                    text_x=x_label if x_label else str(x),
                    text_y=y_label if y_label else str(y),
                    center_pos_x=x_pos,
                    center_pos_y=y_pos,
                    idx=len(x_values) - i - 1,
                )
        self._myinit = False

    def get_bar_x(self, bar_count):
        bar_width = self.get_bar_width()
        total_width = (
            bar_width * bar_count
            + (bar_count - 1) * self.bars_spacing
            + self.label_size * 4
        )
        start_pos = (self.width - total_width) / 2
        x_list = []
        for x in range(0, bar_count):
            x_pos = (
                start_pos
                + (bar_width + self.bars_spacing) * x
                + self.label_size * 2
            )
            x_list.append(x_pos)
        return x_list

    def get_bar_width(self):
        bars_count = len(self.x_values)
        spacing = self.bars_spacing
        width = self.width
        bar_width = (
            width - (bars_count + 1) * spacing - self.label_size * 4
        ) / bars_count
        if bar_width > self.max_bar_width:
            return self.max_bar_width
        elif bar_width < self.min_bar_width:
            return self.min_bar_width
        else:
            return bar_width
