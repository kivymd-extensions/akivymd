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
        pictures:'assets/music1.jpg','assets/music2.jpg','assets/music3.jpg'
        songs:"song1", 'song2', 'song3'
        singers:'Singer1','Singer2','Singer3'
        file_paths:'assets/music1.mp3','assets/music2.mp3','assets/music3.mp3'

"""
)


class MusicPlayer(MDScreen):
    pass
