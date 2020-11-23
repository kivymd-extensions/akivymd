from kivy.lang.builder import Builder
from kivymd.uix.list import OneLineListItem
from kivymd.uix.screen import MDScreen

Builder.load_string(
    """

<Toolbar>

    AKToolbarLayout:
        id: toolbar

        AKToolbarClass:
            MyToolbar:
                id: _toolbar

        AKToolbarContent:
            id: box

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

        AKToolbarFloatingButton:
            MDFloatingActionButton:
                icon: 'arrow-up'
                on_release: toolbar.scroll_to(1)

"""
)


class Toolbar(MDScreen):
    def on_pre_enter(self, *args):
        for x in range(30):
            self.ids.box.add_widget(OneLineListItem(text=f"List {x}"))
        return super().on_pre_enter(*args)

    def on_leave(self, *args):
        self.ids.box.clear_widgets()
        return super().on_leave(*args)
