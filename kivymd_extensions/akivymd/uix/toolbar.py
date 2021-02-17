"""
Components/Toolbar
=================


Example
-------

.. code-block:: python

    from kivy.uix.behaviors import ButtonBehavior
    from kivy.lang.builder import Builder

    import kivymd_extensions.akivymd
    from kivymd.app import MDApp
    from kivymd.uix.list import OneLineListItem

    kv = '''

    Screen:

        AKToolbarLayout:
            id: toolbar

            AKToolbarClass:
                MDToolbar:
                    title: 'Hide On Scroll'
                    left_action_items: [('menu', lambda x: None)]

            AKToolbarPinClass:
                id: pin
                height: dp(40)
                canvas.before:
                    Color:
                        rgba: app.theme_cls.accent_color
                    Rectangle:
                        pos: self.pos
                        size: self.size

                MDLabel:
                    text: 'Pinned to top'
                    halign: 'center'
                    valign: 'center'

            AKToolbarContent:
                id: box

            AKToolbarFloatingButton:
                MDFloatingActionButton:
                    icon: 'arrow-up'
                    on_release: toolbar.scroll_to(1)

    '''


    class Main(MDApp):

        def build(self):
            return Builder.load_string(kv)

        def on_start(self):
            for x in range(30):
                self.root.ids.box.add_widget(OneLineListItem(
                    text= f'List {x}'
                ))
            return super().on_start()


    Main().run()

"""

__all__ = (
    "AKToolbarClass",
    "AKToolbarPinClass",
    "AKToolbarFloatingButton",
    "AKToolbarContent",
    "AKToolbarLayout",
)

from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.effects.dampedscroll import DampedScrollEffect
from kivy.lang.builder import Builder
from kivy.properties import (
    BooleanProperty,
    NumericProperty,
    ObjectProperty,
    OptionProperty,
    ReferenceListProperty,
    StringProperty,
)
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.stencilview import StencilView
from kivymd.theming import ThemableBehavior

Builder.load_string(
    """
<AKToolbarClass>
    size_hint_y: None
    height: self.minimum_height


<AKToolbarPinClass>
    size_hint_y: None
    height: self.minimum_height


<AKToolbarFloatingButton>
    size_hint: None, None
    size: self.minimum_size


<AKToolbarContent>
    size_hint_y: None
    height: self.minimum_height
    orientation: "vertical"


<AKToolbarLayout>
    _toolbar: _toolbar
    _floating_button: _floating_button

    ScrollView:
        id: scroll

        MDBoxLayout:
            id: scrollbox
            adaptive_height: True
            orientation: "vertical"

            BoxLayout:
                size_hint_y: None
                height: _toolbar.height + _pin_widget.height

    MDBoxLayout:
        id: _toolbar
        adaptive_height: True

    MDBoxLayout:
        id: _pin_widget
        top: _toolbar.y
        adaptive_height: True

    BoxLayout:
        id: _floating_button
        size_hint: None, None
        size: self.minimum_size

    """
)


class AKToolbarClass(BoxLayout):
    pass


class AKToolbarFloatingButton(BoxLayout):
    pass


class CustomScrollViewEffect(DampedScrollEffect):
    friction = 0.1


class AKToolbarContent(BoxLayout):
    _root = ObjectProperty()

    def add_widget(self, widget, index=0, canvas=None):
        Clock.schedule_once(self._root._update_toolbar_pos)
        return super().add_widget(widget, index=index, canvas=canvas)


class AKToolbarPinClass(BoxLayout):
    def on_touch_down(self, touch):
        pos = touch.pos

        if not self.collide_point(*pos):
            return False

        for child in self.children:
            child.on_touch_down(touch)

        return True


