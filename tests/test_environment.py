import os

from vam import environment


def test_home():
    assert str(environment.home()) == os.environ['HOME']
