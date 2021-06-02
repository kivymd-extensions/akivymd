"""
Components/ButtonPanel
======================

.. rubric:: A collapsable panel of buttons

Example
----------

.. code-block:: python

    from kivy.lang import Builder
    from kivymd.uix.app import MDApp

    kv_string = '''
    AKButtonPanel:
        pos: root.width / 2 - self.width/2, root.height / 2 + dp(50)
        icon:"plus"
        selectable: True

        MDIconButton:
            icon: "minus"
            theme_text_color: "Custom"
            text_color: 1, 1, 0, 1

        MDIconButton:
            icon: "calendar"
            theme_text_color: "Custom"
            text_color: 1, 0, 0, 1
    '''

    class ButtonPanel(MDApp):

        def build(self):
            return Builder.load_string(kv_string)

"""


from kivy.animation import Animation
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import (
    BooleanProperty,
    ColorProperty,
    ListProperty,
    NumericProperty,
    StringProperty,
)
from kivy.uix.relativelayout import RelativeLayout
from kivymd.theming import ThemableBehavior
from kivymd.uix.button import MDFloatingActionButton, MDIconButton

Builder.load_string(
    """
<AKButtonPanel>:
    size_hint: None, None
    size: dp(56), dp(56)

    canvas:
        Color:
            rgba: self.theme_cls.primary_color if not self.rectangle_color else self.rectangle_color
        RoundedRectangle:
            pos: 0, -self.height + dp(56)
            size: dp(56), self.height
            radius: self.radius

    MDFloatingActionButton:
        id: main_button
        icon: root.icon
        on_release: root._toggle()
        md_bg_color: root.theme_cls.primary_dark if not root.main_button_color else root.main_button_color
        text_color: root.theme_cls.text_color if not root.icon_color else root.icon_color

    RelativeLayout:
        id: icon_holder
        width: dp(56)
        size_hint: None, None

"""
)

class AKButtonPanel(ThemableBehavior, RelativeLayout):

    icon = StringProperty("plus")
    """Defines the icon for the main button

    :attr:`icon` is an :class:`~kivy.properties.StringProperty`
    and defaults to `'plus'`.
    """

    radius = ListProperty([dp(30), dp(30), dp(30), dp(30)])
    """Used to define the radius of the drop down rectangle

    :attr:`radius` is an :class:`~kivy.properties.ListProperty`
    and defaults to `30dp`.
    """

    icon_color = ColorProperty(None)
    """Color of the icon for the main button

    :attr:`icon_color` is an :class:`~kivy.properties.ColorProperty`
    and defaults to `'app.theme_cls.text_color'`.
    """

    selectable = BooleanProperty(False)
    """Allows you to change between selectable and normal mode
    in selectable mode the widget will not move the main button to depict the current button
    pressed.

    :attr:`selectable` is an :class:`~kivy.properties.BooleanProperty`
    and defaults to `False`.
    """

    rectangle_color = ColorProperty(None)
    """Color of the dropdown rectangle. Defaults to the primary color of the app

    :attr:`rectangle_color` is an :class:`~kivy.properties.ColorProperty`
    and defaults to `'app.theme_cls.primary_color'`.
    """

    main_button_color = ColorProperty(None)
    """Color of the main button.It defaults to Primary Dark Color of the app

    :attr:`main_button_color` is an :class:`~kivy.properties.ColorProperty`
    and defaults to `'app.theme_cls.primary_color'`.
    """

    is_open = BooleanProperty(False)
    """A read only property that depicts if the widget is open or not

    :attr:`is_open` is an :class:`~kivy.properties.BooleanProperty`
    and defaults to `False`.
    """

    animation = StringProperty("in_out_circ")
    """The animation interpolation to be used for the rectangle drop down

    :attr:`animation` is an :class:`~kivy.properties.StringProperty`
    and defaults to `'in_out_circ'`.
    """

    anim_duration = NumericProperty(0.3)
    """The duration of the animation for the drop down rectangle in seconds.

    :attr:`anim_duration` is an :class:`~kivy.properties.NumericProperty`
    and defaults to `0.3`.
    """

    # auto_dismiss = BooleanProperty(True)
    # """ Hides the pannel when clicking outside of the pannel"""

    _z = -dp(56)
    # Internal variable used for positioning icons. Do not change this value, can cause weird behaviour

    _added = BooleanProperty(False)
    # Internal variable. Do not change this value, can cause weird behaviour

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def add_widget(self, widget, index=0, canvas=None):
        if isinstance(widget, RelativeLayout) or isinstance(
            widget, MDFloatingActionButton
        ):
            return super().add_widget(widget, 2)
        else:
            if isinstance(widget, MDIconButton):
                widget.bind(on_press=self._button_mover)
                widget.pos_hint = {"center_x": 0.5}
                self.ids.icon_holder.add_widget(widget)

    def _toggle(self, *args):
        if self.is_open:
            self.hide()
        else:
            self.show()

    def hide(self, *args):
        """
        Call this function to hide the panel.
        """
        if not self.is_open:
            return False
        if not self._added:
            for icon in self.ids.icon_holder.children:
                Animation(
                    pos=(0, 0), d=self.anim_duration, t=self.animation
                ).start(icon)
            else:
                Animation(
                    height=dp(56), d=self.anim_duration, t=self.animation
                ).start(self)
                self._z = -dp(56)
                self.is_open = False
        return True

    def show(self):
        """
        Call this function to show the panel.
        """
        if self.is_open:
            return False
        for icon in self.ids.icon_holder.children:
            Animation(
                pos=(0, self._z), d=self.anim_duration, t=self.animation
            ).start(icon)
            self._z -= dp(56)
        else:
            Animation(
                height=-self._z, d=self.anim_duration, t=self.animation
            ).start(self)
            self.is_open = True
        return True

    def _button_mover(self, widget, *args):
        if self.selectable:
            if not self._added:
                self.top_icon = MDIconButton(
                    icon=self.icon,
                    theme_text_color="Custom",
                    pos_hint={"center_x": 0.5},
                )
                self.top_icon.text_color = (
                    self.theme_cls.text_color
                    if not self.icon_color
                    else self.icon_color
                )
                self.top_icon.bind(on_press=self._top_icon_remover)
                self.ids.icon_holder.add_widget(self.top_icon)
                self._added = True
            Animation(
                pos=widget.parent.to_parent(0, widget.pos[1]),
                duration=0.3,
                t="in_out_circ",
            ).start(self.ids.main_button)
            self.ids.main_button.icon = widget.icon
            self.ids.main_button.text_color = widget.text_color

    def _top_icon_remover(self, widget, *args):
        self.ids.main_button.icon = self.top_icon.icon
        self.ids.main_button.text_color = self.top_icon.text_color
        anim1 = Animation(pos=(0, 0), duration=0.3, t="in_out_circ")
        anim1.bind(on_complete=self._icon_remove)
        anim1.start(self.ids.main_button)
        self._added = False

    def _icon_remove(self, widget, *args):
        self.ids.icon_holder.remove_widget(self.top_icon)

    # def on_touch_down(self, touch):
    #     print(self.ids.icon_holder.collide_point(*touch.pos))
    #     if not self.collide_point(*touch.pos):
    #         if self.is_open and self.auto_dismiss:
    #             self.hide()
    #             return True
    #     super().on_touch_down(touch)
