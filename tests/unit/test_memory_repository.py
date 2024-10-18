import pytest
import csv
from pathlib import Path
from datetime import date, datetime
from typing import List
from podcast.adapters.datareader.csvdatareader import CSVDataReader
from podcast.domainmodel.model import Episode, Podcast, Author, Category, Playlist, User
from podcast.adapters.repository import AbstractRepository
from podcast.adapters.memory_repository import MemoryRepository


@pytest.fixture
def in_memory_repo():
    repository = MemoryRepository()
    return repository

def test_can_add_episode(in_memory_repo):
    parent_podcast = Podcast(1001, 1, "test_title", None, "test description", "https://www.test_link", 1, "Unspecified")
    in_memory_repo.add_podcast(parent_podcast)
    episode1 = Episode(5634, 1001, "episode_title", "http://www.audio_link", 100, "description test", "2020-01-01 00:01:11+00")
    in_memory_repo.add_episode(episode1)

    assert in_memory_repo.get_episode(episode1.episode_id) is episode1

def test_can_get_episode(in_memory_repo):
    episode = in_memory_repo.get_episode(1)
    assert episode == Episode(1, 1, "test_title", "https://wwww.audio_link", 100, "description test", "2020-01-01 00:01:11+00")

def test_can_add_podcast(in_memory_repo):
    podcast1 = Podcast(1001, 1, "test_title", None, "test description", "https://www.test_link", 1, "Unspecified")
    in_memory_repo.add_podcast(podcast1)

    assert in_memory_repo.get_podcast(podcast1.id) is podcast1

def test_an_get_podcast(in_memory_repo):
    podcast = in_memory_repo.get_podcast(1)
    assert podcast == Podcast(1, 1, "test_title", None, "test description", "https://www.test_link", 1, "Unspecified")

def test_can_get_number_of_episodes(in_memory_repo):
    number_of_episodes = in_memory_repo.get_number_of_episodes()

    assert number_of_episodes == 5633

def test_can_get_number_of_podcasts(in_memory_repo):
    number_of_podcasts = in_memory_repo.get_number_of_podcasts()
    assert number_of_podcasts == 1000

#def test_can_get_episode_by_id(in_memory_repo):
    #episodes1 = in_memory_repo.get_episode_by_id(1)
    #assert len(episodes) == 3
    #assert episodes[0].title == ("The Mandarian Orange Show Episode 74- Bad Hammer Time, or: "
                                 #"30 Day MoviePass Challenge Part 3")
    #assert episodes[1].title == "Finding yourself in the character by justifying your actions"
    #assert episodes[2].title == "Episode 182 - Lyrically Weak"

def test_repository_does_not_retrieve_a_non_existent_episode(in_memory_repo):
    episode = in_memory_repo.get_episode(5634)
    assert episode is None

#def test_can_get_podcast_by_id(in_memory_repo):
    #podcasts = in_memory_repo.get_podcasts_by_id([1,2,3])
    #assert len(podcasts) == 3

    #assert podcasts[0].title == "D-Hour Radio Network"
    #assert podcasts[1].title == "Brian Denny Radio"
    #assert podcasts[2].title == "Onde Road - Radio Popolare"

def test_repository_does_not_retrieve_a_non_existent_podcast(in_memory_repo):
    podcast = in_memory_repo.get_podcast(1001)
    assert podcast is None

#def test_repository_can_retrieve_episode_by_date(in_memory_repo):
    #episodes = in_memory_repo.get_episode_by_date(date(2017,12, 2))
    #assert len(episodes) == 134

#def test_repository_does_not_retrieve_an_episode_that_does_not_exist_with_given_date(in_memory_repo):
    #episodes = in_memory_repo.get_episode_by_date(date(2017,11,8))
    #assert len(episodes) == 0

#def can_get_next_episode_by_date(in_memory_repo):
    #episode = in_memory_repo.get_episode(1) # Date is: 2017-12-01 00:09:47+00
    #next_episode = in_memory_repo.get_next_episode_by_date(episode) # Date is: 2017-12-14 23:27:35+00

    # Parent podcast of 1 is 14 (and only two episodes exist).

    #assert next_episode == in_memory_repo.get_episode_by_date(date(2017,12,14))

#def test_repository_does_not_retrieve_non_existent_next_episode(in_memory_repo):
    #episode = in_memory_repo.get_episode(293) # Last episode in podcast with id 14
    #next_episode = in_memory_repo.get_next_episode_by_date(episode)

    #assert next_episode is None

