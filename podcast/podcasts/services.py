from podcast.adapters.repository import AbstractRepository
from podcast.domainmodel.model import User


class NonExistentPodcastException(Exception):
    pass
class NonExistentPageException(Exception):
    pass

class NonExistentEpisodeException(Exception):
    pass


def get_podcast(podcast_id: int, repo: AbstractRepository):
    podcast = repo.get_podcast(podcast_id)
    print(f"podcast {podcast}")
    if podcast is None:
        raise NonExistentPodcastException
    return repo.get_podcast(podcast_id)


def get_all_podcasts(repo: AbstractRepository):
    return repo.get_all_podcasts()


def get_episodes_by_podcast_id(podcast_id: int, repo: AbstractRepository):
    episodes = repo.get_episodes_by_podcast(podcast_id)
    return sorted(episodes, key=lambda e: e.pub_date)


def get_episode_by_id(episode_id: int, repo: AbstractRepository):
    episode = repo.get_episode(episode_id)
    if episode is None:
        raise NonExistentEpisodeException
    return episode

def get_pagination(podcast_id, repository, page, episodes_per_page):
    episodes = repository.get_episodes_by_podcast(podcast_id)
    print(episodes)
    num_pages = repository.pagination(episodes, episodes_per_page)
    if page < 1 or page > num_pages:
        raise NonExistentPageException("Page number out of range")
    page_start = (page - 1) * episodes_per_page
    page_end = page_start + episodes_per_page
    return episodes[page_start:page_end], num_pages

def get_average_rating(podcast_id:int, repo: AbstractRepository):
    rating = 0
    list_of_reviews = repo.get_all_reviews_by_podcast(podcast_id)
    if len(list_of_reviews) == 0:
        return "N/A"
    for r in list_of_reviews:
        rating += r.rating
    average_rating = round(float(rating) / len(list_of_reviews), 2)
    return average_rating

def add_user(user: User, repo: AbstractRepository,):
    repo.add_user(user)

