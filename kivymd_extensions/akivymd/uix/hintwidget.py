from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang.builder import Builder
from kivy.properties import (
    BooleanProperty,
    NumericProperty,
    OptionProperty,
    StringProperty,
)
from kivy.uix.boxlayout import BoxLayout

Builder.load_string(
    """
<AKHintWidgetItem>
    pos: self.parent.pos


<AKHintWidget>:
    FloatLayout:
        pos: root.pos
        size: root.size

        FloatLayout:
            id: _float_box
            # pos: root._hintwidget_x, root._hintwidget_y
            size_hint: None, None
            size: root.hintwidget_width, root.hintwidget_height
            opacity: root._hintwidget_alpha
"""
)


class AKHintWidgetItem(BoxLayout):
    pass


class AKHintWidget(BoxLayout):

    hintwidget_width = NumericProperty("150dp")
    hintwidget_height = NumericProperty("150dp")
    opacity_duration = NumericProperty(0.2)
    transition = StringProperty("out_quad")
    offset_x = NumericProperty("10dp")
    offset_y = NumericProperty("10dp")
    show_mode = OptionProperty("touch", options=["touch", "hover"])
    hintwidget_pos = OptionProperty("tr", options=["tr", "tl", "br", "bl"])
    auto_dismiss = BooleanProperty(True)
    open_button = OptionProperty("left", options=["left", "right"])
    show_delay = NumericProperty(0)
    _hintwidget_x = NumericProperty()
    _hintwidget_y = NumericProperty()
    _hintwidget_alpha = NumericProperty(0)
    _opac_anim_started = False
    _state = "close"

    def __init__(self, **kwargs):
        super(AKHintWidget, self).__init__(**kwargs)
        Clock.schedule_once(lambda x: self._update())

    def _update(self):
        if self.show_mode == "hover":
            Window.bind(mouse_pos=self._show_hover)
        elif self.show_mode == "touch":
            Window.unbind(mouse_pos=self._show_hover)

        self.bind(_hintwidget_x=self.ids._float_box.setter("x"))
        self.bind(_hintwidget_y=self.ids._float_box.setter("y"))

    def _right_top_hint(self):
        return (self._hintwidget_x, self._hintwidget_y)

    def _show_hover(self, instance, pos):
        if self.collide_point(pos[0], pos[1]):
            self._set_hintwidget_pos(pos)
            Clock.schedule_once(
                lambda x: self._change_opacity(1), self.show_delay
            )
            self._state = "open"
        else:
            self._change_opacity(0)
            self._state = "close"

    @property
    def state(self):
        return self._state

    def _set_hintwidget_pos(self, pos):
        space_x = self.hintwidget_width + self.offset_x
        space_y = self.hintwidget_height + self.offset_y
        image_top = self.y + self.height
        image_right = self.x + self.width
        image_left = self.x
        image_bottom = self.y

        if self.hintwidget_pos == "tr":
            mag_right = pos[0] + space_x
            mag_top = pos[1] + space_y
            mag_left = pos[0]
            mag_bottom = pos[1]

        if self.hintwidget_pos == "br":
            mag_right = pos[0] + space_x
            mag_top = pos[1]
            mag_left = pos[0]
            mag_bottom = pos[1] - space_y

        if self.hintwidget_pos in "tl":
            mag_right = pos[0]
            mag_top = pos[1] + space_y
            mag_left = pos[0] - space_x
            mag_bottom = pos[1]

        if self.hintwidget_pos in "bl":
            mag_right = pos[0]
            mag_top = pos[1]
            mag_left = pos[0] - space_x
            mag_bottom = pos[1] - space_y

        # ===============
        if mag_right >= image_right:
            self._hintwidget_x = pos[0] - self.offset_x - self.hintwidget_width
        elif mag_left <= image_left:
            self._hintwidget_x = pos[0] + self.offset_x
        else:
            if self.hintwidget_pos in ["tr", "br"]:
                self._hintwidget_x = pos[0] + self.offset_x
            elif self.hintwidget_pos in ["tl", "bl"]:
                self._hintwidget_x = (
                    pos[0] - self.offset_x - self.hintwidget_width
                )

        if mag_top >= image_top:
            self._hintwidget_y = pos[1] - self.offset_y - self.hintwidget_height
        elif mag_bottom <= image_bottom:
            self._hintwidget_y = pos[1] + self.offset_y
        else:
            if self.hintwidget_pos in ["tr", "tl"]:
                self._hintwidget_y = pos[1] + self.offset_y
            elif self.hintwidget_pos in ["bl", "br"]:
                self._hintwidget_y = (
                    pos[1] - self.offset_y - self.hintwidget_height
                )

        # ===============
        if pos[0] > image_right:
            self._hintwidget_x = image_right - space_x

        if pos[0] < image_left:
            self._hintwidget_x = image_left + self.offset_x

        if pos[1] > image_top:
            self._hintwidget_y = image_top - space_y

        if pos[1] < image_bottom:
            self._hintwidget_y = image_bottom + self.offset_y

    def _change_opacity(self, opacity):
        if not self._opac_anim_started:
            anim = Animation(
                _hintwidget_alpha=opacity,
                duration=self.opacity_duration,
                t=self.transition,
            )
            anim.start(self)
            self._opac_anim_started = True
            Clock.schedule_once(
                lambda x: self._allow_opac_animation(), self.opacity_duration
            )

    def _allow_opac_animation(self):
        self._opac_anim_started = False

    def on_touch_down(self, touch):
        pos = touch.pos
        if self.show_mode == "touch" and self.collide_point(pos[0], pos[1]):

            if self._state == "open" and not self.ids._float_box.collide_point(
                pos[0], pos[1]
            ):
                opac = 0
                self._state = "close"
            elif touch.button == self.open_button:
                if not self.ids._float_box.collide_point(pos[0], pos[1]):
                    self._set_hintwidget_pos(pos)
                opac = 1
                self._state = "open"
            else:
                return super().on_touch_down(touch)
            Clock.schedule_once(
                lambda x: self._change_opacity(opac), self.show_delay
            )

        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        if self.show_mode == "touch":
            if not self.auto_dismiss and self._state == "open":
                opac = 1
            else:
                opac = 0
                self._state = "close"
            Clock.schedule_once(
                lambda x: self._change_opacity(opac), self.opacity_duration
            )

        return super().on_touch_up(touch)

    def on_touch_move(self, touch):
        pos = touch.pos
        if self.show_mode == "touch":
            self._set_hintwidget_pos(pos)
        return super().on_touch_move(touch)

    def add_widget(self, widget, index=0, canvas=None):
        if issubclass(widget.__class__, AKHintWidgetItem):
            self.ids._float_box.add_widget(widget)
        else:
            super().add_widget(widget, index=index, canvas=canvas)
