from setuptools import setup

# run the normal setup
setup(
    name = 'nump',
    version = '1.3.3.7',
    author = 'Mathias Bochet (aka Zen)',
    description = 'A typo-squatting pypi package demonstration',
    long_description = 'This is an example of a harmless PyPI package that demonstrates possible typo-squatting. The package is intended for educational purposes only and will download the original requests package.',
    install_requires = [ 'requests' ]
)
