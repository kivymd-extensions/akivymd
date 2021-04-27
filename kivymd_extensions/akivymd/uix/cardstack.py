from kivy.lang import Builder
from kivy.properties import ListProperty, ObjectProperty, ColorProperty, StringProperty
from kivymd.theming import ThemableBehavior
from kivy.uix.relativelayout import RelativeLayout
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.metrics import dp


Builder.load_string(
    """
<AKCardStack>:
    id:stack_holder
    size_hint:None,None
    RelativeLayout:
        id:card3
        pos_hint:{'center_x':.5, 'center_y':.5}
        canvas.before:
            PushMatrix
            Rotate:
                angle: 5
                axis: 0,0,1
                origin: root.center[0]-self.width/1.8, root.center[1]+self.height/2
        canvas.after:
            PopMatrix
        MDCard:
            size_hint:.4,.4
            md_bg_color:root.theme_cls.primary_dark if not root.third_color else root.third_color
            pos_hint:{'center_x':.42, "center_y":.5}
            elevation:0
            radius:root.radius



    RelativeLayout:
        id:card2
        pos_hint:{'center_x':.5, 'center_y':.5}
        canvas.before:
            PushMatrix
            Rotate:
                angle: 3
                axis: 0,0,1
                origin: root.center[0]-self.width/1.8, root.center[1]+self.height/2
        canvas.after:
            PopMatrix
        MDCard:
            size_hint:.4,.4
            md_bg_color:root.theme_cls.primary_color if not root.second_color else root.second_color
            pos_hint:{'center_x':.45, "center_y":.5}
            elevation:0
            radius:root.radius


    RelativeLayout:
        id:card1
        pos_hint:{'center_x':.5, 'center_y':.5}
        canvas.before:
            PushMatrix
            Rotate:
                angle:0
                axis: 0,0,1
                origin: root.center[0]-self.width/1.8, root.center[1]+self.height/2
        canvas.after:
            PopMatrix
        MDCard:
            size_hint:.4,.4
            md_bg_color:root.theme_cls.primary_light if not root.first_color else root.first_color
            pos_hint:{'center_x':.5, "center_y":.5}
            elevation:13
            radius:root.radius


"""
)


class AKCardStack(ThemableBehavior, RelativeLayout):

    radius = ListProperty([dp(20), dp(20), dp(20), dp(20)])
    """This sets the radius for all the cards"""

    first_color = ColorProperty(None)
    """This sets the color of the front most card"""

    second_color = ColorProperty(None)
    """This sets the color of the second most card"""

    third_color = ColorProperty(None)
    """Third sets the color of the last card"""

    current_card = ObjectProperty(None)
    """A read only property that returns the object of the front most card"""

    transition = StringProperty("in_out_circ")
    """Type of animation interpolation to be used"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.counter = 1
        if not self.first_color:
            self.first_color = self.theme_cls.primary_light
        if not self.second_color:
            self.second_color = self.theme_cls.primary_color
        if not self.third_color:
            self.third_color = self.theme_cls.primary_dark

    def change(self, *args):
        # We drop the first card out of the screen
        card_to_drop = "card" + str(self.counter)
        Animation(
            pos_hint={"center_x": 0.5, "center_y": -1}, duration=0.3, t=self.transition
        ).start(self.ids[card_to_drop].children[0])
        # Update the var current_card to reflect the new card brough to front
        if self.counter + 1 == 4:
            self.current_card = self.ids["card1"].children[0]
        else:
            self.current_card = self.ids["card" + str(self.counter + 1)].children[0]
        Clock.schedule_once(self.card_changer, 0.2)

    def card_changer(self, *args):
        # Rotate second card into palce
        if self.counter + 1 == 4:
            card2 = "card1"
        else:
            card2 = "card" + str(self.counter + 1)
        Animation(
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            elevation=13,
            md_bg_color=self.first_color,
            duration=0.3,
        ).start(self.ids[card2].children[0])
        Animation(angle=0, duration=0.4).start(
            self.ids[card2].canvas.before.children[-1]
        )

        # Rotate last card into place
        if self.counter + 2 == 4:
            card3 = "card1"
        elif self.counter + 2 == 5:
            card3 = "card2"
        else:
            card3 = "card3"
        Animation(
            pos_hint={"center_x": 0.45, "center_y": 0.5},
            elevation=0,
            md_bg_color=self.second_color,
            duration=0.5,
        ).start(self.ids[card3].children[0])
        Animation(angle=3, duration=0.5).start(
            self.ids[card3].canvas.before.children[-1]
        )

        # Remove the first card and add it back at the back of the stack as a new_card
        new_card = self.ids["card" + str(self.counter)]
        # Clear this card of its widgets
        new_card.children[0].clear_widgets()
        self.remove_widget(new_card)
        new_card.children[0].pos_hint = {"center_x": 0.35, "center_y": 0.55}
        new_card.children[0].md_bg_color = self.third_color
        new_card.children[0].opacity = 0
        self.add_widget(new_card, 4)
        Animation(
            opacity=1,
            pos_hint={"center_x": 0.42, "center_y": 0.5},
            elevation=13,
            duration=0.4,
        ).start(new_card.children[0])
        Animation(angle=5, duration=0.2).start(new_card.canvas.before.children[-1])

        # Increment the counter variable and if passes 3 resest counter
        if self.counter != 3:
            self.counter += 1
        else:
            self.counter = 1
