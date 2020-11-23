from kivy.lang.builder import Builder
from kivymd.uix.list import OneLineListItem
from kivymd.uix.screen import MDScreen

Builder.load_string(
    """
<MyLabel@MDLabel>
    valign: "center"
    theme_text_color: "Custom"
    text_color: 1,1,1,1

<SwipeMenu>

    AKSwipeMenu:
        id: menu
        on_open: but.icon = "arrow-down"
        on_dismiss: but.icon ="arrow-up"

        AKSwipeMenuMainContent:
            orientation: "vertical"

            MyToolbar:
                id: _toolbar

            ScrollView:
                MDBoxLayout:
                    id: list
                    adaptive_height: True
                    orientation: "vertical"

        AKSwipeMenuTopContent:

            MDBoxLayout:
                size_hint_y: None
                height: dp(60)
                padding: dp(10)

                MyLabel:
                    text: "Swipe up for more details"

                MDIconButton:
                    id: but
                    icon: "arrow-up"
                    pos_hint: {"center_y": .5}
                    theme_text_color: "Custom"
                    text_color: 1,1,1,1
                    on_release:
                        if menu.get_status()=="close": menu.open()
                        else:menu.dismiss()

        AKSwipeMenuBottomContent:

            MDBoxLayout:
                size_hint_y: None
                height: dp(400)

                MyLabel:
                    text: "My Widgets"
                    halign: "center"

"""
)


class SwipeMenu(MDScreen):
    def on_pre_enter(self, *args):
        self.ids.list.clear_widgets()
        for x in range(50):
            self.ids.list.add_widget(
                OneLineListItem(
                    text=f"Items {x}",
                )
            )
        return super().on_enter(*args)
