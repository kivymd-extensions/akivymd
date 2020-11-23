from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen

Builder.load_string(
    """
<Rating>:
    BoxLayout:
        orientation: 'vertical'
        MyToolbar:
            id: _toolbar

        FloatLayout:
            AKRating:
                normal_icon: 'star-circle-outline'
                active_icon: 'star-circle'
                pos_hint: {'center_x': .5, 'center_y': .3}
                on_rate: print(self.get_rate())

            AKRating:
                pos_hint: {'center_x': .5, 'center_y': .5}
                on_rate: print(self.get_rate())
                direction: 'rl'

            AKRating:
                normal_icon: 'star-box-outline'
                active_icon: 'star-box'
                active_color: 1,0,0.4,1
                animation_type: 'grow'
                pos_hint: {'center_x': .5, 'center_y': .7}
                on_rate: print(self.get_rate())

    """
)


class Rating(Screen):
    pass
