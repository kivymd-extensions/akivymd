from kivy.animation import Animation
from kivy.properties import (
    ListProperty,
    NumericProperty,
    OptionProperty,
    StringProperty,
)
from kivymd.utils import asynckivy


class AKAddWidgetAnimationBehavior:
    items = ListProperty()
    speed = NumericProperty(0.05)
    animation_duration = NumericProperty(0.15)
    transition = OptionProperty(
        "fade_size", options=["fade", "fade_size", "size"]
    )
    direction = OptionProperty("vertical", options=["horizontal", "vertical"])
    animation = StringProperty("out_quad")

    def on_items(self, *args):
        self.clear_widgets()

        async def add_item():
            for x in self.items:
                if "fade" in self.transition:
                    x.opacity = 0
                    anim = Animation(
                        opacity=1,
                        duration=self.animation_duration,
                        t=self.animation,
                    )

                if "size" in self.transition:
                    if self.direction == "horizontal":
                        current_width = x.width
                        x.size_hint_x = None
                        x.width = current_width / 2
                        anim = Animation(
                            width=current_width,
                            duration=self.animation_duration,
                            t=self.animation,
                        )
                        anim &= Animation(
                            opacity=1,
                            duration=self.animation_duration * 3,
                            t=self.animation,
                        )

                    elif self.direction == "vertical":
                        current_height = x.height
                        x.size_hint_y = None
                        x.height = current_height / 2
                        anim = Animation(
                            height=current_height,
                            duration=self.animation_duration,
                            t=self.animation,
                        )
                        anim &= Animation(
                            opacity=1,
                            duration=self.animation_duration * 3,
                            t=self.animation,
                        )

                anim.start(x)
                self.add_widget(x)
                await asynckivy.sleep(self.speed)

        return asynckivy.start(add_item())
