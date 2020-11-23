import threading

from kivy.lang import Builder
from kivy.network.urlrequest import UrlRequest
from kivy.uix.screenmanager import Screen
from kivymd.toast import toast
from kivymd.uix.card import MDCard

Builder.load_string(
    """
<DataloaderLabel@AKLabelLoader>
    size_hint_y: None
    height: dp(20)
    theme_text_color: "Primary"
    halign: "left"


<Loadercard>
    padding: "8dp"
    size_hint: None, None
    size: dp(280), dp(140)
    pos_hint: {"center_x": .5, "center_y": .5}
    name: ""
    email: ""
    website: ""
    avatar: ""

    MDBoxLayout:

        MDFloatLayout:
            size_hint_x: .3

            AKImageLoader:
                size_hint: None,None
                size: dp(50), dp(50)
                pos_hint: {"center_x": .5 , "center_y": .5}
                source: root.avatar

        MDBoxLayout:
            orientation: "vertical"
            size_hint_x: .7
            padding: dp(10)
            spacing: dp(10)

            DataloaderLabel:
                text:  root.name

            MDSeparator:

            DataloaderLabel:
                text:  root.email

            MDSeparator:

            DataloaderLabel:
                text: root.website


<Dataloader>
    on_leave: root.clear_data()

    MDBoxLayout:
        orientation: "vertical"

        MyToolbar:
            id: _toolbar

        ScrollView:

            MDBoxLayout:
                adaptive_height: True
                spacing: dp(24)
                padding: dp(24)
                orientation: "vertical"

                Loadercard:
                    id: user1

                Loadercard:
                    id: user2

        MDBoxLayout:
            adaptive_height: True
            padding: dp(5)
            spacing: dp(5)

            MDRaisedButton:
                text: "Get Online Data"
                on_release: root.get_date()

            MDRaisedButton:
                text: "Clear Data"
                on_release: root.clear_data()
"""
)


class Dataloader(Screen):
    def get_date(self):
        t = threading.Thread(target=self.send_request)
        t.start()

    def set_user1(self, *args):
        user1 = args[1]
        self.ids.user1.avatar = "https://cdn4.iconfinder.com/data/icons/avatars-21/512/avatar-circle-human-male-3-512.png"
        self.ids.user1.name = user1["name"]
        self.ids.user1.email = user1["email"]
        self.ids.user1.website = user1["website"]

    def set_user2(self, *args):
        user2 = args[1]
        self.ids.user2.name = user2["name"]
        self.ids.user2.email = user2["email"]
        self.ids.user2.website = user2["website"]
        self.ids.user2.avatar = "https://cdn4.iconfinder.com/data/icons/avatars-21/512/avatar-circle-human-male-3-512.png"

    def send_request(self):
        url = "https://jsonplaceholder.typicode.com/"

        UrlRequest(
            url + "users/1", self.set_user1, on_error=self.got_error, timeout=4
        )
        UrlRequest(
            url + "users/2", self.set_user2, on_error=self.got_error, timeout=4
        )
        return True

    def got_error(self, *args):
        error_msg = "Timeout.Check connection"
        return toast(error_msg)

    def clear_data(self):
        self.ids.user2.name = ""
        self.ids.user2.email = ""
        self.ids.user2.website = ""
        self.ids.user2.avatar = ""
        self.ids.user1.avatar = ""
        self.ids.user1.name = ""
        self.ids.user1.email = ""
        self.ids.user1.website = ""


class Loadercard(MDCard):
    pass
