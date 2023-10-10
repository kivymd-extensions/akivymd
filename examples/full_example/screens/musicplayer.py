import os
os.environ["KIVY_AUDIO"] = "ffpyplayer"
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen

Builder.load_string(
    """
<MusicPlayer>:
    MyToolbar:
        id: _toolbar
        pos_hint: {"top": 1}

    AKMusicPlayer:
        pos:250,250
        pictures:'assets/music1.jpg','assets/music2.jpg'
        songs:"song1", 'song2'
        singers:'Singer1','Singer2'
        file_paths:'assets/music1.mp3','assets/music2.mp3'

"""
)


class MusicPlayer(MDScreen):
    pass
