# conftest.py
import pytest

def pytest_addoption(parser):
    parser.addoption(
        "--run-long", action="store_true", help="Run long tests"
    )

@pytest.hookimpl(tryfirst=True)
def pytest_collection_modifyitems(config, items):
    if config.getoption("--run-long"):
        # If --run-long is specified, don't skip any long tests
        return
    skip_long = pytest.mark.skip(reason="need --run-long option to run")
    for item in items:
        if "long" in item.keywords:
            item.add_marker(skip_long)