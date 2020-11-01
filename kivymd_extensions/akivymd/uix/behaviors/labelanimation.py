from kivy.animation import Animation
from kivy.lang.builder import Builder
from kivy.properties import BooleanProperty, NumericProperty, StringProperty

Builder.load_string(
    """
<AKAnimationBehaviorBase>:
    canvas.before:
        PushMatrix
        Rotate:
            angle: root._angle
            origin: self.center

    canvas.after:
        PopMatrix
"""
)


class AKAnimationBehaviorBase:

    duartion = NumericProperty(0.5)
    transition = StringProperty("out_cubic")
    animation_disabled = BooleanProperty(False)

    _angle = NumericProperty()
    _first_text = True

    def _start_animate(self):
        if self.animation_disabled:
            return

        if self._angle <= 180:
            _angle = 360
        else:
            _angle = 0

        if not self._first_text:
            anim = Animation(
                _angle=_angle, duration=self.duartion, t=self.transition
            )
            anim.start(self)

        self._first_text = False


class AKAnimationTextBehavior(AKAnimationBehaviorBase):
    def on_text(self, *args):
        self._start_animate()


class AKAnimationIconBehavior(AKAnimationBehaviorBase):
    def on_icon(self, *args):
        self._start_animate()