#def test_can_get_previous_episode_by_date(in_memory_repo):
    #episode = in_memory_repo.get_episode(293) # Date is: 2017-12-14 23:27:35+00
    #previous_episode = in_memory_repo.get_previous_episode_by_date(episode) # Date is: 2017-12-01 00:09:47+00
    # Parent podcast of 293 is 14 (and only two episodes exist).

    #assert previous_episode == in_memory_repo.get_episode_by_date(date(2017,12,1))

#def test_repository_does_not_retrieve_non_existent_previous_episode(in_memory_repo):
    #episode = in_memory_repo.get_episode(1) # First episode in podcast with id 14
    #previous_episode = in_memory_repo.get_previous_episode_by_date(episode)

    #assert previous_episode is None


def test_can_get_episodes_by_podcast(in_memory_repo):
    episodes = in_memory_repo.get_episodes_by_podcast(3)
    assert len(episodes) == 2
    assert episodes[0].title == "Onde Road di dom 03/12"
    assert episodes[1].title == "Onde Road di dom 31/12"

def test_can_get_all_categories(in_memory_repo):
    categories = in_memory_repo.get_all_categories()
    assert len(categories) == 65
    categories_list = list(categories)

    C1 = categories_list[0]
    C2 = categories_list[1]
    assert C1.name == "Society & Culture"
    assert C2.id == 2
    assert C1.id == 1
    assert C2.name == "Personal Journals"


def test_can_get_category(in_memory_repo):
    category = in_memory_repo.get_category(1)
    category2 = in_memory_repo.get_category(2)
    category44 = in_memory_repo.get_category(44)
    assert category == Category(1, "Society & Culture")
    assert category2 == Category(2, "Personal Journals")
    assert category44 == Category(44, "Natural Sciences")

def test_repository_does_not_retrieve_a_non_existent_category(in_memory_repo):
    category = in_memory_repo.get_category(92773927739)
    assert category is None

def test_can_get_podcasts_by_category(in_memory_repo):
    P1 = in_memory_repo.get_podcast(1) # D-Hour Radio Network - categories Society & Culture | Personal Journals
    P2 = in_memory_repo.get_podcast(2) # Brian Denny Radio - categories Professional | News & Politics | Sports & Recreation | Comedy

    podcasts1 = in_memory_repo.get_podcasts_by_category(1) # list of podcasts in society and culture
    podcasts2 = in_memory_repo.get_podcasts_by_category(2) # list of podcasts in personal journals
    podcasts3 = in_memory_repo.get_podcasts_by_category(3)  # list of podcasts in Professional

    assert len(podcasts1) == 150
    assert len(podcasts2) == 24
    assert len(podcasts3) == 42
    assert P1 in podcasts1 # D-Hour Radio Network is in society and culture
    assert P1 in podcasts2 # D-Hour Radio Network is in personal journals
    assert P2 in podcasts3 # Brian Denny Radio is in professional


def test_repository_does_not_retrieve_podcasts_for_a_non_existent_category(in_memory_repo):
    podcast = in_memory_repo.get_podcasts_by_category(216738920)
    assert len(podcast) == 0


def test_add_review_and_remove_review(in_memory_repo):
    podcast = in_memory_repo.get_podcast(1)
    user_object = User( 'username', 'pass')
    review = in_memory_repo.add_review(podcast, user_object, 5, "")
    assert len(in_memory_repo.get_all_reviews()) == 1
    in_memory_repo.remove_review(review)
    assert len(in_memory_repo.get_all_reviews()) == 0


def test_get_all_reviews(in_memory_repo):
    podcast = in_memory_repo.get_podcast(1)
    user_object = User('username', 'pass')
    review = in_memory_repo.add_review(podcast, user_object, 5, "")
    podcast2 = in_memory_repo.get_podcast(2)
    review2 = in_memory_repo.add_review(podcast2, user_object, 1, "2")

    assert len(in_memory_repo.get_all_reviews()) == 2

    in_memory_repo.remove_review(review)
    assert len(in_memory_repo.get_all_reviews()) == 1
    in_memory_repo.remove_review(review2)
    assert len(in_memory_repo.get_all_reviews()) == 0


