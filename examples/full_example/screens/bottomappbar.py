from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen
from kivymd.toast import toast

Builder.load_string(
    """
<BottomAppbar>:

    MDBoxLayout:
        orientation: "vertical"

        MyToolbar:
            id: _toolbar

        MDBoxLayout:

    AKFloatingRoundedAppbar:

        AKFloatingRoundedAppbarButtonItem:
            icon: "magnify"
            text: "Search"
            on_release: root.toast(self.text)

        AKFloatingRoundedAppbarButtonItem:
            icon: "plus"
            text: "Add"
            on_release: root.toast(self.text)

        AKFloatingRoundedAppbarButtonItem:
            icon: "dots-vertical"
            text: "Menu"
            on_release: root.toast(self.text)

        AKFloatingRoundedAppbarAvatarItem:
            source: "assets/google.jpg"

        AKFloatingRoundedAppbarAvatarItem:
            source: "assets/google.jpg"
            text: "Google"
"""
)


class BottomAppbar(Screen):
    def toast(self, x):
        return toast(x)
