"""
Components/BadgeLayout
=======================

.. rubric:: This layout can be used to add a badge to the top of KivyMD components.

Example
---------------
.. code-block:: python

    from kivy.lang.builder import Builder
    from kivymd.app import MDApp

    kv_string = '''
    AKBadgeLayout:
        pos_hint: {"center_x": .5, "center_y": .5}
        badgeitem_padding: dp(5)
        bold: True
        text: "233+"
        offset: .5

        MDRaisedButton:
            text: "Press"
    '''
    class AKBadgeLayout(MDApp):
        def build(self):
            return Builder.load_string(kv_string)

    AKBadgeLayout().run()

"""


from kivy.lang.builder import Builder
from kivy.metrics import dp
from kivy.properties import (
    BooleanProperty,
    ColorProperty,
    ListProperty,
    NumericProperty,
    OptionProperty,
    StringProperty,
)
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivymd.theming import ThemableBehavior

Builder.load_string(
    """
<BadgeItem>
    size_hint: None, None
    padding: dp(5)
    size: self.size if root._text else [dp(20), dp(20)]
    opacity: 1 if self._badge_disabled == False else 0

    pos:
        (self.parent.x - self.width * (root._offset), self.parent.y + self.parent.height - self.height * (1 - root._offset)) if root._position == 'left' \
        else (self.parent.x + self.parent.width - self.width * (1 - root._offset), self.parent.y + self.parent.height - self.height * (1 - root._offset))

    canvas.before:
        Color:
            rgba: root._bg_color if root._bg_color else root.theme_cls.bg_normal
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [root.height / 2, ]

        Color:
            rgba: root._badgeitem_color if root._badgeitem_color else root.theme_cls.accent_color
        RoundedRectangle:
            pos:
                [self.pos[0] + root._badgeitem_padding / 2, self.pos[1] + root._badgeitem_padding/2]
            size: [self.size[0] - root._badgeitem_padding, self.size[1] - root._badgeitem_padding]
            radius: [root.height / 2, ]
    Label:
        size_hint: None, None
        size: self.texture_size[0] + dp(10), self.texture_size[1]
        halign: 'center'
        valign: 'center'
        font_size: dp(13)
        bold: root._bold
        pos_hint: {'center_x': .5, 'center_y': .5}
        text: root._text
        color: 1, 1, 1, 1

<AKBadgeLayout>:
    size_hint: None, None
    size: box.size
    BadgeContent:
        id: box
        pos: root.pos
        size_hint: None, None
        size: self.minimum_size

    BadgeItem:
        id: badge
        size_hint: None, None
        size: self.minimum_size
        _bg_color: root.bg_color
        _badgeitem_padding: root.badgeitem_padding
        _badgeitem_color: root.badgeitem_color
        _position: root.position
        _text: root.text
        _bold: root.bold
        _offset: root.offset
        _badge_disabled: root.badge_disabled
    """
)


class BadgeContent(BoxLayout):
    pass


class BadgeItem(ThemableBehavior, BoxLayout):
    _bg_color = ColorProperty()
    _badgeitem_padding = NumericProperty()
    _badgeitem_color = ListProperty()
    _position = OptionProperty("right", options=["right", "left"])
    _text = StringProperty("")
    _bold = BooleanProperty()
    _offset = NumericProperty()
    _badge_disabled = BooleanProperty(False)


class AKBadgeLayout(FloatLayout):
    bg_color = ColorProperty()
    """
    Color of the bakground around a badge.

    :attr:`bg_color` is an :class:`~kivy.properties.ColorProperty`
    and defaults to `'app.theme_cls.bg_normal'`.

    """

    badgeitem_padding = NumericProperty(dp(3))
    """
    Padding for the badge.

    :attr:`badgeitem_padding` is an :class:`~kivy.properties.NumericProperty`
    and defaults to `'3dp'`.

    """

    badgeitem_color = ListProperty()
    """
    Color of the badge.

    :attr:`badgeitem_color` is an :class:`~kivy.properties.ListProperty`
    and defaults to `'app.theme_cls.accent_color'`.

    """

    position = OptionProperty("right", options=["right", "left"])
    """
    Position of the badge relative to the widget it is on.
    Can be set to `right` or `left`.

    :attr:`position` is an :class:`~kivy.properties.OptionProperty`
    and defaults to `'right'`.

    """

    text = StringProperty("")
    """
    Text to be placed inside the badge.

    :attr:`text` is an :class:`~kivy.properties.StringProperty`
    and defaults to `''`.

    """

    bold = BooleanProperty(False)
    """
    Should the text inside the badge be bold

    :attr:`bold` is an :class:`~kivy.properties.BooleanProperty`
    and defaults to `False`.

    """

    offset = NumericProperty(0.25)
    """
    Offset of the badge's center point from the corner of the widget it is applied to

    :attr:`offset` is an :class:`~kivy.properties.NumericProperty`
    and defaults to `'0.25'`.

    """

    badge_disabled = BooleanProperty(False)
    """
    Show the badge or not. If set to `False` the badge opacity will be set to 0.

    :attr:`badge_disabled` is an :class:`~kivy.properties.BooleanProperty`
    and defaults to `False`.

    """

    def add_widget(self, widget, index=0, canvas=None):
        if issubclass(widget.__class__, BadgeItem) or issubclass(
            widget.__class__, BadgeContent
        ):
            return super().add_widget(widget, index=index, canvas=canvas)
        else:
            return self.ids.box.add_widget(widget)
