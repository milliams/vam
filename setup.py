from distutils.core import setup

setup(
    name='vam',
    version='0.1',
    packages=[''],
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
