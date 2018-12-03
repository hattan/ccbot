from distutils.core import setup

setup(
    name='ccbot',
    version='0.1dev',
    description='SoCal Code Camp bot',
    url='http://github.com/hattan/ccbot',    
    packages=['ccbot','ccbot/commands','ccbot/services','ccbot/utils'],
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description=open('README.md').read(),
)