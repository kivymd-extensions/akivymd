# Awesome KivyMD

Awesome KivyMD is a package containing customized and non-material widgets for KivyMD.

<p align="center">
    <img align="center" width="512" src="https://raw.githubusercontent.com/quitegreensky/akivymd/master/images/preview.gif"/>
</p>

## Installation

```bash
pip install kivymd-components
components install akivymd
```

## Usage

```python
from kivy.lang import Builder

from kivymd.app import MDApp
import kivymd.components.akivymd

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

## Usage with Buildozer

For now we cannot specify dependencies in the `buildozer.spec` specification file in the `garden_requirements` 
(for example, like `components_requirements`) parameter. Instead, you must navigate to the root directory of your project,
where the buildozer.spec file is located, and issue the command:

```bash
pip install kivymd-components
components install --app akivymd
```

The component package will be installed locally in your project. Remember to import a package of components as follows:

```python
from kivymd.components.akivymd.uix.widget import Widget
```

### Dependencies:

- [Kivy](https://github.com/kivy/kivy) >= 1.10.1 ([Installation](https://kivy.org/doc/stable/gettingstarted/installation.html))
- [KivyMD](https://github.com/kivymd/KivyMD) >= 0.104.2 (`pip install https://github.com/kivymd/KivyMD/archive/master.zip
`)
- [Python 3.6+](https://www.python.org/) _(Python 2 not supported)_

### Support

If you need assistance or you have a question, you can ask for help on our mailing list:

- **Discord server:** https://discord.gg/RxbT5wF

## License
[MIT](https://choosealicense.com/licenses/mit/)
