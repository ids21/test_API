from . simple_api_client import APIClient
import pytest

def pytest_addoption(parser):
    parser.addoption(
        "--url",
        action="store",
        default="https://ya.ru",
        help="This is request url"
    )

    parser.addoption(
        "--encoding",
        action="store",
        default="UTF-8",
        help="This is request url"
    )

@pytest.fixture(scope="session")
def api_client(request):
    return APIClient(base_address=request.config.getoption("--url"))