"""
Components/FloatingRoundedAppbar
================================

.. rubric:: A floating pill shaped dock/bar to which special icon buttons can be added

Example
-------

.. code-block:: python

    from kivy.lang.builder import Builder
    from kivymd.app import MDApp
    from kivymd.toast import toast
    import kivymd_extensions.akivymd  # NOQA

    kv_string = '''

    MDScreen:

        AKFloatingRoundedAppbar:

            AKFloatingRoundedAppbarButtonItem:
                icon: "magnify"
                text: "Search"
                on_release: app.toast(self.text)

            AKFloatingRoundedAppbarAvatarItem:
                source: "assets/google.jpg"
    '''


    class BottomAppbar(MDApp):
        def build(self):
            return Builder.load_string(kv_string)

        def toast(self, x):
            return toast(x)


    BottomAppbar().run()

"""
from kivy.lang.builder import Builder
from kivy.properties import BooleanProperty, ListProperty, StringProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivymd.theming import ThemableBehavior
from kivymd.uix.behaviors import MagicBehavior

Builder.load_string(
    """
<AKFloatingRoundedAppbarItemBase>:
    orientation: "vertical"
    size_hint: None, None
    height: self.parent.height - dp(5)
    width: self.minimum_width
    pos_hint: {"center_x": .5, "center_y": .5}


<AKFloatingRoundedAppbarButtonItem>:
    MDIcon:
        icon: root.icon
        halign: "center"
        valign: "center"
        theme_text_color: "Custom"
        text_color: root.icon_color if root.icon_color else root.theme_cls.text_color
        font_size: dp(20)
        pos_hint: {"center_x": .5, "center_y": .5}
        size_hint: None, None
        size: self.font_size, self.font_size

    Label:
        text: root.text
        halign: "center"
        valign: "center"
        font_size: dp(10)
        color: root.text_color if root.text_color else root.theme_cls.text_color
        size_hint: None, None
        size: self.texture_size


<AKFloatingRoundedAppbarAvatarItem>:
    spacing: dp(1)

    BoxLayout:
        size_hint: None, None
        size : [self.parent.height - dp(2), self.parent.height - dp(2)] if not root.text else [dp(20), dp(20)]
        pos_hint: {"center_x": .5, "center_y": .5}
        canvas.after:
            Color:
                rgba: 1, 1, 1, 1
            Ellipse:
                pos: self.pos
                size: self.size
                source: root.source

    Label:
        text: root.text
        halign: "center"
        valign: "center"
        font_size: dp(10)
        color: root.text_color if root.text_color else root.theme_cls.text_color
        size_hint: None, None
        size: self.texture_size

<AKFloatingRoundedAppbar>:
    size_hint: None, None
    size: self.minimum_width, dp(40)
    pos_hint: {"center_x": .5}
    y: dp(10)
    spacing: dp(40)
    padding: dp(40)
    canvas.before:
        Color:
            rgba: root.bg_color if root.bg_color else root.theme_cls.primary_color
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [root.height/2, ]
    """
)

__all__ = (
    "AKFloatingRoundedAppbar",
    "AKFloatingRoundedAppbarAvatarItem",
    "AKFloatingRoundedAppbarButtonItem",
)


class AKFloatingRoundedAppbarItemBase(
    ThemableBehavior, ButtonBehavior, MagicBehavior, BoxLayout
):
    def on_release(self):
        if self.parent.press_effect:
            self.grow()


class AKFloatingRoundedAppbarButtonItem(AKFloatingRoundedAppbarItemBase):
    """
    This class is used to create an icon button to be placed inside the app bar
    """

    icon = StringProperty()
    """
    Icon to be displayed on the button

    :attr:`icon` is an :class:`~kivy.properties.StringProperty`
    and defaults to `None`.
    """

    text = StringProperty()
    """
    Text to be displayed below the icon

    :attr:`text` is an :class:`~kivy.properties.StringProperty`
    and defaults to `None`.
    """

    text_color = ListProperty()
    """
    Color of the text displayed below the icon

    :attr:`text_color` is an :class:`~kivy.properties.ListProperty`
    and defaults to `'app.theme_cls.text_color'`.
    """

    icon_color = ListProperty()
    """
    Color of the icon

    :attr:`icon_color` is an :class:`~kivy.properties.ListProperty`
    and defaults to `'app.theme_cls.text_color'`.
    """


class AKFloatingRoundedAppbarAvatarItem(AKFloatingRoundedAppbarItemBase):
    """
    This class is used to create a button with an image to be placed inside the app bar
    """

    source = StringProperty()
    """
    Filepath for the image to be displayed on the button

    :attr:`source` is an :class:`~kivy.properties.StringProperty`
    and defaults to `None`.
    """

    text = StringProperty()
    """
    Text to be displayed below the image

    :attr:`text` is an :class:`~kivy.properties.StringProperty`
    and defaults to `None`.
    """

    text_color = ListProperty()
    """
    Color of the text below the image

    :attr:`text_color` is an :class:`~kivy.properties.ListProperty`
    and defaults to `'app.theme_cls.text_color'`.
    """


class AKFloatingRoundedAppbar(ThemableBehavior, BoxLayout):
    """
    This is the base class for `AKFloatingRoundedAppbar`. Instances of `AKFloatingRoundedAppbarButtonItem`
    and `AKFloatingRoundedAppbarAvatarItem` can be added inside this class.
    """

    bg_color = ListProperty()
    """
    Color of the appbar

    :attr:`bg_color` is an :class:`~kivy.properties.ListProperty`
    and defaults to `'app.theme_cls.primary_color'`.
    """

    press_effect = BooleanProperty(True)
    """
    If this property is set to `True`. Pressing on a button/Avatar icon of the bar will display a grow
    and shrink effect for the pressed icon. See
    `Kivymd Magic behaviour <https://kivymd.readthedocs.io/en/latest/behaviors/magic/#kivymd.uix.behaviors.magic_behavior.MagicBehavior.grow>`_
    for more info.

    :attr:`press_effect` is an :class:`~kivy.properties.BooleanProperty`
    and defaults to `True`.
    """