def test_get_all_review_by_podcast(in_memory_repo):
    podcast = in_memory_repo.get_podcast(1)
    user_object = User('username', 'pass')
    review = in_memory_repo.add_review(podcast, user_object, 5, "")
    podcast2 = in_memory_repo.get_podcast(2)
    review2 = in_memory_repo.add_review(podcast2, user_object, 1, "2")

    assert len(in_memory_repo.get_all_reviews_by_podcast(1)) != 2
    assert len(in_memory_repo.get_all_reviews_by_podcast(1)) == 1
    assert len(in_memory_repo.get_all_reviews_by_podcast(2)) == 1


    in_memory_repo.remove_review(review)
    assert len(in_memory_repo.get_all_reviews_by_podcast(1)) == 0
    in_memory_repo.remove_review(review2)
    assert len(in_memory_repo.get_all_reviews_by_podcast(2)) == 0

def test_repository_can_check_for_playlist(in_memory_repo):
    user_object = User('name', 'pass')
    in_memory_repo.set_playlist(user_object)
    in_memory_repo.check_for_playlist(user_object)

    assert in_memory_repo.check_for_playlist(user_object) == True

def test_repository_can_set_playlist(in_memory_repo):
    user_object = User('name', 'pass')
    in_memory_repo.__playlist = None
    in_memory_repo.set_playlist(user_object)

    assert in_memory_repo.check_for_playlist(user_object) == True


def test_repository_can_get_playlist(in_memory_repo):
    user_object = User('name', 'pass')
    in_memory_repo.set_playlist(user_object)

    playlist = in_memory_repo.get_playlist(user_object)

    assert playlist.playlist_id == 1
    assert playlist._owner == user_object
    assert playlist._playlist_name == "name's Playlist"


def test_repository_can_add_episode_to_playlist(in_memory_repo):
    user_object = User('name', 'pass')
    in_memory_repo.set_playlist(user_object)

    parent_podcast = Podcast(1001, 1, "test_title", None, "test description", "https://www.test_link", 1, "Unspecified")
    episode1 = Episode(5634, 1001, "episode_title", "http://www.audio_link", 100, "description test","2020-01-01 00:01:11+00")
    in_memory_repo.add_episode_to_playlist(episode1, user_object)

    playlist = in_memory_repo.get_playlist(user_object)

    assert playlist.episodes[0] == episode1
    assert len(playlist.episodes) == 1


def test_can_remove_episode_from_playlist(in_memory_repo):
    user_object = User('name', 'pass')
    in_memory_repo.set_playlist(user_object)
    parent_podcast = Podcast(1001, 1, "test_title", None, "test description", "https://www.test_link", 1, "Unspecified")
    episode1 = Episode(5634, 1001, "episode_title", "http://www.audio_link", 100, "description test","2020-01-01 00:01:11+00")
    in_memory_repo.add_episode_to_playlist(episode1, user_object)

    in_memory_repo.remove_episode_from_playlist(episode1, user_object)
    playlist = in_memory_repo.get_playlist_by_user(user_object)
    assert len(playlist.episodes) == 0


def test_repository_can_add_podcast_to_playlist(in_memory_repo):
    user_object = User('name', 'pass')
    in_memory_repo.set_playlist(user_object)

    parent_podcast = Podcast(1001, 1, "test_title", None, "test description", "https://www.test_link", 1, "Unspecified")
    in_memory_repo.add_podcast(parent_podcast)
    episode1 = Episode(5634, 1001, "episode_title", "http://www.audio_link", 100, "description test","2020-01-01 00:01:11+00")
    episode2 = Episode(5635, 1001, "episode_title2", "http://www.audio_link2", 100, "description test","2020-01-01 00:01:12+00")
    in_memory_repo.add_episode(episode1)
    in_memory_repo.add_episode(episode2)

    in_memory_repo.add_podcast_to_playlist(parent_podcast, user_object)

    playlist = in_memory_repo.get_playlist(user_object)
    assert len(playlist.episodes) == 2
    assert playlist.episodes[0] == episode1

    # Managing all user playlists

def test_repository_can_add_playlist(in_memory_repo):
    user_object = User('name', 'pass')
    in_memory_repo.set_playlist(user_object)
    playlist = in_memory_repo.get_playlist(user_object)

    assert len(in_memory_repo.get_all_playlists()) == 1

def test_can_get_all_playlists(in_memory_repo):
    # User 1 adding to playlists list
    user_object = User('name', 'pass')
    in_memory_repo.set_playlist(user_object)
    playlist = in_memory_repo.get_playlist(user_object)

    # User 2 adding to playlists list
    user_object2 = User('name2', 'pass2')
    in_memory_repo.set_playlist(user_object2)
    playlist2 = in_memory_repo.get_playlist(user_object2)

    in_memory_repo.set_playlist(user_object)

    assert in_memory_repo.get_all_playlists() == [playlist, playlist2]

