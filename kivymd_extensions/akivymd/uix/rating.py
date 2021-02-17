"""
Components/Rating
=================


Example
-------

.. code-block:: python

    from kivy.lang.builder import Builder

    from kivymd.app import MDApp

    KV = '''
    Screen:
        AKRating:
            direction : 'lr'
            pos_hint: {'center_x': .5, 'center_y': .5}
            on_rate: print(self.get_rate())
    '''

    class Main(MDApp):

        def build(self):
            return Builder.load_string(KV)


    Main().run()
"""

from kivy.clock import Clock
from kivy.lang.builder import Builder
from kivy.metrics import dp
from kivy.properties import (
    ListProperty,
    NumericProperty,
    OptionProperty,
    StringProperty,
)
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivymd.theming import ThemableBehavior
from kivymd.uix.behaviors import MagicBehavior

Builder.load_string(
    """
<_RaitingItem>
    size_hint: None, None
    size: root.font_size + root.item_spacing, root.font_size
    magic_speed: 0.6

    MDIcon:
        icon: root.icon
        theme_text_color: "Custom" if root.text_color else "Primary"
        text_color: root.text_color if root.text_color else root.theme_cls.primary_color
        font_size: root.font_size
        halign: "center"
        valign: "center"


<AKRating>
    size_hint: None, None
    size: self.minimum_size
    """
)


class _RaitingItem(ThemableBehavior, ButtonBehavior, BoxLayout, MagicBehavior):
    icon = StringProperty()
    text_color = ListProperty()
    font_size = NumericProperty()
    item_spacing = NumericProperty()


class AKRating(ThemableBehavior, BoxLayout):
    """
    :Events:
        :attr:`on_rate`
            Called when an icon is clicked.
    """

    count = NumericProperty(5)
    """Number of items.

    :attr:`count` is an :class:`~kivy.properties.NumericProperty`
    and defaults to `5`.
    """

    direction = OptionProperty("lr", options=["lr", "rl"])
    """Direction of item selection. Can be `lr` for left to right or `rl` for right to left.

    :attr:`direction` is an :class:`~kivy.properties.OptionProperty`
    and defaults to `lr`.
    """

    normal_icon = StringProperty("star-outline")
    """Normal icon.

    :attr:`normal_icon` is an :class:`~kivy.properties.StringProperty`
    and defaults to `star-outline`.
    """

    active_icon = StringProperty("star")
    """Active icon.

    :attr:`normal_icon` is an :class:`~kivy.properties.StringProperty`
    and defaults to `star`.
    """

    normal_color = ListProperty()
    """Normal icon color.

    :attr:`normal_color` is an :class:`~kivy.properties.ListProperty`
    and defaults to primary color.
    """

    active_color = ListProperty()
    """Active icon color.

    :attr:`active_color` is an :class:`~kivy.properties.ListProperty`
    and defaults to accent color.
    """

    icon_size = NumericProperty(dp(30))
    """The size of icons.

    :attr:`icon_size` is an :class:`~kivy.properties.NumericProperty`
    and defaults to `dp(30)`.
    """

    item_spacing = NumericProperty(dp(7))
    """The space between icons.

    :attr:`item_spacing` is an :class:`~kivy.properties.NumericProperty`
    and defaults to `dp(7)`.
    """

    animation_type = OptionProperty(
        "twist", options=[False, "twist", "wobble", "shake", "grow"]
    )
    """The animation type when an icon is clicked. The animations will be applied on active icons only.
        Set to `False` for no animation.

    :attr:`animation_type` is an :class:`~kivy.properties.OptionProperty`
    and defaults to `twist`.
    """

    _selected = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self._update)
        self.register_event_type("on_rate")

    def _update(self, *args):
        self._generate_items()

    def _generate_items(self, *args):

        for _ in range(self.count):
            item = _RaitingItem(
                font_size=self.icon_size,
                on_release=lambda x: self.dispatch("on_rate"),
                item_spacing=self.item_spacing,
            )
            item.bind(on_release=self._select_callback)
            self.add_widget(item)

        self._update_items()

    def _select_callback(self, instance):
        self._selected = self._get_item_index(instance)
        self._update_items()

    def _update_items(self):
        if not self.active_color:
            active_color = self.theme_cls.accent_color
        else:
            active_color = self.active_color

        if not self.normal_color:
            normal_color = self.theme_cls.primary_color
        else:
            normal_color = self.normal_color

        items = self._get_children()
        for item in items[: self._selected + 1]:
            item.text_color = active_color
            item.icon = self.active_icon

            if self.animation_type:
                eval("item.%s()" % self.animation_type)

        for item in items[self._selected + 1 :]:
            item.text_color = normal_color
            item.icon = self.normal_icon

    def _get_children(self):
        if self.direction == "rl":
            children = self.children
        elif self.direction == "lr":
            children = list(reversed(self.children))
        return children

    def get_rate(self):
        return self._selected + 1

    def _get_item_index(self, item):
        return self._get_children().index(item)

    def on_rate(self, *args):
        pass

    def set_rate(self, rate):
        """Set current rate. """

        self._selected = rate - 1
        self._update_items()
