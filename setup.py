from distutils.core import setup
from setuptools import find_packages

from vam import __version__


def readme():
    with open('README.rst') as f:
        return f.read()


setup(
    name='vam',
    version=__version__,
    url='https://github.com/milliams/vam',
    long_description=readme(),
    packages=find_packages(exclude=['doc', 'tests']),
    license='MIT',
    author='Matt Williams',
    author_email='matt@milliams.com',
    description='Virtualenv Application Manager',
    entry_points={
        'console_scripts': [
            'vam=vam.vam:vam',
        ],
    },
    install_requires=[
        'click'
    ],
)