def test_can_get_playlist_by_user(in_memory_repo):
    user_object = User('name', 'pass')
    in_memory_repo.set_playlist(user_object)
    playlist = in_memory_repo.get_playlist(user_object)

    get_playlist = in_memory_repo.get_playlist_by_user(user_object)
    assert get_playlist == playlist

def test_add_user(in_memory_repo):
    user_object = User( 'name', 'pass')
    in_memory_repo.add_user(user_object)
    assert len(in_memory_repo.get_all_user()) == 1
    in_memory_repo.remove_user(user_object)
    assert len(in_memory_repo.get_all_user()) == 0

def test_get_user(in_memory_repo):
    user_object = User('name', 'pass')
    in_memory_repo.add_user(user_object)
    assert (in_memory_repo.get_user("name")) == "name"
    in_memory_repo.remove_user(user_object)
    assert len(in_memory_repo.get_all_user()) == 0

def test_get_user_obj(in_memory_repo):
    user_object = User('name', 'pass')
    in_memory_repo.add_user(user_object)
    assert (in_memory_repo.get_user_object("name")) == user_object
    in_memory_repo.remove_user(user_object)
    assert len(in_memory_repo.get_all_user()) == 0

def test_remove_user(in_memory_repo):
    user_object = User('name', 'pass')
    in_memory_repo.add_user(user_object)
    assert len(in_memory_repo.get_all_user()) == 1
    in_memory_repo.remove_user(user_object)
    assert len(in_memory_repo.get_all_user()) == 0


def test_get_all_podcasts(in_memory_repo):
    all_podcasts = in_memory_repo.get_all_podcasts()
    assert len(all_podcasts) == 1000

    podcast1 = in_memory_repo.get_podcast(1)
    podcast2 = in_memory_repo.get_podcast(2)
    podcast5 = in_memory_repo.get_podcast(5)
    podcast1000 = in_memory_repo.get_podcast(1000)


    assert all_podcasts[0] == podcast1
    assert all_podcasts[1] == podcast2
    assert all_podcasts[4] == podcast5
    assert all_podcasts[999] == podcast1000



def test_get_all_episodes(in_memory_repo):
    all_episodes = in_memory_repo.get_all_episodes()
    assert len(all_episodes) == 5633

    episode1 = in_memory_repo.get_episode(1)
    episode2 = in_memory_repo.get_episode(2)
    episode7 = in_memory_repo.get_episode(7)
    episode5633 = in_memory_repo.get_episode(5633)

    assert all_episodes[0] == episode1
    assert all_episodes[1] == episode2
    assert all_episodes[6] == episode7
    assert all_episodes[5632] == episode5633

def test_pagination(in_memory_repo):
    podcasts = in_memory_repo.get_all_podcasts()
    assert in_memory_repo.pagination(podcasts,2) == 500
    assert in_memory_repo.pagination(podcasts, 5) == 200
    assert in_memory_repo.pagination([], 2) == 1
    assert in_memory_repo.pagination(podcasts, 9) == 112


def test_add_category(in_memory_repo):
    category = Category(1221, "Category")
    in_memory_repo.add_category(category)
    assert in_memory_repo.get_category(1221).id == 1221
    assert in_memory_repo.get_category(1221).name == "Category"


def add_multiple_categories(self, categories: List[Category]):
    pass

def add_multiple_episodes(self, episode: List[Episode]):
    pass

def add_multiple_podcasts(self, podcasts: List[Podcast]):
    pass

def add_multiple_authors(in_memory_repo):
    pass

def test_search_podcast_by_author(in_memory_repo):
    results = in_memory_repo.search_podcast_by_author("brian")
    assert len(results) == 8
    results = in_memory_repo.search_podcast_by_author("sally")
    assert len(results) == 0
    results = in_memory_repo.search_podcast_by_author("brad")
    assert len(results) == 3

def test_search_podcast_by_category(in_memory_repo):
    results = in_memory_repo.search_podcast_by_category("sport")
    assert len(results) == 100
    results = in_memory_repo.search_podcast_by_category("business")
    assert len(results) == 88



def test_search_podcast_by_title(in_memory_repo):
    results = in_memory_repo.search_podcast_by_title("eye")
    assert len(results) == 3
    results = in_memory_repo.search_podcast_by_title("so")
    assert len(results) == 42

