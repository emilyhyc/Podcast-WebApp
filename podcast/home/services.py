from podcast.adapters.repository import AbstractRepository

def get_number_of_episodes(repo: AbstractRepository):
    return repo.get_number_of_episodes()

def get_number_of_podcasts(repo: AbstractRepository):
    return repo.get_number_of_podcasts()

def get_user(repo: AbstractRepository, username):
    return repo.get_user(username)
