from datetime import date, datetime

import pytest
from sqlalchemy.exc import InvalidRequestError

import podcast.adapters.repository as repo
from podcast.adapters.database_repository import SqlAlchemyRepository
from podcast.domainmodel.model import User, Podcast, Episode, Review, Playlist, Category, Author


def test_repository_can_add_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = User('User1', 'Op0')
    repo.add_user(user)

    repo.add_user(User('User2', 'Op0'))

    user1 = repo.get_user('User1')
    user2 = repo.get_user('User2')

    assert user1 == user
    assert isinstance(user1, User)
    assert len(repo.get_all_user()) == 2


def test_repository_can_retrieve_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    repo.add_user(User('fmercury', '8734gfe2058v'))

    user = repo.get_user('fmercury')
    assert user == User('fmercury', '8734gfe2058v')

def test_repository_does_not_retrieve_a_non_existent_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    user = repo.get_user('prince')
    assert user is None

def test_repository_can_remove_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    user = User('User1', 'Op0')
    repo.add_user(user)
    all_users = repo.get_all_user()
    assert len(all_users) == 1
    removed_user = all_users[0]
    repo.remove_user(removed_user)
    all_users = repo.get_all_user()
    assert len(all_users) == 0
def test_repository_cant_remove_user_if_user_list_empty(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    user = User('User1', 'Op0')
    assert len(repo.get_all_user()) == 0
    with pytest.raises(InvalidRequestError):
        repo.remove_user(user)

def test_repository_can_get_user_object(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    user = User('User1', 'Op0')
    repo.add_user(user)
    x = repo.get_user_object('User1')
    assert x == user

def test_repository_can_get_all_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    all_users = repo.get_all_user()
    assert len(all_users) == 0
    user = User('User1', 'Op0')
    repo.add_user(user)
    all_users = repo.get_all_user()
    assert len(all_users) == 1



# Podcast

def test_repository_can_add_podcast(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    test_author = Author(33333, "author")
    podcast = Podcast(10011, test_author, "test_title", None, "test description", "https://www.test_link", 1, "Unspecified")
    repo.add_podcast(podcast)
    all_podcasts = repo.get_all_podcasts()
    assert podcast in all_podcasts


def test_repository_can_get_podcast(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    test_author = Author(33333, "author")
    podcast = Podcast(10011, test_author, "test_title", None, "test description", "https://www.test_link", 1, "Unspecified")
    repo.add_podcast(podcast)
    podcast = repo.get_podcast(10011)
    assert podcast.title == "test_title"

def test_repository_can_get_all_podcasts(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    podcasts = repo.get_all_podcasts()
    assert len(podcasts) == 1000


def test_repository_can_add_episode(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    episode = Episode(10100101, 1011, "test_episode", "audio_link", 56, "description", "pub_date")
    repo.add_episode(episode)
    assert episode in repo.get_all_episodes()

def test_repository_can_get_episode(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    episode = Episode(10100101, 1011, "test_episode", "audio_link", 56, "description", "pub_date")
    repo.add_episode(episode)
    assert episode.title == "test_episode"
    assert episode.audio_length == 56

def test_repository_can_get_all_episodes(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    episodes = repo.get_all_episodes()
    assert len(episodes) == 5633

def test_repository_can_get_number_of_episodes(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    no_episodes = repo.get_number_of_episodes()
    assert (no_episodes) == 5633


def test_repository_can_get_number_of_podcasts(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    no_podcasts = repo.get_number_of_podcasts()
    assert (no_podcasts) == 1000

def test_repository_can_get_pagination(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    podcasts = repo.get_all_podcasts()
    assert repo.pagination(podcasts,2) == 500
    assert repo.pagination(podcasts, 5) == 200
    assert repo.pagination([], 2) == 1
    assert repo.pagination(podcasts, 9) == 112

def test_repository_can_get_episodes_by_podcast(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    episodes = repo.get_episodes_by_podcast(3)
    assert len(episodes) == 2
    assert episodes[0].title == "Onde Road di dom 03/12"
    assert episodes[1].title == "Onde Road di dom 31/12"

def test_repository_can_get_all_categories(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    categories = repo.get_all_categories()
    assert len(categories) == 65
    categories_list = list(categories)

    C1 = categories_list[0]
    C2 = categories_list[1]
    assert C1.name == "Society & Culture"
    assert C2.id == 2
    assert C1.id == 1
    assert C2.name == "Personal Journals"

def test_can_get_category(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    category = repo.get_category(1)
    category2 = repo.get_category(2)
    category44 = repo.get_category(44)
    assert category == Category(1, "Society & Culture")
    assert category2 == Category(2, "Personal Journals")
    assert category44 == Category(44, "Natural Sciences")

def test_repository_does_not_retrieve_a_non_existent_category(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    category = repo.get_category(92773927739)
    assert category is None

def test_can_get_podcasts_by_category(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    P1 = repo.get_podcast(1) # D-Hour Radio Network - categories Society & Culture | Personal Journals
    P2 = repo.get_podcast(2) # Brian Denny Radio - categories Professional | News & Politics | Sports & Recreation | Comedy

    podcasts1 = repo.get_podcasts_by_category(1) # list of podcasts in society and culture
    podcasts2 = repo.get_podcasts_by_category(2) # list of podcasts in personal journals
    podcasts3 = repo.get_podcasts_by_category(3)  # list of podcasts in Professional

    assert len(podcasts1) == 150
    assert len(podcasts2) == 24
    assert len(podcasts3) == 42
    assert P1 in podcasts1 # D-Hour Radio Network is in society and culture
    assert P1 in podcasts2 # D-Hour Radio Network is in personal journals
    assert P2 in podcasts3 # Brian Denny Radio is in professional


def test_repository_does_not_retrieve_podcasts_for_a_non_existent_category(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    podcasts = repo.get_podcasts_by_category(216738920)
    assert len(podcasts) == 0

def test_repository_can_add_category(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    category = Category(1221, "Category")
    repo.add_category(category)
    assert repo.get_category(1221).id == 1221
    assert repo.get_category(1221).name == "Category"


def test_repository_can_add_AND_REMOVE_reviews(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    podcast = repo.get_podcast(1)
    user_object = User('username', 'pass')
    review = repo.add_review(podcast, user_object, 5, "") #add review
    assert len(repo.get_all_reviews()) == 1
    repo.remove_review(review) #remove review
    assert len(repo.get_all_reviews()) == 0

def test_repository_can_get_all_reviews(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    podcast = repo.get_podcast(1)
    user_object = User('username', 'pass')
    review = repo.add_review(podcast, user_object, 5, "")
    podcast2 = repo.get_podcast(2)
    review2 = repo.add_review(podcast2, user_object, 1, "2")

    assert len(repo.get_all_reviews()) == 2

    repo.remove_review(review)
    assert len(repo.get_all_reviews()) == 1
    repo.remove_review(review2)
    assert len(repo.get_all_reviews()) == 0

def test_repository_can_get_all_reviews_by_podcast(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    podcast = repo.get_podcast(1)
    user_object = User('username', 'pass')
    review = repo.add_review(podcast, user_object, 5, "")
    podcast2 = repo.get_podcast(2)
    review2 = repo.add_review(podcast2, user_object, 1, "2")

    assert len(repo.get_all_reviews_by_podcast(1)) != 2
    assert len(repo.get_all_reviews_by_podcast(1)) == 1
    assert len(repo.get_all_reviews_by_podcast(2)) == 1

    repo.remove_review(review)
    assert len(repo.get_all_reviews_by_podcast(1)) == 0
    repo.remove_review(review2)
    assert len(repo.get_all_reviews_by_podcast(2)) == 0



# playlist section
def test_repository_can_check_for_playlist(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    user = User("User1", "password")
    repo.add_user(user)
    user_object = repo.get_user_object("User1")

    repo.set_playlist(user_object)
    playlist = repo.get_playlist_by_user(user_object)
    repo.add_playlist(playlist)
    assert repo.check_for_playlist(user_object) is True

def test_repository_can_set_playlist(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    user = User("User1", "password")
    repo.add_user(user)
    user_object = repo.get_user_object("User1")

    assert repo.get_playlist_by_user(user_object) is None

    repo.set_playlist(user_object)
    assert repo.get_playlist_by_user(user_object) is not None

def test_repository_can_get_playlist(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    user = User("User1", "password")
    repo.add_user(user)
    user_object = repo.get_user_object("User1")

    assert repo.get_playlist(user_object) is None

    repo.set_playlist(user_object)
    assert repo.get_playlist(user_object) is not None

def test_repository_can_add_episode_to_playlist(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    user = User("User1", "password")
    repo.add_user(user)
    user_object = repo.get_user_object("User1")
    repo.set_playlist(user_object)
    playlist = repo.get_playlist_by_user(user_object)
    episode = repo.get_episode(1)

    assert len(playlist.episodes) == 0
    repo.add_episode_to_playlist(episode, user_object)
    assert len(playlist.episodes) == 1


def test_repository_can_remove_episode_from_playlist(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    user = User("User1", "password")
    repo.add_user(user)
    user_object = repo.get_user_object("User1")
    repo.set_playlist(user_object)
    playlist = repo.get_playlist_by_user(user_object)

    episode = repo.get_episode(1)
    episode2 = repo.get_episode(2)
    assert len(playlist.episodes) == 0
    repo.add_episode_to_playlist(episode, user_object)
    assert len(playlist.episodes) == 1
    repo.add_episode_to_playlist(episode2, user_object)
    assert len(playlist.episodes) == 2

    repo.remove_episode_from_playlist(episode2, user_object)
    assert playlist.episodes[0] == episode
    assert len(playlist.episodes) == 1

def test_repository_can_add_podcast_to_playlist(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    user = User("User1", "password")
    repo.add_user(user)
    user_object = repo.get_user_object("User1")
    repo.set_playlist(user_object)
    playlist = repo.get_playlist_by_user(user_object)

    podcast = repo.get_podcast(1)
    assert len(playlist.episodes) == 0
    repo.add_podcast_to_playlist(podcast, user_object)
    assert len(playlist.episodes) == 10

def test_repository_can_add_playlist(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    user = User("User1", "password")
    repo.add_user(user)
    user_object = repo.get_user_object("User1")
    new_playlist = Playlist(1000, user_object, "User1's playlist")

    repo.add_playlist(new_playlist)
    assert repo.get_playlist(user_object) == new_playlist

def test_repository_can_get_all_playlists(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    user = User("User1", "password")
    user2 = User("User2", "password")
    user3 = User("User3", "password")
    repo.add_user(user)
    repo.add_user(user2)
    repo.add_user(user3)

    user_object = repo.get_user_object("User1")
    user_object2 = repo.get_user_object("User2")
    user_object3 = repo.get_user_object("User3")

    assert len(repo.get_all_playlists()) == 0

    repo.set_playlist(user_object)
    assert len(repo.get_all_playlists()) == 1
    assert repo.get_all_playlists()[0] == repo.get_playlist_by_user(user_object)

    repo.set_playlist(user_object2)
    assert len(repo.get_all_playlists()) == 2
    assert repo.get_all_playlists()[1] == repo.get_playlist_by_user(user_object2)

    repo.set_playlist(user_object3)
    assert len(repo.get_all_playlists()) == 3
    assert repo.get_all_playlists()[2] == repo.get_playlist_by_user(user_object3)



def test_repository_can_get_playlist_by_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    user = User("User1", "password")
    user2 = User("User2", "password")
    repo.add_user(user)
    repo.add_user(user2)
    user_object = repo.get_user_object("User1")
    user_object2 = repo.get_user_object("User2")

    repo.set_playlist(user_object)
    repo.set_playlist(user_object2)
    other_playlist = repo.get_playlist_by_user(user_object)
    playlist = repo.get_playlist_by_user(user_object2)

    assert len(playlist.episodes) == 0

    episode = repo.get_episode(1)
    episode2 = repo.get_episode(2)
    repo.add_episode_to_playlist(episode, user_object2)
    repo.add_episode_to_playlist(episode2, user_object2)

    assert len(playlist.episodes) == 2
    assert len(other_playlist.episodes) == 0


# region Author data

def test_repository_can_search_podcast_by_title(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    list_podcasts = repo.search_podcast_by_title("yes")
    assert len(list_podcasts) == 1
    assert repo.get_podcast(820) in list_podcasts
    list_podcasts = repo.search_podcast_by_title("fan")
    assert len(list_podcasts) == 6
    assert repo.get_podcast(13) in list_podcasts
    assert repo.get_podcast(582) in list_podcasts


def test_repository_can_search_podcast_by_author(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    list_podcasts = repo.search_podcast_by_author("steve")
    assert len(list_podcasts) == 8
    assert repo.get_podcast(308) in list_podcasts
    assert repo.get_podcast(907) in list_podcasts


def test_repository_can_search_podcast_by_category(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    list_podcasts = repo.search_podcast_by_category("sport")
    assert len(list_podcasts) == 100
    assert repo.get_podcast(578) in list_podcasts
    assert repo.get_podcast(405) in list_podcasts
