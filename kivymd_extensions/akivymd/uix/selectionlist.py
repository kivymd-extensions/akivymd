from kivy.animation import Animation
from kivy.lang import Builder
from kivy.properties import BooleanProperty, NumericProperty, StringProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivymd.theming import ThemableBehavior
from kivymd.uix.behaviors import CircularRippleBehavior

Builder.load_string(
    """
<AKSelectList>
    orientation: "lr-tb"
    spacing: dp(5)
    padding: dp(10)
    size_hint_y: None
    height: self.minimum_height


<AKSelectListAvatarItem>
    orientation: "vertical"
    size_hint: 1 / root.columns, None
    height: self.width * 1.2
    padding: dp(5)
    spacing: dp(5)
    on_release: root._choose_selection(_first_label.text)

    FloatLayout:
        Image:
            pos_hint: {"center_x": .5, "center_y": .5}
            keep_ratio: True
            source: root.source

        MDIcon:
            id: _box
            pos_hint: {"center_x": 0.9, "center_y": 0.9}
            size_hint: None,None
            font_size: 0
            icon: "check-circle"
            color: root.theme_cls.primary_color

    BoxLayout:
        size_hint_y: None
        height: dp(50)
        orientation: "vertical"
        spacing: dp(4)

        MDLabel:
            id: _first_label
            text: root.first_label
            theme_text_color: "Primary"
            halign: "center"

        MDLabel:
            text: root.second_label
            halign: "center"
            theme_text_color: "Secondary"
            font_style: "Caption"
"""
)


class AKSelectListAvatarItem(
    ThemableBehavior, ButtonBehavior, CircularRippleBehavior, BoxLayout
):
    columns = NumericProperty(4)
    source = StringProperty("")
    first_label = StringProperty("")
    second_label = StringProperty("")
    animate_start = BooleanProperty(True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _choose_selection(self, select):

        selected_list = self.parent._selected_list

        if select not in selected_list:
            selected_list.append(select)
            self._selection_anim()

        else:
            selected_list.remove(select)
            self._deselection_anim()

        if not selected_list:
            selected_list = []

        self.parent._selected_list = selected_list

    def _selection_anim(self):
        anim = Animation(font_size=self.width / 3, t="out_bounce", duration=0.1)
        anim.start(self.ids._box)

    def _deselection_anim(self):
        anim = Animation(
            font_size=0,
            size=self.ids._box.texture_size,
            t="in_bounce",
            duration=0.1,
        )
        anim.start(self.ids._box)


class AKSelectList(StackLayout):
    _selected_list = []

    def get_selection(self):
        return self._selected_list

    def clear_selection(self):
        if not self.children:
            return

        for child in self.children:
            if child.first_label in self._selected_list:
                child._deselection_anim()
        self._selected_list = []

    def select_all(self):
        for child in self.children:
            if child.first_label not in self._selected_list:
                child._selection_anim()
                self._selected_list.append(child.first_label)
