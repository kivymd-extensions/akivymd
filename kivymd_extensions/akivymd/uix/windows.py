from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang.builder import Builder
from kivy.properties import (
    BooleanProperty,
    ListProperty,
    NumericProperty,
    ObjectProperty,
    StringProperty,
)
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivymd.theming import ThemableBehavior
from kivymd.uix.behaviors import RectangularElevationBehavior

Builder.load_string(
    """
<HeaderButton>
    size_hint: None, None
    canvas.before:
        Color:
            rgba: root.button_color if root.button_color  else root.theme_cls.accent_color
        Ellipse:
            pos: self.pos
            size: self.size

    MDIcon:
        icon: root.button_icon
        halign: "center"
        valign: "center"
        theme_text_color: "Custom"
        text_color: root.button_text_color if root.button_text_color  else root.theme_cls.primary_color
        font_size: self.parent.height - dp(4)
        pos_hint: {"center_x": .5, "center_y": .5}


<AKFloatingWindowLayout>


<AKFloatingWindow>:
    orientation: "vertical"
    radius: [root.window_radius, ]
    WindowHeader:
        orientation: "vertical"
        id: header
        size_hint_y: None
        height: root.header_height
        canvas.before:
            Color:
                rgba: root.header_color_active if root._window_active else root.header_color_normal
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [root.window_radius, root.window_radius,0 ,0 ]

        BoxLayout:
            MDLabel:
                text: root.window_title
                valign: "center"
                halign: "left"
                padding: [dp(10), 0]
                font_size: root.title_font_size
                theme_text_color: "Custom"
                text_color: root.header_text_color if root.header_text_color else 1, 1, 1, 1

            MDBoxLayout:
                adaptive_width: True
                spacing: dp(3)
                padding: [dp(10), 0]
                HeaderButton:
                    size: header.height - dp(3), header.height - dp(3)
                    button_icon: root.max_button_icon
                    button_color: root.max_button_color if root.max_button_color else 0, 0, 1, 1
                    button_text_color: root.max_button_text_color if root.max_button_text_color else 1,1,1,1
                    pos_hint: {"center_x": .5, "center_y": .5}
                    on_release: root.maximize()

                HeaderButton:
                    size: header.height - dp(3), header.height - dp(3)
                    button_icon: root.exit_button_icon
                    button_color: root.exit_button_color if root.exit_button_color else 1, 0, 0, 1
                    button_text_color: root.exit_button_text_color if root.exit_button_text_color else 1,1,1,1
                    pos_hint: {"center_x": .5, "center_y": .5}
                    on_release: root.dismiss()

        MDSeparator:

    WindowContent:
        id: content
        canvas.before:
            Color:
                rgba: root.bg_color if root.bg_color else root.theme_cls.bg_dark
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [0, 0, root.window_radius, root.window_radius]
"""
)


class WindowHeader(ThemableBehavior, BoxLayout):
    pass


class WindowContent(BoxLayout):
    pass


class HeaderButton(ThemableBehavior, ButtonBehavior, BoxLayout):
    button_icon = StringProperty()
    button_color = ListProperty()
    button_text_color = ListProperty()


