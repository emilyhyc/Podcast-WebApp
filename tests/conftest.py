import pytest

from podcast import create_app
from podcast.adapters import memory_repository
from podcast.adapters.memory_repository import MemoryRepository
from util import get_project_root

TEST_DATA_PATH = get_project_root() / "tests" / "data"

@pytest.fixture
def in_memory_repo():
    repo = MemoryRepository()
    memory_repository.populate(TEST_DATA_PATH, repo)
    return repo

@pytest.fixture
def client():
    my_app = create_app({
        'TESTING': True,  # Set to True during testing.
        'TEST_DATA_PATH': TEST_DATA_PATH,  # Path for loading test data into the repository.
        'WTF_CSRF_ENABLED': False  # test_client will not send a CSRF token, so disable validation.
    })

    return my_app.test_client()

class AuthenticationManager:
    def __init__(self, client):
        self.__client = client

    def login(self, username='xxx', password='Pass123'):
        return self.__client.post(
            'authentication/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self.__client.get('/authentication/logout')


@pytest.fixture
def auth(client):
    return AuthenticationManager(client)


