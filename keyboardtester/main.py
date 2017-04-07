
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.label import Label
from kivy.utils import platform
from kivy.properties import (StringProperty, ListProperty,
                             NumericProperty)

import sys
from os import unlink
from os.path import abspath, join, exists

if platform =='android':
    from jnius import autoclass

# Crudely change the path just to make sure things work the same on
# the desktop
if abspath('.') not in sys.path:
    sys.path.append(abspath('.'))

class ColouredButton(ButtonBehavior, Label):
    background_normal = ListProperty([1, 1, 1, 1])
    background_down = ListProperty([0.5, 0.5, 0.5, 1])
    padding = NumericProperty(0)
    radius = NumericProperty(0)

class Manager(ScreenManager):
    pass

class DeviceInfoScreen(Screen):
    brand = StringProperty('NOT DETECTED')
    # device = StringProperty('NOT DETECTED')
    manufacturer = StringProperty('NOT DETECTED')
    model = StringProperty('NOT DETECTED')
    # product = StringProperty('NOT DETECTED')
    
    instruction_text = ('On each of the following screens, please '
                        'enter text with your keyboard using the '
                        'specific method requested.')

    no_output_text = ('Even if you see no keyboard output, keep typin g'
                      'as if the keyboard is working.')
    
    error_text = ('Don\'t worry if you make a mistake in any '
                  'way, just continue as instructed.')

    unavailibility_text = ('If your keyboard does not support the '
                           'requested input type, just click \'skip\'.')

    def __init__(self, *args, **kwargs):
        super(DeviceInfoScreen, self).__init__(*args, **kwargs)

        if platform == 'android':
            Build = autoclass('android.os.Build')
            self.brand = Build.BRAND
            # self.device = Build.DEVICE
            self.manufacturer = Build.MANUFACTURER
            self.model = Build.MODEL
            # self.product = Build.PRODUCT

        App.get_running_app().log('Brand: {}'.format(self.brand))
        App.get_running_app().log('Device: {}'.format(self.device))
        App.get_running_app().log('Manufacturer: {}'.format(self.manufacturer))
        App.get_running_app().log('Model: {}'.format(self.model))
        App.get_running_app().log('Product: {}'.format(self.product))



class TapInputScreen(Screen):
    pass

class SwipeInputScreen(Screen):
    pass

class SuggestionInputScreen(Screen):
    pass


class KeyboardTesterApp(App):
    def build(self):
        self.reset_log()
        return Manager()

    def reset_log(self):
        if exists('keyboard_log.txt'):
            unlink('keyboard_log.txt')

    def log(self, s, newline=True):
        if newline and not s.endswith('\n'):
            s = s + '\n'
        with open('keyboard_log.txt', 'a') as fileh:
            fileh.write(s)



if __name__ == '__main__':
    KeyboardTesterApp().run()
