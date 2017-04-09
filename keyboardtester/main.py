from __future__ import print_function

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.label import Label
from kivy.utils import platform
from kivy.properties import (StringProperty, ListProperty,
                             NumericProperty, ObjectProperty)

from kivy.core.window import Window
Window.softinput_mode = 'pan'

import sys
from os import unlink
from os.path import abspath, join, exists

if platform =='android':
    from jnius import autoclass

# Crudely change the path just to make sure things work the same on
# the desktop
if abspath('.') not in sys.path:
    sys.path.append(abspath('.'))

from scrolllabel import ScrollLabel

if platform == 'android':
    from jnius import autoclass
    Environment = autoclass('android.os.Environment')
    activity = autoclass('org.kivy.android.PythonActivity').mActivity
    # directory = Environment.getExternalStorageDirectory(None)
    directory = activity.getExternalFilesDir(None)
    filename = join(directory.getAbsolutePath(), 'keyboard_log.txt')
else:
    filename = abspath('keyboard_log.txt')

print('filename is', filename)

def send_email(text, filen):
    print('Asked to send email with text {} and file {}'.format(text, filen))
    if platform == 'android':
        send_email_android(text, filen)
    else:
        import webbrowser
        webbrowser.open('test')

def send_email_android(text, filen):
    from jnius import autoclass, cast

    Intent = autoclass('android.content.Intent')
    AndroidString = autoclass('java.lang.String')
    Uri = autoclass('android.net.Uri')

    activity = autoclass('org.kivy.android.PythonActivity').mActivity

    intent = Intent(Intent.ACTION_SEND)
    intent.setType('message/rfc822')

    recipient = 'alexanderjohntaylor@gmail.com'
    subject = 'Kivy keyboard log'

    intent.putExtra(Intent.EXTRA_EMAIL, [recipient])

    android_subject = cast('java.lang.CharSequence',
                            AndroidString(subject))
    intent.putExtra(Intent.EXTRA_SUBJECT, android_subject)

    android_text = cast('java.lang.CharSequence',
                        AndroidString(text))
    intent.putExtra(Intent.EXTRA_TEXT, android_text)

    # File = autoclass('java.io.File')
    # file_object = File(filen)
    # print('file is', file_object)
    file_uri = Uri.parse('file://{}'.format(filen))
    # file_uri = Uri.fromFile(file_object)
    # print('uri is', file_uri)
    intent.putExtra(Intent.EXTRA_STREAM, cast('android.os.Parcelable', file_uri))
    # intent.putExtra(Intent.EXTRA_STREAM, Uri.parse('file://{}'.format(filen)))
    # intent.putExtra(Intent.EXTRA_STREAM, 'file://{}'.format(filen))

    chooser_title = cast('java.lang.CharSequence',
                            AndroidString('Send message with:'))
    activity.startActivity(Intent.createChooser(intent,
                                                chooser_title))
    # activity.startActivity(intent)


class ColouredButton(ButtonBehavior, Label):
    background_normal = ListProperty([1, 1, 1, 1])
    background_down = ListProperty([0.5, 0.5, 0.5, 1])
    padding = NumericProperty(0)
    radius = NumericProperty(0)

class Manager(ScreenManager):
    pass

class OrderedScreen(Screen):
    next_screen = StringProperty()
    textinput = ObjectProperty()

    def on_pre_enter(self):
        App.get_running_app().log('SCREEN: {}'.format(self.name))

    def skip(self):
        App.get_running_app().log('result: SKIP', prefix='  ')
        self.next()

    def done(self):
        App.get_running_app().log('result: DONE', prefix='  ')
        self.next()

    def next(self):
        App.get_running_app().root.current = self.next_screen

    def reset(self):
        if self.textinput is not None:
            self.textinput.focus = False
            self.textinput.text = ''

class DeviceInfoScreen(OrderedScreen):
    brand = StringProperty('NOT DETECTED')
    # device = StringProperty('NOT DETECTED')
    manufacturer = StringProperty('NOT DETECTED')
    model = StringProperty('NOT DETECTED')
    # product = StringProperty('NOT DETECTED')
    
    instruction_text = ('On each of the following screens, please '
                        'enter text with your keyboard using the '
                        'specific method requested.')

    no_output_text = ('Even if you see no keyboard output, keep typing '
                      'as if the keyboard is working.')
    
    error_text = ('Don\'t worry if you make a mistake in any '
                  'way, just continue as instructed.')

    unavailibility_text = ('If your keyboard does not support the '
                           'requested input type, just click \'skip\'.')

    def __init__(self, *args, **kwargs):
        super(DeviceInfoScreen, self).__init__(*args, **kwargs)

        self.name = 'deviceinfo'

        if platform == 'android':
            Build = autoclass('android.os.Build')
            self.brand = Build.BRAND
            # self.device = Build.DEVICE
            self.manufacturer = Build.MANUFACTURER
            self.model = Build.MODEL
            # self.product = Build.PRODUCT

    def on_pre_enter(self):
        super(DeviceInfoScreen, self).on_pre_enter()

        App.get_running_app().log('brand: {}'.format(self.brand), prefix='  ')
        # App.get_running_app().log('Device: {}'.format(self.device))
        App.get_running_app().log('manufacturer: {}'.format(self.manufacturer), prefix='  ')
        App.get_running_app().log('model: {}'.format(self.model), prefix='  ')
        # App.get_running_app().log('Product: {}'.format(self.product))

        App.get_running_app().body_text = (
            'Keyboard log for brand {}, manufacturer {}, model {}.'.format(
                self.brand, self.manufacturer, self.model))



class TapInputScreen(OrderedScreen):
    pass

class SwipeInputScreen(OrderedScreen):
    pass

class OtherInputScreen(OrderedScreen):
    pass

class AnyProblemsScreen(OrderedScreen):
    def some_problems(self):
        App.get_running_app().log('problems: yes', prefix='  ')
        self.next()

    def no_problems(self):
        App.get_running_app().log('problems: no', prefix='  ')
        self.next()

class FinalScreen(OrderedScreen):
    file_text = StringProperty()

    def on_pre_enter(self):
        super(FinalScreen, self).on_pre_enter()

        with open(filename, 'r') as fileh:
            self.file_text = fileh.read()


class KeyboardTesterApp(App):
    body_text = StringProperty()

    def build(self):
        Window.bind(on_keyboard=self.key_input)
        self.reset_log()
        return Manager()

    def reset(self):
        self.reset_log()
        if self.root is not None:
            for screen in self.root.children:
                screen.reset()
            self.root.current = 'deviceinfo'

    def reset_log(self):
        if exists(filename):
            unlink(filename)

    def log(self, s, newline=True, prefix=''):
        if newline and not s.endswith('\n'):
            s = s + '\n'
        s = prefix + s
        with open(filename, 'a') as fileh:
            fileh.write(s)

    def send_email(self):
        send_email(self.body_text, abspath(filename))

    def key_input(self, window, key, scancode, codepoint, modifier):
        if key == 27:
            if platform == 'android':
                from jnius import autoclass
                activity = autoclass('org.kivy.android.PythonActivity')
                activity.moveTaskToBack(True)
            return True
        return False


if __name__ == '__main__':
    KeyboardTesterApp().run()
