from kivy.lang import Builder
from kivymd.uix.screen import MDScreen

Builder.load_string(
    """
<SpinnerBox@MDBoxLayout>
    adaptive_height: True
    text: ""

    MDLabel:
        theme_text_color: "Primary"
        text: root.text
        size_hint_x: None
        width:dp(200)
        halign: "center"
        valign: "center"


<Spinners>

    on_leave:
        root.stop_animation()

    MDBoxLayout:
        orientation: "vertical"

        MyToolbar:
            id: _toolbar

        MDFloatLayout:
            padding: dp(10)

            AKSpinnerCircleFlip:
                id: circleflip
                spinner_size: dp(30)
                pos_hint: {"center_x": .5, "top": .9}

            AKSpinnerDoubleBounce:
                id:doublebounce
                spinner_size: dp(30)
                pos_hint: {"center_x": .5, "center_y": .7}

            AKSpinnerFoldingCube:
                id: foldingcube
                spinner_size: dp(40)
                pos_hint: {"center_x": .5, "center_y": .4}
                angle: 45

            AKSpinnerThreeDots:
                id: threedots
                spinner_size: dp(20)
                pos_hint: {"center_x": .5, "y": .1}

            Widget:

    MDBoxLayout:
        padding: dp(5)
        spacing: dp(5)

        MDRaisedButton:
            text: "Start"
            on_release: root.start_animation()

        MDRaisedButton:
            text: "Stop"
            on_release: root.stop_animation()
"""
)


class Spinners(MDScreen):
    def stop_animation(self):
        ids = self.ids
        ids.foldingcube.active = False
        ids.threedots.active = False
        ids.doublebounce.active = False
        ids.circleflip.active = False

    def start_animation(self):
        ids = self.ids
        ids.foldingcube.active = True
        ids.threedots.active = True
        ids.doublebounce.active = True
        ids.circleflip.active = True
