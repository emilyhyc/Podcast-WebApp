from podcast.adapters.repository import AbstractRepository
from podcast.domainmodel.model import Playlist, User, Episode, Podcast


def get_user_object(repo: AbstractRepository, username: str):
    return repo.get_user_object(username)


def check_for_playlist(repo: AbstractRepository, user: User):
    return repo.check_for_playlist(user)


def set_playlist(repo: AbstractRepository, user: User):
    repo.set_playlist(user)


def get_playlist(repo: AbstractRepository, user: User):
    return repo.get_playlist(user)


def add_episode_to_playlist(repo: AbstractRepository, episode: Episode, user: User):
    if repo.check_for_playlist(user):
        repo.add_episode_to_playlist(episode, user)


def remove_episode_from_playlist(repo: AbstractRepository, episode: Episode, user: User):
    if repo.check_for_playlist(user):
        repo.remove_episode_from_playlist(episode, user)


def add_podcast_to_playlist(repo: AbstractRepository, podcast: Podcast, user: User):
    if repo.check_for_playlist(user):
        repo.add_podcast_to_playlist(podcast, user)


def get_playlist_by_user(repo: AbstractRepository, user: User):
    return repo.get_playlist_by_user(user)


def get_podcast(repo: AbstractRepository, podcast_id):
    return repo.get_podcast(podcast_id)

def get_episode(repo: AbstractRepository, episode_id: int):
    return repo.get_episode(episode_id)


class NonExistentPlaylistException(Exception):
    pass


class NonExistentPageException(Exception):
    pass


def get_pagination(repository, playlist, page, episodes_per_page):
    num_pages = repository.pagination(playlist, episodes_per_page)
    if page < 1 or page > num_pages:
        raise NonExistentPageException("Page out of range")
    page_start = (page - 1) * episodes_per_page
    page_end = page_start + episodes_per_page
    return playlist[page_start:page_end], num_pages