from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen

from kivymd.uix.list import OneLineListItem, MDList

from akivymd.uix.behaviors.addwidget import AKAddWidgetAnimationBehavior

Builder.load_string(
    """
<AddWidgetBehavior>:
    name: "AddWidgetBehavior"

    MDBoxLayout:
        orientation: "vertical"

        MDToolbar:
            title: root.name
            left_action_items: [["arrow-left", lambda x: app.show_screen("Home", "back")]]

        ScrollView:

            AnimatedBox:
                id: list
                transition: "fade_size"
"""
)


class AnimatedBox(MDList, AKAddWidgetAnimationBehavior):
    pass


class AddWidgetBehavior(Screen):
    def on_enter(self):
        self.update()

    def update(self, *args):
        items = []
        for x in range(20):
            items.append(OneLineListItem(text="item %d" % x, on_release=self.update))
        self.ids.list.items = items

    def on_leave(self):
        self.ids.list.clear_widgets()
