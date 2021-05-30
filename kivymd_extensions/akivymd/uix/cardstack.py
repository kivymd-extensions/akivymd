"""
Components/CardStack
=====================


.. rubric:: The AKCardStack displays an infinte stack of cards that can be swiped away.

Example
----------

.. code-block:: python

    from kivy.lang import Builder
    from kivymd.app import MDApp

    kv_string = '''
    <CardStack@MDScreen>:

        AKCardStack:
            id: cardstack
            pos_hint: {"center_x": .5, "center_y": .5}
            size: dp(800),dp(800)
            transition: "in_out_circ"

        MDRaisedButton:
            text: "change cards"
            on_press: root.change()
            pos_hint: {"center_x": .5, "y": .05}
    '''
    )


    class CardStack(MDApp):
        def build(self):
            return Builder.load_string(kv_string)

        def change(self):
            self.ids.cardstack.change()

    CardStack().run()


"""


from kivy.animation import Animation
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import (
    ColorProperty,
    ListProperty,
    NumericProperty,
    ObjectProperty,
    OptionProperty,
    StringProperty,
)
from kivy.uix.relativelayout import RelativeLayout
from kivymd.theming import ThemableBehavior

Builder.load_string(
    """
<AKCardStack>:
    id:stack_holder
    size_hint: None, None

    RelativeLayout:
        id:card3
        pos_hint: {"center_x": .5, "center_y": .5}

        canvas.before:
            PushMatrix
            Rotate:
                angle: 5
                axis: 0, 0, 1
                origin: root.center[0] - self.width / 1.8, root.center[1] + self.height / 2

        canvas.after:
            PopMatrix

        MDCard:
            size_hint: .4, .4
            md_bg_color: root.theme_cls.primary_dark if not root.third_color else root.third_color
            pos_hint: {"center_x": .42, "center_y": .5}
            elevation: 0
            radius: root.radius

    RelativeLayout:
        id: card2
        pos_hint: {"center_x":.5, "center_y":.5}

        canvas.before:
            PushMatrix
            Rotate:
                angle: 3
                axis: 0, 0, 1
                origin: root.center[0] - self.width / 1.8, root.center[1] + self.height / 2

        canvas.after:
            PopMatrix

        MDCard:
            size_hint: .4, .4
            md_bg_color: root.theme_cls.primary_color if not root.second_color else root.second_color
            pos_hint: {"center_x": .45, "center_y": .5}
            elevation: 0
            radius: root.radius

    RelativeLayout:
        id:card1
        pos_hint: {"center_x": .5, "center_y": .5}

        canvas.before:
            PushMatrix

            Rotate:
                angle: 0
                axis: 0, 0, 1
                origin: root.center[0] - self.width / 1.8, root.center[1] + self.height / 2

        canvas.after:
            PopMatrix

        MDCard:
            size_hint: .4, .4
            md_bg_color: root.theme_cls.primary_light if not root.first_color else root.first_color
            pos_hint: {"center_x": .5, "center_y": .5}
            elevation: root.elevation
            radius: root.radius
"""
)


