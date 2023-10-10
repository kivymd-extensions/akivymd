"""
Components/MusicPlayer
=========================

.. rubric:: A music player widgets that allows you to play a list of songs

.. note:: This widget may not work properly on android currently due to audio provider problems.

.. warning::

    If on desktop you need to change audio provider to any audio provider other than `sdl2`.
    Check `here to see how to set the environment variable <https://kivy.org/doc/stable/guide/environment.html#restrict-core-to-specific-implementation>`_.
    Remember that this must be set at the beginning of your program.


Example
-----------------

.. code-block:: python

    import os
    os.environ["KIVY_AUDIO"] = "ffpyplayer"
    from kivy.lang import Builder
    from kivymd.uix.screen import MDScreen

    Builder.load_string(
        '''
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

    '''
    )
    class MusicPlayer(MDScreen):
        pass


"""

from kivy.uix.relativelayout import RelativeLayout
from kivy.lang import Builder
from kivy.animation import Animation
from kivymd.theming import ThemableBehavior
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.metrics import dp
from kivy.properties import (
    ColorProperty,
    ListProperty,
    NumericProperty,
    ObjectProperty,
    StringProperty,
)
from kivymd.uix.behaviors import (
    CircularRippleBehavior,
    CircularElevationBehavior,
)


Builder.load_string(
    """
<AKMusicPlayer>
    size:dp(375),dp(125)
    size_hint:None,None

    MDCard:
        md_bg_color:root.md_bg_color
        elevation:root.card_elevation
        radius:root.radius
        pos_hint:{'center_x':.5, 'center_y':.5}

    MusicPic:
        id:musicpic
        _source:root.current_pic
        size_hint:None,None
        size:root.height+root.height/5, root.height+root.height/5
        pos_hint:{'center_x':0, 'center_y':.5}
        elevation:15

    MDLabel:
        text:root.current_song
        pos:dp(75),dp(40)
        bold:True
        theme_text_color: "Custom"
        text_color: self.theme_cls.text_color if not root.font_color else root.font_color

    MDLabel:
        text:root.current_singer
        pos:dp(75),dp(20)
        theme_text_color: "Custom"
        text_color:self.theme_cls.text_color if not root.font_color else root.font_color

    MDSlider:
        id:seeker
        pos_hint:{'right':1, 'center_y':.45}
        size_hint:.8,.1
        min:0
        max:root.current_song_length
        value:root.current_song_pos
        hint: False
        show_off:False
        color: self.theme_cls.primary_color if not root.seeker_color else root.seeker_color

    MDIconButton:
        icon:'skip-next-circle'
        pos_hint:{'right':.85, 'center_y':.2}
        user_font_size:'30sp'
        theme_text_color: "Custom"
        text_color: self.theme_cls.primary_color if not root.icon_color else root.icon_color
        on_release:root.skip_next()

    MDIconButton:
        id:play_button
        icon:'play'
        user_font_size:'30sp'
        theme_text_color: "Custom"
        text_color: self.theme_cls.primary_color if not root.icon_color else root.icon_color
        pos_hint:{'right':.65, 'center_y':.2}
        on_release:root.player()

    MDIconButton:
        icon:'skip-previous-circle'
        user_font_size:'30sp'
        theme_text_color: "Custom"
        text_color: self.theme_cls.primary_color if not root.icon_color else root.icon_color
        pos_hint:{'right':.45, 'center_y':.2}
        on_release:root.skip_previous()


<MusicPic>:
    canvas:
        Ellipse:
            pos:root.pos
            size:root.size
            source:root._source
        Color:
            rgba:1,1,1,1
        Ellipse:
            pos:root.pos[0]+root.size[0]/2-dp(10), root.pos[1]+root.size[1]/2-dp(10)
            size:dp(20),dp(20)
    canvas.before:
        PushMatrix
        Rotate:
            angle: root._angle
            origin: self.center
    canvas.after:
        PopMatrix

    """
)


