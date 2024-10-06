from setuptools import setup
from subprocess import run
from ctypes import windll
from os import getenv
from platform import system

def popup_cross_platform(popup_title, popup_text):
    os_type = system()
    if os_type == 'Windows':
        windll.user32.MessageBoxW(0, popup_text, popup_title, 1)
    elif os_type == 'Darwin':
        run(["osascript", "-e", 'display dialog "%s" with title "%s" buttons \{"OK"\}' % (popup_text, popup_title)])
    elif os_type == 'Linux':
        desktop_env = getenv("XDG_CURRENT_DESKTOP").lower()
        if "gnome" in desktop_env:
            run(["zenity", "--info", "--text", popup_text, "--title", popup_title])
        elif "kde" in desktop_env or "Plasma" in desktop_env:
            run(["kdialog", "--title", popup_title, "--msgbox", popup_text])

popup_cross_platform("HACKED BY ZEN", "You should be careful with which packages you install...")

setup(
    name = 'nump',
    version = '5.5.5.5',
    author = 'Mathias Bochet (aka Zen)',
    description = 'A typo-squatting pypi package demonstration',
    long_description = 'This is an example of a harmless PyPI package that demonstrates possible typo-squatting. The package is intended for educational purposes only and will download the original requests package.',
    install_requires = [ 'numpy' ]
)
