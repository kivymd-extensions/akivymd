from kivy.lang import Builder
from kivy.uix.relativelayout import RelativeLayout
from kivymd.uix.button import MDIconButton
from kivymd.uix.button import MDFloatingActionButton
from kivymd.theming import ThemableBehavior
from kivy.animation import Animation
from kivy.metrics import dp
from kivy.properties import (
    ColorProperty,
    ListProperty,
    NumericProperty,
    StringProperty,
    BooleanProperty,
)

Builder.load_string(
    """
<AKButtonPanel>:
    pos:self.pos
    size_hint:None,None
    height:dp(56)
    canvas:
        Color:
            rgba:self.theme_cls.primary_color if not self.rectangle_color else self.rectangle_color
        RoundedRectangle:
            pos:self.pos[0],self.pos[1]-self.height + dp(56)
            size:dp(56),self.height
            radius:self.radius

    MDFloatingActionButton:
        id:main_button
        icon:root.icon
        pos:root.pos
        on_release:root._show()
        md_bg_color:root.theme_cls.primary_dark if not root.main_button_color else root.main_button_color
        text_color:root.theme_cls.text_color if not root.icon_color else root.icon_color


    RelativeLayout:
        id:icon_holder
        pos:root.pos[0], root.pos[1]
        width:dp(56)
        size_hint:None,None

"""
)


class AKButtonPanel(ThemableBehavior, RelativeLayout):

    radius = ListProperty([dp(30), dp(30), dp(30), dp(30)])
    """Used to define the radius of the drop down rectangle"""

    icon = StringProperty("plus")
    """Defines the icon for the main button"""

    icon_color = ColorProperty(None)
    """Color of the icon for the main button"""

    selectable = BooleanProperty(False)
    """Allows you to change between selectable and normal mode
    in selectable mode the widget will not move the main button to depict the current button
    pressed"""

    rectangle_color = ColorProperty(None)
    """Color of the dropdown rectangle. Defaults to the primary color of the app"""

    main_button_color = ColorProperty(None)
    """Color of the main button.It defaults to Primary Dark Color of the app"""

    open = BooleanProperty(False)
    """A read only property that depicts if the widget is open or not"""

    animation = StringProperty("in_out_circ")
    """The animation interpolation to be used for the rectangle drop down"""

    anim_duration = NumericProperty(0.3)
    """The duration of the animation for the drop down rectangle"""

    z = NumericProperty(-dp(56))
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
                widget.pos_hint = {'center_x':.5}
                self.ids.icon_holder.add_widget(widget)

    def _show(self, *args):
        if self.open:
            if not self._added:
                for icon in self.ids.icon_holder.children:
                    Animation(pos=(0, 0), d=self.anim_duration, t=self.animation).start(
                        icon
                    )
                else:
                    Animation(
                        height=dp(56), d=self.anim_duration, t=self.animation
                    ).start(self)
                    self.z = -dp(56)
                    self.open = False

        else:
            for icon in self.ids.icon_holder.children:
                Animation(
                    pos=(0, self.z), d=self.anim_duration, t=self.animation
                ).start(icon)
                self.z -= dp(56)
            else:
                Animation(height=-self.z, d=self.anim_duration, t=self.animation).start(
                    self
                )
                self.open = True

    def _button_mover(self, widget, *args):
        if self.selectable:
            if not self._added:
                self.top_icon = MDIconButton(
                    icon=self.icon, theme_text_color="Custom", pos_hint={'center_x':.5}
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
        anim1 = Animation(pos=self.pos, duration=0.3, t="in_out_circ")
        anim1.bind(on_complete=self._icon_remove)
        anim1.start(self.ids.main_button)
        self._added = False

    def _icon_remove(self, widget, *args):
        self.ids.icon_holder.remove_widget(self.top_icon)
