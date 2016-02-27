from distutils.core import setup

from vam import __version__

setup(
    name='vam',
    version=__version__,
    url='https://github.com/milliams/vam',
    license='MIT',
    author='Matt Williams',
    author_email='matt@milliams.com',
    description='Virtualenv Application Manager',
    entry_points={
        'console_scripts': [
            'vam=vam:vam',
        ],
    },
    install_requires=[
        'click'
    ],
)
