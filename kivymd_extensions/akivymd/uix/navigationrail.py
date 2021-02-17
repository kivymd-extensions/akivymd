from kivy.animation import Animation
from kivy.clock import Clock
from kivy.lang.builder import Builder
from kivy.properties import (
    BooleanProperty,
    ListProperty,
    NumericProperty,
    StringProperty,
)
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivymd.theming import ThemableBehavior

Builder.load_string(
    """
<AKNavigationrailItemBase>:


<AKNavigationrailCustomItem>:


<AKNavigationrailItem>:
    size_hint_y: None
    height: root.parent.parent.item_height
    MDIcon:
        icon: root.icon
        size_hint_x: None
        width: root.height
        theme_text_color: "Custom"
        text_color: root.active_icon_color if root.active else root.icon_color
        halign: "center"

    MDLabel:
        opacity: root.item_text_opacity
        text: root.text
        theme_text_color: "Custom"
        text_color: root.active_text_color if root.active else root.text_color
        halign: "left"
        valign: "center"


<AKNavigationrail>

    BoxLayout:
        orientation: "vertical"
        id: items_box
        size_hint_x: None
        width: root._opening_width
        canvas.before:

            #==========
            # bg
            #==========
            Color:
                rgba: root.navigation_bg_color
            Rectangle:
                pos: self.pos
                size: self.size

            #==========
            # Main rect
            #==========
            Color:
                rgba: root.active_color if root.active_color else root.theme_cls.bg_normal
            RoundedRectangle:
                pos: self.pos[0], self.pos[1] + root._ghost_pos_y
                size: self.width, root.item_height
                radius: [root.item_height / 2, 0, 0, root.item_height / 2]

            #=============
            # second rects
            #=============
            Color:
                rgba: root.active_color if root.active_color else root.theme_cls.bg_normal
            Rectangle:
                size: root._item_radius, root._item_radius
                pos: self.width - root._item_radius, root._ghost_pos_y - root._item_radius
            Rectangle:
                size: root._item_radius, root._item_radius
                pos:  self.width - root._item_radius, root._ghost_pos_y + root.item_height

            #===========
            # circles
            #===========
            Color:
                rgba: root.navigation_bg_color
            Ellipse:
                size: root._item_radius * 2, root._item_radius * 2
                pos: self.width - root._item_radius * 2,  root._ghost_pos_y - root._item_radius * 2
            Ellipse:
                size: root._item_radius * 2, root._item_radius * 2
                pos: self.width - root._item_radius * 2, root._ghost_pos_y + root.item_height

    BoxLayout:
        id: content
"""
)


class AKNavigationrailItemBase(BoxLayout):
    pass


class AKNavigationrailItem(
    ThemableBehavior, ButtonBehavior, AKNavigationrailItemBase
):
    icon = StringProperty()
    text = StringProperty()
    text_color = ListProperty([0, 0, 0, 0])
    icon_color = ListProperty([0, 0, 0, 0])
    active_text_color = ListProperty([0, 0, 0, 0])
    active_icon_color = ListProperty([0, 0, 0, 0])
    active = BooleanProperty(False)

    item_text_opacity = NumericProperty(1)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(lambda x: self._update())

    def _update(self):

        if self.active_text_color == [0, 0, 0, 0]:
            self.active_text_color = self.theme_cls.primary_color

        if self.text_color == [0, 0, 0, 0]:
            self.text_color = self.theme_cls.text_color

        if self.active_icon_color == [0, 0, 0, 0]:
            self.active_icon_color = self.theme_cls.primary_color

        if self.icon_color == [0, 0, 0, 0]:
            self.icon_color = self.theme_cls.text_color

    def on_release(self):
        self.root = self.parent.parent
        index = self.root.ids.items_box.children.index(self)
        self.root.set_current(index, item_index=False)
        return super().on_release()


class AKNavigationrailCustomItem(AKNavigationrailItemBase):
    pass


class AKNavigationrailContent(BoxLayout):
    pass


class AKNavigationrail(ThemableBehavior, BoxLayout):
    opening_width = NumericProperty("200dp")
    navigation_bg_color = ListProperty()
    item_height = NumericProperty("60dp")
    item_radius = NumericProperty("100dp")
    active_color = ListProperty()
    transition = StringProperty("out_quad")
    duration = NumericProperty(0.2)

    _ghost_pos_y = NumericProperty(0)
    _selected = None
    _opening_width = NumericProperty()
    _item_radius = NumericProperty()
    _state = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(lambda x: self._update())
        self.register_event_type("on_open")
        self.register_event_type("on_dismiss")

    def _update(self):
        if not self.navigation_bg_color:
            self.navigation_bg_color = self.theme_cls.primary_color
        self._opening_width = self.opening_width
        self._item_radius = self.item_radius
        self.open()

    def get_state(self):
        return self._state

    def on_dismiss(self, *args):
        pass

    def dismiss(self):
        width = self.item_height
        anim = Animation(
            _opening_width=width,
            _item_radius=width / 2,
            duration=self.duration,
            t=self.transition,
        )
        anim.start(self)
        self._hide_text()
        self.dispatch("on_dismiss")
        self._state = "dismiss"
        return

    def on_open(self, *args):
        pass

    def open(self):
        width = self.opening_width
        anim = Animation(
            _opening_width=width,
            _item_radius=self.item_radius,
            duration=self.duration,
            t=self.transition,
        )
        anim.start(self)
        self.dispatch("on_open")
        self._show_text()
        self._state = "open"
        return

    def _set_ghost_pos(self, y, anim):
        if anim:
            anim = Animation(
                _ghost_pos_y=y, t=self.transition, duration=self.duration
            )
            anim.start(self)
        else:
            self._ghost_pos_y = y
        return

    def refresh_items(self):
        if not self._selected:
            return
        Clock.schedule_once(
            lambda x: self.set_current(
                self._selected, item_index=False, anim=False
            )
        )
        return

    def set_current(self, index, item_index=True, anim=True):
        if item_index:
            item = self.get_item_children()[index]
            all_items = self.get_all_children()
            index = all_items.index(item)

        button = self.ids.items_box.children[index]
        y = button.pos[1]
        self._activete_button(button)
        self._set_selected(index)
        self._set_ghost_pos(y, anim=anim)

    def _activete_button(self, button):
        for item in self.get_item_children():
            item.active = False
        button.active = True
        return

    def get_item_children(self):
        children = [
            item
            for item in self.ids.items_box.children
            if issubclass(item.__class__, AKNavigationrailItem)
        ]
        return children

    def get_all_children(self):
        return [item for item in self.ids.items_box.children]

    def _set_selected(self, index):
        self._selected = index

    def on_size(self, *args):
        self.refresh_items()

    def add_widget(self, widget, index=0, canvas=None):
        if issubclass(widget.__class__, AKNavigationrailItem):
            self.ids.items_box.add_widget(widget)
            Clock.schedule_once(lambda x: self.set_current(-1, anim=False), 1)

        elif issubclass(widget.__class__, AKNavigationrailCustomItem):
            self.ids.items_box.add_widget(widget)

        elif issubclass(widget.__class__, AKNavigationrailContent):
            self.ids.content.add_widget(widget)
        else:
            return super().add_widget(widget, index=index, canvas=canvas)

    def _hide_text(self):
        for item in self.get_item_children():
            anim = Animation(
                item_text_opacity=0,
                duration=self.duration / 2,
                t=self.transition,
            )
            anim.start(item)

    def _show_text(self):
        for item in self.get_item_children():
            anim = Animation(
                item_text_opacity=1,
                duration=self.duration / 2,
                t=self.transition,
            )
            anim.start(item)
