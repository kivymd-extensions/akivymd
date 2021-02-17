from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang.builder import Builder
from kivy.metrics import dp
from kivy.properties import (
    BooleanProperty,
    ListProperty,
    NumericProperty,
    OptionProperty,
    StringProperty,
)
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivymd.theming import ThemableBehavior

Builder.load_string(
    """
<Button_Item>
    size_hint: None, None
    size: root.button_height, root.button_height
    pos_hint: {"center_x": .5, "center_y": .5}

    canvas.before:
        Color:
            rgba:
                root.button_bg_color if root.button_bg_color \
                else app.theme_cls.primary_light
            a: root._bg_opacity
        RoundedRectangle:
            size: self.size
            pos: self.pos
            radius: [self.height / 2, ]

    AKBadgeLayout:
        badgeitem_size: root.badgeitem_size
        bg_color: root.badge_bg_color
        badgeitem_padding: root.badgeitem_padding
        badgeitem_color: root.badgeitem_color
        position: root.badge_position
        text: root.badge_text
        bold: root.badge_bold
        offset: root.badge_offset
        badge_disabled: root.badge_disabled

        MDIcon:
            id: _icon
            icon: root.icon
            halign: "center"
            size_hint: None, None
            size: root.height, root.height
            font_size: root.icon_size
            theme_text_color: "Custom"
            text_color: root.icon_color if root.icon_color else app.theme_cls.primary_dark

    FloatLayout:
        id: _float
        size_hint_x: None
        width: root.width - _icon.width

        Label:
            id: _label
            text: root.text
            opacity: 0
            halign: "center"
            color:
                root.text_color if root.text_color \
                else app.theme_cls.primary_dark
            font_size: root.text_size
            size_hint: None, None
            size: self.texture_size
            pos_hint: {"center_y": .5}
            x: _float.x + (_float.width - _label.width) / 2  - (root.height - _icon.font_size) / 2

<AKBottomNavigation2>:
    size_hint: None, None
    height: root.bottomnavigation_height
    canvas.before:
        Color:
            rgba: root.bg_color if root.bg_color else app.theme_cls.bg_darkest
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [root.radius, root.radius, 0, 0]

    BoxLayout:
        id: _button_box
"""
)


class Button_Item(ThemableBehavior, ButtonBehavior, BoxLayout):
    transition = StringProperty("out_quad")
    duration = NumericProperty(0.3)
    button_bg_color = ListProperty(None)
    button_width = NumericProperty(dp(120))
    text_size = NumericProperty(dp(13))
    text_color = ListProperty(None)
    button_height = NumericProperty(dp(40))
    icon_size = NumericProperty(dp(20))
    icon_color = ListProperty(None)
    text = StringProperty()
    icon = StringProperty()
    mode = OptionProperty(
        "color_on_normal", options=["color_on_normal", "color_on_active"]
    )
    # ================
    badgeitem_size = NumericProperty(dp(20))
    badge_bg_color = ListProperty()
    badgeitem_padding = NumericProperty(dp(3))
    badgeitem_color = ListProperty()
    badge_position = StringProperty("right")
    badge_text = StringProperty("")
    badge_bold = BooleanProperty(False)
    badge_offset = NumericProperty(0.4)
    badge_disabled = BooleanProperty(False)

    _bg_opacity = NumericProperty(1)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_release(self):
        for button in self.parent.children:
            if button == self:
                continue
            button._button_shrink()

        self._button_expand()
        return super().on_release()

    def _button_expand(self):
        label_anim = Animation(
            opacity=1, transition=self.transition, duration=self.duration
        )
        label_anim.start(self.ids._label)

        anim = Animation(
            width=self.button_width,
            _bg_opacity=1,
            t=self.transition,
            duration=self.duration,
        )
        anim.start(self)

    def _button_shrink(self):
        if self.mode == "color_on_active":
            opacity = 0
        else:
            opacity = 1

        label_anim = Animation(
            opacity=0, transition=self.transition, duration=self.duration
        )
        label_anim.start(self.ids._label)

        but_anim = Animation(
            width=self.height,
            _bg_opacity=opacity,
            t=self.transition,
            duration=self.duration,
        )
        but_anim.start(self)


class AKBottomNavigation2(ThemableBehavior, BoxLayout):
    bottomnavigation_height = NumericProperty("65dp")
    radius = NumericProperty("20dp")
    bg_color = ListProperty(None)
    elelevation = NumericProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_resize=self._update)
        Clock.schedule_once(lambda x: self.set_current(None))
        Clock.schedule_once(lambda x: self._update())

    def _update(self, *args):
        self.width = Window.width
        buttons = self.ids._button_box.children
        button_sizes = (
            (len(buttons) - 1) * buttons[0].button_height
        ) + buttons[0].button_width
        space = self.width - button_sizes
        spacing = space / (len(buttons) + 1)
        self.ids._button_box.spacing = spacing
        self.ids._button_box.padding = [spacing, 0, spacing, 0]

    def set_current(self, index):
        if not index:
            index = -1
        button = self.ids._button_box.children[index]
        button.dispatch("on_release")

    def add_widget(self, widget, index=0, canvas=None):
        if issubclass(widget.__class__, Button_Item):
            return self.ids._button_box.add_widget(widget)
        else:
            return super().add_widget(widget, index=index, canvas=canvas)
