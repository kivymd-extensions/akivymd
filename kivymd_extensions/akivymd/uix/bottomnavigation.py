from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang.builder import Builder
from kivy.metrics import dp
from kivy.properties import ListProperty, NumericProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivymd.theming import ThemableBehavior
from kivymd.uix.button import MDIconButton
from kivymd.uix.label import MDLabel

__all__ = ("AKBottomNavigation",)

Builder.load_string(
    """
<_AKLabel>
    size_hint: None, None
    size: dp(48), dp(48)
    font_style: "Caption"
    halign: "center"
    valign: "center"
    theme_text_color: "Custom"
    text_color: root.text_color if root.text_color else root.theme_cls.primary_light


<_AKButton>
    theme_text_color: "Custom"
    text_color: root.icon_color if root.icon_color else root.theme_cls.primary_color


<AKBottomNavigation>:
    orientation: "vertical"
    size_hint_y: None
    height: self.minimum_height
    BoxLayout:
        size_hint_y: None
        height: dp(14)

        canvas.before:
            Color:
                rgba: root.bar_color if root.bar_color else root.theme_cls.primary_color
            Rectangle:
                pos: self.pos
                size: self.size

    BoxLayout:
        size_hint_y: None
        height: dp(56)

        canvas.before:
            Color:
                rgba: root.bg_color if root.bg_color else root.theme_cls.bg_dark
            Rectangle:
                pos: self.pos
                size: self.size

        Widget:
            id: _bubble
            bubble_x: 0
            size_hint: None, None
            size: root.width, dp(70)
            canvas.before:
                Color:
                    rgba: root.bar_color if root.bar_color else root.theme_cls.primary_color
                Rectangle:
                    pos: self.bubble_x, dp(28)
                    size: dp(112), dp(28)
                Ellipse:
                    pos: self.bubble_x + dp(28), 0
                    size: dp(56), dp(56)
                Color:
                    rgba: root.bg_color if root.bg_color else root.theme_cls.bg_dark
                Ellipse:
                    pos: self.bubble_x- dp(28), 0
                    size: dp(56), dp(56)
                Ellipse:
                    pos: self.bubble_x + dp(84), 0
                    size: dp(56), dp(56)

            FloatLayout:
                id: _text_bar
                size_hint: None, None
                size: root.width, dp(56)

            FloatLayout:
                id: _buttons_bar
                size_hint: None, None
                size: root.width, dp(70)
"""
)


class _AKLabel(MDLabel):
    text_color = ListProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class _AKButton(MDIconButton):
    icon_color = ListProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(lambda x: self._update())

    def on_release(self):
        self.root.set_current(self.parent.children.index(self))

    def _update(self):
        self.root = self.parent.parent.parent.parent


class AKBottomNavigation(ThemableBehavior, BoxLayout):
    items = ListProperty()
    bar_color = ListProperty()
    icon_color = ListProperty()
    text_color = ListProperty()
    bg_color = ListProperty()
    transition = StringProperty("out_sine")
    duration = NumericProperty(0.2)

    _selected = -1

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_resize=self._on_resize)

    def _clear_bar(self):
        self.ids._buttons_bar.clear_widgets()
        self.ids._text_bar.clear_widgets()

    def _update_items(self, items):
        count = len(self.items)
        section_x = 1 / (count + 1)
        but_pos = section_x
        for x in range(0, count):
            button = _AKButton(
                icon=self.items[x]["icon"],
                pos_hint={"center_x": but_pos},
                icon_color=self.icon_color,
            )
            button.bind(on_release=self.items[x]["on_release"])

            label = _AKLabel(
                text=self.items[x]["text"],
                pos_hint={"center_x": but_pos},
                opacity=0,
                text_color=self.text_color,
            )

            self.ids._text_bar.add_widget(label)
            self.ids._buttons_bar.add_widget(button)
            but_pos += section_x
        self.ids._bubble.bubble_x = Window.size[
            0
        ] * self.ids._buttons_bar.children[self._selected].pos_hint[
            "center_x"
        ] - dp(
            56
        )
        self.ids._buttons_bar.children[self._selected].opacity = 0
        self.ids._text_bar.children[self._selected].opacity = 1

    def _on_resize(self, instance, width, height):
        self.ids._bubble.bubble_x = width * self.ids._buttons_bar.children[
            self._selected
        ].pos_hint["center_x"] - dp(56)

    def on_items(self, *args):
        self._clear_bar()
        return self._update_items(self.items)

    def set_current(self, index):
        current_item_button = self.ids._buttons_bar.children[index]
        current_item_text = self.ids._text_bar.children[index]
        AKBottomNavigation._selected = index

        for x in self.ids._buttons_bar.children:  # button
            x.opacity = 1

        for x in self.ids._text_bar.children:  # text
            x.opacity = 0

        bubble_pos = current_item_button.x - dp(31)
        anim_bubble = Animation(
            bubble_x=bubble_pos, t=self.transition, duration=self.duration
        )
        anim_text_opacity = Animation(
            opacity=1, t=self.transition, duration=self.duration
        )
        anim_icon_opacity = Animation(
            opacity=0, t=self.transition, duration=self.duration
        )

        anim_icon_opacity.start(current_item_button)
        anim_text_opacity.start(current_item_text)
        anim_bubble.start(self.ids._bubble)
