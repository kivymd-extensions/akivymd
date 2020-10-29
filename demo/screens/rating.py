from kivy.lang.builder import Builder

from kivymd.uix.screen import MDScreen

Builder.load_string(
    """
<Rating>
    name: "Rating"

    MDToolbar:
        title: root.name
        left_action_items: [["arrow-left", lambda x: app.show_screen("Home", "back")]]
        pos_hint: {"top": 1}

    AKRating:
        direction: "lr"
        pos_hint: {"center_x": .5, "center_y": .35}
        on_rate: print(self.get_rate())

    AKRating:
        direction: "rl"
        animation_type: "wobble"
        pos_hint: {"center_x": .5, "center_y": .45}
        on_rate: print(self.get_rate())

    AKRating:
        animation_type: "shake"
        active_color: app.theme_cls.primary_color
        icon_size: "45dp"
        pos_hint: {"center_x": .5, "center_y": .55}
        on_rate: print(self.get_rate())
"""
)


class Rating(MDScreen):
    pass
