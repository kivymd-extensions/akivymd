from kivy.lang.builder import Builder
from kivymd.uix.list import OneLineListItem
from kivymd.uix.screen import MDScreen

Builder.load_string(
    """
<SilverAppbar>

    AKSilverAppbar:
        max_height: dp(300)
        title: root.name
        left_action_items: [["arrow-left", lambda x: app.show_screen("Home", "back")]]
        pin_top: True
        hide_toolbar: True
        radius: dp(20)
        toolbar_bg: app.theme_cls.primary_color

        AKSilverAppbarHeader:
            orientation: "vertical"

            Image:
                source: "assets/fly.jpg"
                allow_stretch: True
                keep_ratio: False

        AKSilverAppbarContent:
            padding: dp(10)
            id: content
            size_hint_y: None
            height: self.minimum_height
            orientation: "vertical"
            md_bg_color: app.theme_cls.primary_color
"""
)


class SilverAppbar(MDScreen):
    def on_enter(self, *args):
        for x in range(30):
            self.ids.content.add_widget(OneLineListItem(text="Item %d" % x))

    def on_leave(self, *args):
        self.ids.content.clear_widgets()
