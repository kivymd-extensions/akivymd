# Awesome KivyMD

Awesome KivyMD is a package containing customized and non-material widgets for KivyMD.

<p align="center">
    <img align="center" width="512" src="https://raw.githubusercontent.com/quitegreensky/akivymd/master/images/preview.gif"/>
</p>

## Installation

```bash
pip install kivymd_extensions.akivymd

#or

pip install https://github.com/kivymd-extensions/akivymd/archive/main.zip
```

## Usage with Buildozer

```bash
requirements = https://github.com/kivymd-extensions/akivymd/archive/main.zip
```

### Dependencies:

- [KivyMD](https://github.com/kivymd/KivyMD) >= 1.1.1 (from master branch)
- [Kivy](https://github.com/kivy/kivy) >= 2.2.1 ([Installation](https://kivy.org/doc/stable/gettingstarted/installation.html))
- [Python 3.7+](https://www.python.org/)

> **_NOTE:_**
It's recommened to install the most recent version of `KivyMD` from master:
```bash
pip install https://github.com/kivymd/KivyMD/archive/refs/heads/master.zip
```

## Documentation

### Usage

```python
from kivy.lang import Builder

from kivymd.app import MDApp
import kivymd_extensions.akivymd

KV = """
<NavigationButton@Button_Item>
    icon_color: app.theme_cls.text_color
    text_color: app.theme_cls.text_color
    button_bg_color: app.theme_cls.primary_color
    mode: 'color_on_active'
    badge_disabled: True


MDScreen:

    AKBottomNavigation2:
        bg_color: app.theme_cls.bg_darkest

        NavigationButton:
            text: 'Alert'
            icon: 'bell-outline'

        NavigationButton:
            text: 'Bank'
            icon: 'bank-outline'

        NavigationButton:
            text: 'Download'
            icon: 'arrow-down-bold-outline'
"""


class Test(MDApp):
    def build(self):
        return Builder.load_string(KV)


Test().run()
```

## Examples

```bash
git clone https://github.com/kivymd-extensions/akivymd.git
cd akivymd
cd examples/full_example
python main.py
```

## Build Docs

```bash
git clone https://github.com/kivymd-extensions/akivymd.git
cd docs
sphinx-build -b html sources ./_build
```

## Support

If you need assistance or you have a question, you can ask for help on our mailing list:

- **Discord server:** https://discord.gg/wu3qBST
- _Email:_ kivydevelopment@gmail.com

## License

[MIT License](LICENSE)
