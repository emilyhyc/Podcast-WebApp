from podcast.adapters.repository import AbstractRepository
# from podcast.adapters.database_repository import SqlAlchemyRepository
from podcast.domainmodel.model import User

from werkzeug.security import generate_password_hash, check_password_hash


class NameNotUniqueException(Exception):
    pass

class UnregisteredUserException(Exception):
    pass

class UnauthenticatedUserException(Exception):
    pass


# repo = SqlAlchemyRepository
repo = AbstractRepository

def add_user(username: str, password: str, repo: repo):
    temp_user = repo.get_user(username)
    if temp_user is not None:
        raise NameNotUniqueException

    # password_hash = generate_password_hash(password)

    # user_id = len(repo.get_all_user()) + 1
    user = User(username, password)
    repo.add_user(user)


def get_user(username: str, password:str, repo: repo):
    user = repo.get_user_object(username)

    if user is None:
        raise UnregisteredUserException
    user_dict = {"username": user.username, "password": user.password}
    return user_dict


def auth_user(username: str, password: str, repo: repo):
    authenticated = False
    user_dict = get_user(username, password, repo)

    if user_dict is not None:
        authenticated = check_password_hash(user_dict["password"], password)

    if not authenticated:
        raise UnauthenticatedUserException

