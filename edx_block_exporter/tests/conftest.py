import pytest


@pytest.fixture(scope="session", autouse=True)
def init_env():
    from cms.startup import run as init_cms
    init_cms()