class AKMusicPlayer(RelativeLayout, ThemableBehavior):

    md_bg_color = ColorProperty()
    """Color of the main MusicPlayer Card

    :attr:`md_bg_color` is an :class:`~kivy.properties.ColorProperty`
    and defaults to primary theme color of the app.

    """

    font_color = ColorProperty(None)
    """Color of label text

    :attr:`font_color` is an :class:`~kivy.properties.ColorProperty`
    and defaults to `'app.theme_cls.font_color'`.

    """

    icon_color = ColorProperty(None)
    """Color of icons

    :attr:`icon_color` is an :class:`~kivy.properties.ColorProperty`
    and defaults to `'app.theme_cls.primary_color'`

    """

    seeker_color = ColorProperty(None)
    """Color of seeker bar

    :attr:`seeker_color` is an :class:`~kivy.properties.ColorProperty`
    and defaults to `'app.theme_cls.primary_color'`.

    """

    card_elevation = NumericProperty(13)
    """Elevation of main MusicPlayer Card

    :attr:`card_elevation` is an :class:`~kivy.properties.NumericProperty`
    and defaults to '13'

    """

    radius = ListProperty([dp(20), dp(20), dp(20), dp(20)])
    """Radius of main MusicPlayer Card

    :attr:`radius` is an :class:`~kivy.properties.ListProperty`
    and defaults to '[dp(20), dp(20), dp(20), dp(20)]'.

    """

    file_paths = ListProperty([])
    """File paths of all songs to be played

    :attr:`filepath` is an :class:`~kivy.properties.ListProperty`
    and defaults to `None`.

    """

    songs = ListProperty(["Song1"])
    """List of all names of songs that are to be played by the widgets.
    Will display `Song1` if no song file paths are added.

    :attr:`songs` is an :class:`~kivy.properties.ListProperty`
    and defaults to `Song1`.

    """

    pictures = ListProperty()
    """List of all filepaths to pictures of songs to be played

    :attr:`pictures` is an :class:`~kivy.properties.ListProperty`
    and defaults to `None`.

    """

    singers = ListProperty(["Singer1"])
    """List of all singer names of all songs to be played.
    Will display `Singer1` if no singer file paths are added.

    :attr:`singers` is an :class:`~kivy.properties.ListProperty`
    and defaults to `Singer1`.

    """

    current_filepath = StringProperty()
    """Read only property of the file path of the currently playig song's filepath

    :attr:`current_filepath` is an :class:`~kivy.properties.StringProperty`
    and defaults to `None`.

    """

    current_song = StringProperty()
    """Read only Property that returns the name of the currently playing song

    :attr:`current_song` is an :class:`~kivy.properties.StringProperty`
    and defaults to `None`.

    """

    current_pic = StringProperty()
    """Read only Property that returns the album art of the current playing song

    :attr:`current_pic` is an :class:`~kivy.properties.StringProperty`
    and defaults to `None`.

    """

    current_singer = StringProperty()
    """Read only Property that returns the singer of the current playing song

    :attr:`current_singer` is an :class:`~kivy.properties.StringProperty`
    and defaults to `None`.

    """

    current_song_length = NumericProperty()
    """Read Only Property that returns the length of the current playing song in seconds

    :attr:`current_song_length` is an :class:`~kivy.properties.NumericProperty`
    and defaults to `None`.

    """

    current_song_pos = NumericProperty()
    """Read Only Property that returns the amount of seconds that has been played

    :attr:`current_song_pos` is an :class:`~kivy.properties.NumericProperty`
    and defaults to `None`.

    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self._current_setter, 0)

    def _current_setter(self, *args):
        self.current_song = self.songs[0]
        self.current_pic = self.pictures[0]
        self.current_singer = self.singers[0]
        self.song = SoundLoader.load(self.file_paths[0])
        Clock.schedule_interval(self._song_position, 1)
        self.current_song_length = self.song.length
        self.ids.seeker.bind(on_touch_up=self._seeker)

    def skip_next(self, *args):
        """
        Call this method to skip to the next song
        """
        try:
            self.song.unload()
        except:
            pass
        id = self.pictures.index(self.current_pic)
        if id+1 == len(self.songs): #We are at end of list so loop to start
            id=-1
        self.current_pic = self.pictures[id + 1]
        self.current_song = self.songs[id + 1]
        self.current_singer = self.singers[id + 1]
        anim1 = Animation(_angle=-720, d=0.5, t="out_circ")
        anim1.start(self.ids.musicpic)
        anim1.bind(on_complete=self._angle_reseter)
        self.song = SoundLoader.load(self.file_paths[id + 1])
        self.current_song_length = self.song.length
        self.ids.play_button.icon = "pause"

    def skip_previous(self, *args):
        """
        Call this method to skip to the previous song
        """
        try:
            self.song.unload()
        except:
            pass
        id = self.pictures.index(self.current_pic)
        self.current_pic = self.pictures[id - 1]
        self.current_song = self.songs[id - 1]
        self.current_singer = self.singers[id - 1]
        anim2 = Animation(_angle=720, d=0.5, t="out_circ")
        anim2.start(self.ids.musicpic)
        anim2.bind(on_complete=self._angle_reseter)
        self.song = SoundLoader.load(self.file_paths[id - 1])
        self.ids.play_button.icon = "pause"

    def _angle_reseter(self, *args):
        self.ids.musicpic._angle = 0
        self.song.play()

    def _song_position(self, *args):
        self.current_song_pos = self.song.get_pos()
        if int(self.song.get_pos()) == int(self.song.length):
            self.skip_next()

    def _seeker(self, instance, touch):
        if super(AKMusicPlayer, self).ids.seeker.collide_point(*touch.pos):
            self.song.seek(instance.value)
            return super(AKMusicPlayer, self).on_touch_up(touch)

    def player(self, *args):
        """
        Call this method to stop or play the song
        """
        if self.song.state == "play":
            self.song.stop()
            self.ids.play_button.icon = "play"
        else:
            self.song.play()
            self.ids.play_button.icon = "pause"


class MusicPic(CircularRippleBehavior, CircularElevationBehavior):

    _source = ObjectProperty()
    """Internal variable do not edit"""

    _angle = NumericProperty()
    """Internal variable do not edit"""
