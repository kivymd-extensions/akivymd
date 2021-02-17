from kivy.animation import Animation
from kivy.clock import Clock
from kivy.lang.builder import Builder
from kivy.properties import ListProperty, NumericProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDFillRoundFlatButton

from kivymd_extensions.akivymd.uix.spinners import AKSpinnerDoubleBounce

Builder.load_string(
    """
<Message_label@BoxLayout>:
    icon: ""
    text: ""
    padding: dp(4)
    MDIcon:
        size_hint_x: None
        width: dp(20)
        icon: root.icon
        theme_text_color: "Custom"
        text_color: 1, 1 ,1, 1
        halign: "center"
        valign: "center"

    MDLabel:
        text: root.text
        halign: "center"
        valign: "center"
        font_style: "Caption"
        theme_text_color: "Custom"
        text_color: 1, 1, 1, 1

<AKProgressbutton>:
    size_hint: None,None
    size: self.minimum_size

    FloatLayout:
        id: float_box
        size_hint: None, None

        BoxLayout: ## Success
            id: _success_box
            pos_hint: {"center_x": .5, "center_y": .5}

            canvas.before:
                Color:
                    rgba: root.success_color
                    a: root._success_opacity
                RoundedRectangle:
                    size: root._success_box_size
                    pos: [self.x + self.width / 2 - root._success_box_size[0] / 2, self.y]
                    radius: [self.height / 2]

            Message_label:
                id: _success_label
                opacity: 0
                icon: root.success_icon
                text: root.success_text

        BoxLayout: ## Failure
            id: _failure_box
            pos_hint: {"center_x": .5, "center_y": .5}

            canvas.before:
                Color:
                    rgba: root.failure_color
                    a: root._failure_opacity
                RoundedRectangle:
                    size: root._failure_box_size
                    pos: [self.x + self.width / 2 - root._failure_box_size[0] / 2, self.y]
                    radius: [self.height / 2]

            Message_label:
                id: _failure_label
                opacity: 0
                icon: root.failure_icon
                text: root.failure_text
"""
)


class AKProgressbutton(BoxLayout):

    success_icon = StringProperty("check")
    success_text = StringProperty("Success")
    success_color = ListProperty([0, 0.7, 0, 1])

    failure_icon = StringProperty("close")
    failure_text = StringProperty("Failed")
    failure_color = ListProperty([1, 0, 0, 1])

    duration = NumericProperty(0.2)
    animation = StringProperty("out_quad")

    _success_box_size = ListProperty([0, 0])
    _failure_box_size = ListProperty([0, 0])
    _success_opacity = NumericProperty(0)
    _failure_opacity = NumericProperty(0)

    reset_timeout = NumericProperty(2)

    def __init__(self, button=None, spinner=None, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(lambda x: self._update())
        self.button = button
        self.spinner = spinner

    def _update(self):

        if not self.button:
            self.button = MDFillRoundFlatButton(text="Ok")

        if not self.spinner:
            self.spinner = AKSpinnerDoubleBounce()

        self.button.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        self.button.bind(on_release=self._submit)

        self.spinner.pos_hint = {"center_x": 0.5, "center_y": 0.5}

        self.ids.float_box.add_widget(self.button)
        self.ids.float_box.add_widget(self.spinner)

        self.ids.float_box.size = self.button.size
        self.spinner.spinner_size = self.button.height

        self._success_box_size = [0, self.button.height]
        self._failure_box_size = [0, self.button.height]

    def _spinner_state(self, state):
        self.spinner.active = state

    def _submit(self, instance):
        self._spinner_state(True)
        self._hide_button()

    def _hide_button(self, *args):
        anim = Animation(opacity=0, duration=self.duration, t=self.animation)
        anim.start(self.button)
        self.button.disabled = True

    def success(self):
        self._spinner_state(False)
        anim_box = Animation(
            _success_opacity=1,
            _success_box_size=self.button.size,
            duration=self.duration,
            t=self.animation,
        )
        anim_label = Animation(
            opacity=1, duration=self.duration, t=self.animation
        )

        anim_box.start(self)
        anim_label.start(self.ids._success_label)

        Clock.schedule_once(
            lambda x: self._reset(), self.reset_timeout + self.duration
        )

    def failure(self):
        self._spinner_state(False)
        anim_box = Animation(
            _failure_opacity=1,
            _failure_box_size=self.button.size,
            duration=self.duration,
            t=self.animation,
        )
        anim_label = Animation(
            opacity=1, duration=self.duration, t=self.animation
        )

        anim_box.start(self)
        anim_label.start(self.ids._failure_label)

        Clock.schedule_once(
            lambda x: self._reset(), self.reset_timeout + self.duration
        )

    def _reset(self):
        self.button.disabled = False
        self._spinner_state(False)
        button_anim = Animation(
            opacity=1, duration=self.duration, t=self.animation
        )

        success_box = Animation(
            _success_opacity=0,
            _success_box_size=[0, self.button.height],
            duration=self.duration,
            t=self.animation,
        )
        success_label = Animation(
            opacity=0, duration=self.duration, t=self.animation
        )

        failure_box = Animation(
            _failure_opacity=0,
            _failure_box_size=[0, self.button.height],
            duration=self.duration,
            t=self.animation,
        )
        failure_label = Animation(
            opacity=0, duration=self.duration, t=self.animation
        )

        button_anim.start(self.button)
        success_box.start(self)
        success_label.start(self.ids._success_label)
        failure_box.start(self)
        failure_label.start(self.ids._failure_label)
