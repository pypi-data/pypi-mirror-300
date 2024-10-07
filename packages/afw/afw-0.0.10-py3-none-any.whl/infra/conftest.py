import pytest

def pytest_addoption(parser):
    parser.addoption("--url", action="store", default="http://localhost")
    parser.addoption("--username", action="store", default="admin")
    parser.addoption("--password", action="store", default="admin")

@pytest.fixture
def url(request):
    return request.config.getoption("--url")

@pytest.fixture
def username(request):
    return request.config.getoption("--username")

@pytest.fixture
def password(request):
    return request.config.getoption("--password")