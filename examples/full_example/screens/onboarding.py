from kivy.lang.builder import Builder
from kivymd.toast import toast
from kivymd.uix.screen import MDScreen

Builder.load_string(
    """
<MyAKOnboardingItem@AKOnboardingItem>
    source: ""
    text: ""
    title: ""

    MDFloatLayout:

        Image:
            source: root.source
            pos_hint: {"center_x": .5, "y": .6}
            size_hint: .4, .3

        MDBoxLayout:
            orientation: "vertical"
            padding: dp(10)
            adaptive_height: True
            pos_hint: {"center_x": .5, "top": .5}
            spacing: dp(20)
            size_hint_x: .7

            canvas.before:
                Color:
                    rgba: app.theme_cls.primary_dark
                RoundedRectangle:
                    pos: self.pos
                    size: self.size

            MDLabel:
                text: root.title
                bold: True
                size_hint_y: None
                height: self.texture_size[1]
                theme_text_color: "Primary"
                font_style: "H6"
                halign: "center"
                valign: "center"

            MDLabel:
                size_hint_y: None
                height: self.texture_size[1]
                theme_text_color: "Primary"
                font_style: "Body1"
                halign: "center"
                valign: "center"
                text: root.text


<Onboarding>
    on_leave: boarding.reset()

    MDBoxLayout:
        orientation: "vertical"
        spacing: dp(10)

        AKOnboarding:
            id: boarding
            on_finish: root.finish_callback()
            circles_size: dp(15)

            MyAKOnboardingItem:
                source: "assets/slide_one_img.png"
                text: "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book"
                title:"What is Lorem Ipsum?"

            MyAKOnboardingItem:
                source: "assets/slide_two_img.png"
                text: "It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout."
                title:"Why do we use it?"

            MyAKOnboardingItem:
                source: "assets/slide_three_img.png"
                text: "Contrary to popular belief, Lorem Ipsum is not simply random text. It has roots in a piece of classical Latin literature from 45 BC, making it over 2000 years old."
                title:"Where does it come from?"
"""
)


class Onboarding(MDScreen):
    def finish_callback(self):
        toast("Finish callback")
