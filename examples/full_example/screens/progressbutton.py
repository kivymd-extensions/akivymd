import time
from threading import Thread

from kivy.lang.builder import Builder
from kivymd.uix.screen import MDScreen

Builder.load_string(
    """
#:import MDFillRoundFlatIconButton kivymd.uix.button.MDFillRoundFlatIconButton


<ProgressButton>

    MDBoxLayout:
        orientation: "vertical"

        MyToolbar:
            id: _toolbar

        MDFloatLayout:

            AKProgressbutton:
                id: progressbutton_success
                pos_hint: {"center_x": .5, "center_y": .7}
                button: MDFillRoundFlatIconButton(text="Start", on_release=root.success, icon="language-python")

            AKProgressbutton:
                id: progressbutton_failure
                pos_hint: {"center_x": .5, "center_y": .3}
                button: MDFillRoundFlatIconButton(text="Start", on_release=root.failure, icon="language-python")
"""
)


class ProgressButton(MDScreen):
    def success(self, *args):
        t = Thread(target=self.start_success)
        t.start()

    def failure(self, *args):
        t = Thread(target=self.start_failure)
        t.start()

    def start_success(self, *args):
        time.sleep(3)
        return self.ids.progressbutton_success.success()

    def start_failure(self, *args):
        time.sleep(3)
        return self.ids.progressbutton_failure.failure()
