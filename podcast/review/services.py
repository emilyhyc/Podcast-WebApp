from podcast.adapters.repository import AbstractRepository
from podcast.domainmodel.model import Review, Podcast, User


class NonExistentPodcastException(Exception):
    pass


class NonExistentPageException(Exception):
    pass


def get_all_podcasts(repo: AbstractRepository):
    return repo.get_all_podcasts()


def get_podcast(podcast_id: int, repo: AbstractRepository):
    podcast = repo.get_podcast(podcast_id)
    if podcast is None:
        raise NonExistentPodcastException(f"not found")
    return podcast


def get_all_reviews_by_podcast(podcast_id: int, repo: AbstractRepository):
    list_of_reviews = repo.get_all_reviews_by_podcast(podcast_id)
    return list_of_reviews


def add_user(user: User, repo: AbstractRepository, ):
    repo.add_user(user)


def get_pagination(repository, reviews, page, reviews_per_page):
    num_pages = repository.pagination(reviews, reviews_per_page)
    if page < 1 or page > num_pages:
        raise NonExistentPageException("Page out of range")
    page_start = (page - 1) * reviews_per_page
    page_end = page_start + reviews_per_page
    return reviews[page_start:page_end], num_pages


def add_review(repo: AbstractRepository, podcast: Podcast, username: str, rating: int, comment: str = ""):
    user = repo.get_user_object(username)
    print(user)
    x = repo.add_review(podcast, user, rating, comment)
    return x
