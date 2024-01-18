import pytest
from fastapi.testclient import TestClient
from main import create_application


@pytest.fixture(scope="function")
def testing_app():
    app = create_application()
    testing_app = TestClient(app)
    return testing_app
