from setuptools import setup, find_packages
from distutils.extension import Extension
from Cython.Distutils import build_ext

from os.path import join, dirname

packages = find_packages()

with open(join(dirname(__file__), 'version.txt'), 'r') as fileh:
    version = fileh.read().strip()

options = {'apk': {'window': None,
                   'requirements': 'sdl2,kivy,python2,pygments,jedi',
                   'android-api': 19,
                   'ndk-dir': '/home/asandy/android/crystax-ndk-10.3.2',
                   'dist-name': 'pyonic_python2',
                   'ndk-version': '10.3.2',
                   'package': 'net.inclem.keyboardtester',
                   'permission': 'INTERNET',
                   'arch': 'armeabi-v7a',
                   # 'icon': 'build_assets/icon_py2-96.png',
                   }}
setup(
    name='Kivy keyboard tester',
    version=version,
    description=('An app to test different types of keyboard input and submit the'
                 'results to the Kivy team.'),
    author='Alexander Taylor',
    author_email='alexanderjohntaylor@gmail.com',
    packages=packages,
    options=options,
    package_data={'keyboardtester': ['*.py', '*.kv'],
                  }
)