class AKCardStack(ThemableBehavior, RelativeLayout):

    """
    Represents a stack of cards. Call the `change()` method on this class to
    change the stack of cards.

    Use the :attr:`current_card` to get front most card to add widgets to it.

    """

    radius = ListProperty([dp(20), dp(20), dp(20), dp(20)])
    """Sets the radius for all the cards

    :attr:`radius` is an :class:`~kivy.properties.ListProperty`
    and defaults to `[dp(20), dp(20), dp(20), dp(20)]`.

    """

    first_color = ColorProperty(None)
    """Sets the color of the front most card

    :attr:`first_color` is an :class:`~kivy.properties.ColorProperty`
    and defaults to `'app.theme_cls.primary_light'`.

    """

    second_color = ColorProperty(None)
    """Sets the color of the second most card

    :attr:`second_color` is an :class:`~kivy.properties.ColorProperty`
    and defaults to `'app.theme_cls.primary_color'`.

    """

    third_color = ColorProperty(None)
    """Sets the color of the last card

    :attr:`third_color` is an :class:`~kivy.properties.ColorProperty`
    and defaults to `'app.theme_cls.primary_dark'`.

    """

    current_card = ObjectProperty(None)
    """A read only property that returns the object of the front most card

    :attr:`current_card` is an :class:`~kivy.properties.ObjectProperty`
    and defaults to `None`.

    """

    transition = StringProperty("in_out_circ")
    """Type of animation interpolation to be used

    :attr:`transition` is an :class:`~kivy.properties.StringProperty`
    and defaults to `'in_out_circ'`.

    """

    card_out_direction = OptionProperty("down", options=["down", "up", "left", "right"])
    """Direction in which the front most card is animated out of the screen.
    Can be 'down', 'up', 'left' or 'right'.

    :attr:`card_out_direction` is an :class:`~kivy.properties.OptionProperty`
    and defaults to `'down'`.

    """

    card_in_direction = OptionProperty('side', options = ['bottom','top', 'side'])
    """Direction in which the new card to be added comes from.
    Can be 'side', 'bottom', or 'top'

    :attr:`card_in_direction` is an :class:`~kivy.properties.OptionProperty`
    and defaults to `'side'`.

    """

    elevation = NumericProperty(0)
    """The elevation of the front most card
    :attr:`elevation` is an :class:`~kivy.properties.NumericProperty`
    and defaults to `0`.

    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.counter = 1
        if not self.first_color:
            self.first_color = self.theme_cls.primary_light
        if not self.second_color:
            self.second_color = self.theme_cls.primary_color
        if not self.third_color:
            self.third_color = self.theme_cls.primary_dark
        Clock.schedule_once(self.initial_current_card, -1)

    def initial_current_card(self, time):
        """
        Sets the :attr:'current_card' at the start of the program
        """
        self.current_card = self.ids.card1.children[0]

    def change(self, *args):
        """
        Causes the CardStack to change to the next card
        """
        card_to_drop = "card" + str(self.counter)
        if self.card_out_direction == 'down':
            Animation(
                pos_hint={"center_x": 0.5, "center_y": -1},
                duration=0.3,
                t=self.transition,
            ).start(self.ids[card_to_drop].children[0])
        elif self.card_out_direction == 'up':
            Animation(
                pos_hint={"center_x": 0.5, "center_y": 1.5},
                duration=0.3,
                t=self.transition,
            ).start(self.ids[card_to_drop].children[0])
        elif self.card_out_direction == 'right':
            Animation(
                pos_hint={"center_x": 1.5, "center_y": .5},
                duration=0.3,
                t=self.transition,
            ).start(self.ids[card_to_drop].children[0])
        else:
            Animation(
                pos_hint={"center_x": -1, "center_y": .5},
                duration=0.3,
                t=self.transition,
            ).start(self.ids[card_to_drop].children[0])
        # Update the var current_card to reflect the new card brought to front
        if self.counter + 1 == 4:
            self.current_card = self.ids["card1"].children[0]
        else:
            self.current_card = self.ids[
                "card" + str(self.counter + 1)
            ].children[0]
        Clock.schedule_once(self.card_changer, 0.2)

    def card_changer(self, *args):
        """
        Internal function. Do not call this function use `change()` instead
        """
        # Rotate second card into palce
        if self.counter + 1 == 4:
            card2 = "card1"
        else:
            card2 = "card" + str(self.counter + 1)
        Animation(
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            elevation=self.elevation,
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
        if self.card_in_direction == 'side':
            new_card.children[0].pos_hint = {"center_x": 0.35, "center_y": 0.55}
        elif self.card_in_direction == 'top':
            new_card.children[0].pos_hint = {"center_x": 0.42, "center_y": 0.60}
        else:
            new_card.children[0].pos_hint = {"center_x": 0.42, "center_y": 0.4}
        new_card.children[0].md_bg_color = self.third_color
        new_card.children[0].opacity = 0
        self.add_widget(new_card, 4)
        Animation(
            opacity=1,
            pos_hint={"center_x": 0.42, "center_y": 0.5},
            elevation=0,
            duration=0.4,
        ).start(new_card.children[0])
        Animation(angle=5, duration=0.2).start(
            new_card.canvas.before.children[-1]
        )

        # Increment the counter variable and if passes 3 resest counter
        if self.counter != 3:
            self.counter += 1
        else:
            self.counter = 1
