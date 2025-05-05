from os import getenv


def test_debug_false():
    assert getenv("FLASK_DEBUG", 0) == 0


def test_local_false():
    assert getenv("LOCAL_DEPLOY", 0) == 0