class AKFloatingWindow(
    ThemableBehavior, RectangularElevationBehavior, BoxLayout
):
    _window_active = BooleanProperty(False)
    header_height = NumericProperty("20dp")
    header_color_normal = ListProperty()
    header_color_active = ListProperty()
    header_text_color = ListProperty()
    title_font_size = NumericProperty("10dp")
    window_title = StringProperty()
    window_elevation = NumericProperty(10)
    fade_exit = BooleanProperty(True)
    fade_open = BooleanProperty(True)
    animation_transition = StringProperty("out_quad")
    animation_duration = NumericProperty(0.1)
    open_position = ListProperty()
    maximize_animation = BooleanProperty(True)
    minimize_animation = BooleanProperty(True)
    window_radius = NumericProperty("8dp")
    bg_color = ListProperty()

    exit_button_icon = StringProperty("close")
    exit_button_color = ListProperty()
    exit_button_text_color = ListProperty()
    max_button_icon = StringProperty("window-maximize")
    max_button_color = ListProperty()
    max_button_text_color = ListProperty()

    bottom_widget = ObjectProperty()
    left_widget = ObjectProperty()
    right_widget = ObjectProperty()
    top_widget = ObjectProperty()

    _state = "close"
    _maximized = False
    _resize_click_dis = NumericProperty("10dp")
    _allow_resize = False
    _size_before = False
    _pos_before = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(lambda x: self._update())

    @property
    def state(self):
        return self._state

    @property
    def maximized(self):
        return self._maximized

    def _update(self):
        if not self.header_color_active:
            self.header_color_active = self.theme_cls.primary_color
        if not self.header_color_normal:
            self.header_color_normal = self.theme_cls.primary_light

        self.elevation = self.window_elevation

        exit_pos = [-self.width, -self.height]
        self.pos = exit_pos
        self.opacity = 0
        self._state = "close"

    def _update_open_pos(self):
        self.open_position = [
            Window.size[0] / 2 - self.width / 2,
            Window.size[1] / 2 - self.height / 2,
        ]

    def add_widget(self, widget, index=0, canvas=None):
        if issubclass(widget.__class__, WindowContent) or issubclass(
            widget.__class__, WindowHeader
        ):
            return super().add_widget(widget, index=index, canvas=canvas)
        else:
            return self.ids.content.add_widget(widget)

    def dismiss(self):
        if self._state == "close":
            return

        exit_pos = [-self.width, -self.height]

        if self.fade_exit:
            (
                Animation(
                    opacity=0,
                    t=self.animation_transition,
                    duration=self.animation_duration,
                )
                + Animation(pos=exit_pos, duration=0)
            ).start(self)
        else:
            self.opacity = 0
            self.pos = exit_pos

        self._state = "close"

    def open(self):
        self.parent._bring_to_front(self)
        self.parent._update_header_color(self)
        self._update_open_pos()

        if self._state == "open":
            return

        if self.fade_open:
            anim = Animation(pos=self.open_position, duration=0) + Animation(
                opacity=1,
                t=self.animation_transition,
                duration=self.animation_duration,
            )
            anim.start(self)
        else:
            self.opacity = 1
            self.pos = self.open_position
        self._state = "open"

    def minimize_to_normal(self):
        pos = self._pos_before
        size = self._size_before

        if self.minimize_animation:
            anim = Animation(
                pos=pos,
                size=size,
                duration=self.animation_duration,
                t=self.animation_transition,
            )
            anim.start(self)
        else:
            self.pos = pos
            self.size = size
        self._maximized = False

    def maximize(self):
        if self._maximized:
            self.minimize_to_normal()
            return

        self._size_before = []
        self._pos_before = []
        self._size_before += [self.size[0], self.size[1]]
        self._pos_before += [self.pos[0], self.pos[1]]

        if not self.bottom_widget:
            y = 0
        else:
            y = self.bottom_widget.y + self.bottom_widget.height

        if not self.top_widget:
            top = Window.size[1]
        else:
            top = self.top_widget.y

        if not self.left_widget:
            x = 0
        else:
            x = self.left_widget.x + self.left_widget.width

        if not self.right_widget:
            right = Window.size[0]
        else:
            right = self.right_widget.x

        pos = [x, y]
        size = [right - x, top - y]
        if self.maximize_animation:
            anim = Animation(
                pos=pos,
                size=size,
                duration=self.animation_duration,
                t=self.animation_transition,
            )
            anim.start(self)
        else:
            self.pos = pos
            self.size = size

        self._maximized = True

    def on_touch_down(self, touch):
        touch_pos = touch.pos
        window_right = self.x + self.width
        window_bottom = self.y
        x = window_right - self._resize_click_dis
        right = window_right + self._resize_click_dis
        y = window_bottom - self._resize_click_dis
        top = window_bottom + self._resize_click_dis

        if x < touch_pos[0] < right and y < touch_pos[1] < top:
            self._allow_resize = True
            Window.set_system_cursor("size_nwse")
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        self._allow_resize = False
        Window.set_system_cursor("arrow")
        return super().on_touch_up(touch)

    def on_touch_move(self, touch):
        if self._allow_resize:
            touch_pos = touch.pos

            width = touch_pos[0] - self.x
            height = self.y + self.height - touch_pos[1]
            self.size = [width, height]
            self.pos = [self.x, touch_pos[1]]

        return super().on_touch_move(touch)


class AKFloatingWindowLayout(ThemableBehavior, FloatLayout):
    _allow_move = False
    _x_dist = None
    _y_dist = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(lambda x: self._update())

    def _update(self):
        top_window = self._get_top_window()
        self._update_header_color(top_window)

    def _update_header_color(self, top_window):
        windows = self.children
        for window in windows:
            window._window_active = False
        top_window._window_active = True

    def on_touch_down(self, touch):
        touch_pos = touch.pos

        clicked_window = self._get_clicked_window(touch_pos)
        top_window = self._get_top_window()
        header = top_window.ids.header

        if clicked_window == top_window and header.collide_point(
            touch_pos[0], touch_pos[1]
        ):
            self._allow_move = True
            self._x_dist = touch_pos[0] - top_window.pos[0]
            self._y_dist = touch_pos[1] - top_window.pos[1]

        if clicked_window and clicked_window != top_window:
            self._update_header_color(clicked_window)
            self._bring_to_front(clicked_window)
            return

        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        self._allow_move = False
        return super().on_touch_up(touch)

    def on_touch_move(self, touch):
        if self._allow_move:
            touch_pos = touch.pos
            top_window = self._get_top_window()
            top_window.pos = [
                touch_pos[0] - self._x_dist,
                touch_pos[1] - self._y_dist,
            ]
        return super().on_touch_move(touch)

    def _bring_to_front(self, window):
        if not window:
            return False

        temp_window = window
        self.remove_widget(window)
        self.add_widget(temp_window)

    def _get_top_window(self):
        return self.children[0]

    def _get_clicked_window(self, touch_pos):
        windows = self.children
        for window in windows:
            if window.collide_point(touch_pos[0], touch_pos[1]):
                return window
