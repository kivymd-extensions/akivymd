from kivy.animation import Animation
from kivy.lang import Builder
from kivy.properties import NumericProperty, ObjectProperty, StringProperty
from kivy.uix.scatter import Scatter
from kivymd.uix.dialog import BaseDialog

Builder.load_string(
    """
<Navigation_button@MDIconButton>
    theme_text_color: "Custom"
    text_color: 1, 1, 1, 1


<AKImageViewerItem>:
    id: scatter
    do_rotation: False
    Image:
        id: _image
        size_hint: None, None
        size: scatter.size
        source: root.source

<AKImageViewer>:
    id: _mainbox
    size_hint: (0.9, 0.4) if root.theme_cls.device_orientation == "portrait" else (0.9, 0.7)
    carousel: carousel

    FloatLayout:
        Navigation_button:
            id: _left_button
            pos_hint: {"x": 0 , "center_y": .5}
            icon: "chevron-left"
            on_release:
                root._previous_slide()
                root._reset_current_slide()

        Navigation_button:
            id: _right_button
            icon: "chevron-right"
            pos_hint: {"right": 1, "center_y": .5}
            on_release:
                root._next_slide()
                root._reset_current_slide()

        Carousel:
            id: carousel
            size_hint: None,None
            size: _mainbox.size[0]-2 * _left_button.size[0], _mainbox.size[1]
            pos_hint: {"center_x": .5, "center_y": .5}
            scroll_distance: dp(9999)
            min_move: 0
"""
)


class AKImageViewerItem(Scatter):
    zoom_max = NumericProperty(2)
    bounce_duration = NumericProperty(0.3)
    bounce_animation = StringProperty("out_cubic")
    source = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.zoom_max_exceeded = False
        self.zoom_min_exceeded = False
        self.zoom_min = 1
        self.scale = self.zoom_min

    def on_touch_down(self, touch):
        if touch.is_double_tap:
            if self.scale == self.zoom_min:
                self.reset_max_zoom()
            elif self.zoom_max >= self.scale > self.zoom_min:
                self.reset_min_zoom()

        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        if self.zoom_max_exceeded:
            self.reset_max_zoom()

        if self.zoom_min_exceeded:
            self.reset_min_zoom()

        self.zoom_max_exceeded = False
        self.zoom_min_exceeded = False
        return super().on_touch_up(touch)

    def on_touch_move(self, touch):
        super().on_touch_move(touch)
        if self.scale > self.zoom_max:
            self.zoom_max_exceeded = True
        else:
            self.zoom_max_exceeded = False

        if self.scale < self.zoom_min:
            self.zoom_min_exceeded = True
        else:
            self.zoom_min_exceeded = False

    def reset_max_zoom(self):
        max_zoom_anim = Animation(
            scale=self.zoom_max,
            duration=self.bounce_duration,
            t=self.bounce_animation,
        )
        max_zoom_anim.start(self)

    def reset_position(self):
        position_anim = Animation(
            pos=(0, 0), duration=self.bounce_duration, t=self.bounce_animation
        )
        position_anim.start(self)

    def reset_min_zoom(self):
        min_zoom_anim = Animation(
            scale=self.zoom_min,
            duration=self.bounce_duration,
            t=self.bounce_animation,
        )
        min_zoom_anim.start(self)
        self.reset_position()


class AKImageViewer(BaseDialog):
    carousel = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _next_slide(self):
        if len(self.carousel.slides) == 0:
            return

        if self.carousel.current_slide == self.carousel.slides[-1]:
            self.carousel.load_slide(self.carousel.slides[0])
        else:
            self.carousel.load_next(mode="next")

    def on_dismiss(self):
        self.carousel.load_slide(self.carousel.slides[0])
        self.carousel.current_slide.reset_min_zoom()
        self.carousel.current_slide.reset_position()

    def _previous_slide(self):
        if len(self.carousel.slides) == 0:
            return

        if self.carousel.current_slide == self.carousel.slides[0]:
            self.carousel.load_slide(self.carousel.slides[-1])
        else:
            self.carousel.load_previous()

    def _reset_current_slide(self):
        self.carousel.current_slide.reset_min_zoom()
        self.carousel.current_slide.reset_position()

    def add_widget(self, widget, index=0, canvas=None):
        if issubclass(widget.__class__, AKImageViewerItem):
            self.carousel.add_widget(widget)
        else:
            return super().add_widget(widget, index=index, canvas=canvas)