class AKToolbarLayout(ThemableBehavior, StencilView, RelativeLayout):
    duration = NumericProperty(0.3)
    """Animations duration.

    :attr:`duration` is an :class:`~kivy.properties.NumericProperty`
    and defaults to `0.3`.
    """

    transition = StringProperty("out_quad")
    """Animations transition.

    :attr:`duration` is an :class:`~kivy.properties.StringProperty`
    and defaults to `'out_quad'`.
    """

    show_on_stop = BooleanProperty(False)
    """Always shows toolbar after scroll stop.

    :attr:`show_on_stop` is an :class:`~kivy.properties.BooleanProperty`
    and defaults to `False`.
    """

    auto_adjust = BooleanProperty(True)
    """Automatically adjusts the toolbar's height after scrolling stop.

    :attr:`auto_adjust` is an :class:`~kivy.properties.BooleanProperty`
    and defaults to `True`.
    """

    float_button_pos = OptionProperty("br", options=["br", "bl", "tl", "tr"])
    """Floating button position.

    :attr:`float_button_pos` is an :class:`~kivy.properties.OptionProperty`
    and defaults to `br`.
    """

    float_button_padding_x = NumericProperty("30dp")
    """Floating button's horizontal padding.

    :attr:`float_button_padding_x` is an :class:`~kivy.properties.NumericProperty`
    and defaults to `'30dp`.
    """

    float_button_padding_y = NumericProperty("30dp")
    """Floating button's vertical padding.

    :attr:`float_button_padding_y` is an :class:`~kivy.properties.NumericProperty`
    and defaults to `'30dp`.
    """

    float_button_padding = ReferenceListProperty(
        float_button_padding_x, float_button_padding_y
    )
    float_button_show_distance = NumericProperty("150dp")

    _toolbar = ObjectProperty()
    _floating_button = ObjectProperty()
    _last_y = False
    _anim_playing = False
    _float_anim_playing = False
    _float_button_status = "close"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self._update)

    def _update(self, *args):
        self.ids.scroll.bind(vbar=self._set_toolbar_pos)
        self.ids.scroll.bind(on_scroll_stop=self.on_scroll_stop)
        self.ids.scroll.effect_cls = CustomScrollViewEffect

        Window.bind(on_resize=self._update_toolbar_pos)
        Window.bind(on_resize=self._update_floating_button_pos)
        self._last_height = self.height

    def _set_toolbar_pos(self, instance, vbar):
        y = vbar[0] * self.height

        if not self._last_y:
            self._last_y = y
            return
        else:
            diff = self._last_y - y
            self._last_y = y

        # Sometimes scrollview jumps suddenly
        if diff > 50:
            return

        # handle floating button
        scrolled_y = (1 - vbar[1] - vbar[0]) * self.height
        if (
            scrolled_y > self.float_button_show_distance
            and self._float_button_status == "close"
        ):
            self.show_float_button()
        elif (
            scrolled_y < self.float_button_show_distance
            and self._float_button_status == "open"
        ):
            self.hide_float_button()

        if self._anim_playing:
            Animation.stop_all(self._toolbar)
            self._anim_playing = False

        self._toolbar.y += diff
        # hide
        if self._toolbar.y > self.height:
            self.hide_toolbar()
        # full size
        elif (
            self._toolbar.top < self.height or round(vbar[0] + vbar[1], 2) == 1
        ):
            self.show_toolbar()

    def hide_toolbar(self, animate=False, *args):
        if animate and not self._anim_playing:
            self._anim_playing = True
            anim = Animation(y=self.height, d=self.duration, t=self.transition)
            anim.bind(on_complete=self._allow_anim)
            anim.start(self._toolbar)
        else:
            self._toolbar.y = self.height

    def show_toolbar(self, animate=False, *args):
        if animate and not self._anim_playing:
            self._anim_playing = True
            anim = Animation(
                top=self.height, d=self.duration, t=self.transition
            )
            anim.bind(on_complete=self._allow_anim)
            anim.start(self._toolbar)
        else:
            self._toolbar.top = self.height

    def _allow_anim(self, *args):
        self._anim_playing = False
        return

    def _update_toolbar_pos(self, *args):
        def update_pos(*args):
            self._toolbar.top = self.height

        Clock.schedule_once(update_pos)

    def add_widget(self, widget, index=0, canvas=None):
        if issubclass(widget.__class__, AKToolbarContent):
            widget._root = self
            return self.ids.scrollbox.add_widget(widget)

        elif issubclass(widget.__class__, AKToolbarClass):
            return self.ids._toolbar.add_widget(widget)

        elif issubclass(widget.__class__, AKToolbarPinClass):
            return self.ids._pin_widget.add_widget(widget)

        elif issubclass(widget.__class__, AKToolbarFloatingButton):
            self.ids._floating_button.add_widget(widget)
            Clock.schedule_once(self._update_floating_button_pos)

        else:
            return super().add_widget(widget, index=index, canvas=canvas)

    def on_scroll_stop(self, instance, touch):
        if self.show_on_stop:
            Clock.schedule_once(self.show_toolbar, 1)
        elif self.auto_adjust:
            Clock.schedule_once(self._auto_adjust, 1)

    def _auto_adjust(self, *args):
        middle_pos = self.height - self._toolbar.height / 2
        if self._toolbar.y < middle_pos:
            self.show_toolbar(animate=True)
        else:
            self.hide_toolbar(animate=True)

    def _update_floating_button_pos(self, *args):
        width = Window.width

        padding_y = self.float_button_padding_y

        if self.float_button_pos == "br":
            self._floating_button.x = width + 20
            self._floating_button.y = padding_y

        elif self.float_button_pos == "bl":
            raise NotImplementedError

        elif self.float_button_pos == "tr":
            raise NotImplementedError

        elif self.float_button_pos == "tl":
            raise NotImplementedError

    def _allow_float_anim(self, *args):
        self._float_anim_playing = False

    def show_float_button(self):
        if self._float_anim_playing:
            self._float_anim_playing = True
            return

        self._float_button_status = "open"
        Animation.stop_all(self._floating_button)
        width = Window.width
        anim = Animation(
            right=width - self.float_button_padding_x,
            d=self.duration,
            t=self.transition,
        )
        anim.bind(on_complete=self._allow_float_anim)
        anim.start(self._floating_button)

    def hide_float_button(self):
        if self._float_anim_playing:
            self._float_anim_playing = True
            return

        self._float_button_status = "close"
        Animation.stop_all(self._floating_button)
        width = Window.width
        width = Window.width
        anim = Animation(x=width + 20, d=self.duration, t=self.transition)
        anim.bind(on_complete=self._allow_float_anim)
        anim.start(self._floating_button)

    def get_float_button_status(self):
        return self._float_button_status

    def scroll_to(self, value):
        Animation(scroll_y=value, d=self.duration, t=self.transition).start(
            self.ids.scroll
        )
