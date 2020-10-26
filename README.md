# Awesome KivyMD

Awesome KivyMD is a package containing customized and non-material widgets for KivyMD.

## Installation

```bash
pip install kivymd-components
components install akivymd
```

## Usage Example

```
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

## Examples
<p align="center">
<img align="center" width="512" src="https://raw.githubusercontent.com/quitegreensky/akivymd/master/images/preview.gif"/>
</p>

## Contributing

## License
[MIT](https://choosealicense.com/licenses/mit/)
