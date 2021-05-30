Getting Started
=================

In order to start using `AKivyMD` you must have already installed `Kivy <https://kivy.org/doc/stable/>`_ and `KivyMD <https://kivymd.readthedocs.io/en/latest/>`_.
After installing these two libraries you can proceed to installing `AKivyMD`.


Installation
-------------------

Install the stable version of akivymd using this command.::

    pip install kivymd_extensions.akivymd

or if you wish to install the latest version directly from GitHub::

    pip install https://github.com/kivymd-extensions/akivymd/archive/main.zip

Basic Example
-------------------------

After installing `AKivyMD` you can now use the widgets directly inside your kivy program. Here is a
basic example to get you started out.

.. code-block:: python

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
