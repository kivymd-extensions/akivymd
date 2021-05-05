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
            angle: root.angle
            origin: self.center
    canvas.after:
        PopMatrix

    """
)


class AKMusicPlayer(RelativeLayout, ThemableBehavior):

    """NOTE: Add this to the beginning of your python value before importing kivy

    import os
    os.environ['KIVY_AUDIO'] = 'ffpyplayer'

    This is required as the default sdl2 audio provider doesnt allow the ability to seek and
    detect length of audio
    """

    md_bg_color = ColorProperty()
    """Color of the main MusicPlayer Card"""

    font_color = ColorProperty(None)
    """Color of the label's text"""

    icon_color = ColorProperty(None)
    """color of the icons"""

    seeker_color = ColorProperty(None)
    """color of the seeker bar"""

    card_elevation = NumericProperty(13)
    """Elevation of the main MusicPlayer Card"""

    radius = ListProperty([dp(20), dp(20), dp(20), dp(20)])
    """Radius of the main MusicPlayer Card"""

    file_paths = ListProperty([])
    """File paths of all songs to be played"""

    songs = ListProperty(["Song1"])
    """List of all names of songs that are to be played by the widgets"""

    pictures = ListProperty()
    """List of all filepaths to pictures of songs to be played"""

    singers = ListProperty(["Singer1"])
    """List of all singer names of all songs to be played"""

    current_filepath = StringProperty()
    """Read only property of the file path of the currently playig song's filepath"""

    current_song = StringProperty()
    """Read only Property that returns the name of the currently playing song"""

    current_pic = ObjectProperty()
    """Read only Property that returns the album art of the current playing song"""

    current_singer = StringProperty()
    """Read only Property that returns the singer of the current playing song"""

    current_song_length = NumericProperty()
    """Read Only Property that returns the length of the current playing song in seconds"""

    current_song_pos = NumericProperty()
    """Read Only Property that returns the amount of seconds that is currently being played"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.current_setter, 0)

    def current_setter(self, *args):
        self.current_song = self.songs[0]
        self.current_pic = self.pictures[0]
        self.current_singer = self.singers[0]
        self.song = SoundLoader.load(self.file_paths[0])
        Clock.schedule_interval(self.song_position, 1)
        self.current_song_length = self.song.length
        self.ids.seeker.bind(on_touch_up=self.seeker)

    def skip_next(self, *args):
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
        anim1 = Animation(angle=-720, d=0.5, t="out_circ")
        anim1.start(self.ids.musicpic)
        anim1.bind(on_complete=self.angle_reseter)
        self.song = SoundLoader.load(self.file_paths[id + 1])
        self.current_song_length = self.song.length
        self.ids.play_button.icon = "pause"

    def skip_previous(self, *args):
        try:
            self.song.unload()
        except:
            pass
        id = self.pictures.index(self.current_pic)
        self.current_pic = self.pictures[id - 1]
        self.current_song = self.songs[id - 1]
        self.current_singer = self.singers[id - 1]
        anim2 = Animation(angle=720, d=0.5, t="out_circ")
        anim2.start(self.ids.musicpic)
        anim2.bind(on_complete=self.angle_reseter)
        self.song = SoundLoader.load(self.file_paths[id - 1])
        self.ids.play_button.icon = "pause"

    def angle_reseter(self, *args):
        self.ids.musicpic.angle = 0
        self.song.play()

    def song_position(self, *args):
        self.current_song_pos = self.song.get_pos()
        if int(self.song.get_pos()) == int(self.song.length):
            self.skip_next()

    def seeker(self, instance, touch):
        if super(AKMusicPlayer, self).ids.seeker.collide_point(*touch.pos):
            self.song.seek(instance.value)
            return super(AKMusicPlayer, self).on_touch_up(touch)

    def player(self, *args):
        if self.song.state == "play":
            self.song.stop()
            self.ids.play_button.icon = "play"
        else:
            self.song.play()
            self.ids.play_button.icon = "pause"


class MusicPic(CircularRippleBehavior, CircularElevationBehavior):

    _source = ObjectProperty()
    # Do not edit this property

    angle = NumericProperty()
    # Do not edit this property
