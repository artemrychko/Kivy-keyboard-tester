
# Kivy keyboard tester

This is an Android app for testing Kivy's keyboard. When opened, it
instructs the user to input text in a few different ways, before
emailing the result back to me for analysis.

The app is intended to broaden the range of keyboard debug information
available, as we know there are some bugs in Kivy's key handling on
some Android devices, but cannot reproduce them on devices we have
available.

Kivy keyboard tester is itself written in Kivy, and compiled for
Android using a Kivy branch that logs text input events to a file.
