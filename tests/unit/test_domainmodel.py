import os, csv
from pathlib2 import Path

import pytest
from podcast.domainmodel.model import Author, Podcast, Category, User, PodcastSubscription, Review, Playlist, Episode
from podcast.adapters.datareader.csvdatareader import CSVDataReader
from datetime import datetime
from util import get_project_root



def test_author_initialization():
    author1 = Author(1, "Brian Denny")
    assert repr(author1) == "<Author 1: Brian Denny>"
    assert author1.name == "Brian Denny"

    with pytest.raises(ValueError):
        author2 = Author(2, "")

    with pytest.raises(ValueError):
        author3 = Author(3, 123)

    author4 = Author(4, " USA Radio   ")
    assert author4.name == "USA Radio"

    author4.name = "Jackson Mumey"
    assert repr(author4) == "<Author 4: Jackson Mumey>"


def test_author_eq():
    author1 = Author(1, "Author A")
    author2 = Author(1, "Author A")
    author3 = Author(3, "Author B")
    assert author1 == author2
    assert author1 != author3
    assert author3 != author2
    assert author3 == author3


def test_author_lt():
    author1 = Author(1, "Jackson Mumey")
    author2 = Author(2, "USA Radio")
    author3 = Author(3, "Jesmond Parish Church")
    assert author1 < author2
    assert author2 > author3
    assert author1 < author3
    author_list = [author3, author2, author1]
    assert sorted(author_list) == [author1, author3, author2]


def test_author_hash():
    authors = set()
    author1 = Author(1, "Doctor Squee")
    author2 = Author(2, "USA Radio")
    author3 = Author(3, "Jesmond Parish Church")
    authors.add(author1)
    authors.add(author2)
    authors.add(author3)
    assert len(authors) == 3
    assert repr(
        sorted(authors)) == "[<Author 1: Doctor Squee>, <Author 3: Jesmond Parish Church>, <Author 2: USA Radio>]"
    authors.discard(author1)
    assert repr(sorted(authors)) == "[<Author 3: Jesmond Parish Church>, <Author 2: USA Radio>]"


def test_author_name_setter():
    author = Author(1, "Doctor Squee")
    author.name = "   USA Radio  "
    assert repr(author) == "<Author 1: USA Radio>"

    with pytest.raises(ValueError):
        author.name = ""

    with pytest.raises(ValueError):
        author.name = 123


def test_category_initialization():
    category1 = Category(1, "Comedy")
    assert repr(category1) == "<Category 1: Comedy>"
    category2 = Category(2, " Christianity ")
    assert repr(category2) == "<Category 2: Christianity>"

    with pytest.raises(ValueError):
        category3 = Category(3, 300)

    category5 = Category(5, " Religion & Spirituality  ")
    assert category5.name == "Religion & Spirituality"

    with pytest.raises(ValueError):
        category1 = Category(4, "")


def test_category_name_setter():
    category1 = Category(6, "Category A")
    assert category1.name == "Category A"

    with pytest.raises(ValueError):
        category1 = Category(7, "")

    with pytest.raises(ValueError):
        category1 = Category(8, 123)


def test_category_eq():
    category1 = Category(9, "Action")
    category2 = Category(10, "Indie")
    category3 = Category(11, "Sports")
    assert category1 == category1
    assert category1 != category2
    assert category2 != category3
    assert category1 != "9: Adventure"
    assert category2 != 105


def test_category_hash():
    category1 = Category(9, "Action")
    category2 = Category(10, "Indie")
    category3 = Category(11, "Sports")
    category_set = set()
    category_set.add(category1)
    category_set.add(category2)
    category_set.add(category3)
    assert sorted(category_set) == [category1, category2, category3]
    category_set.discard(category2)
    category_set.discard(category1)
    assert sorted(category_set) == [category3]


def test_category_lt():
    category1 = Category(9, "Action")
    category2 = Category(10, "Indie")
    category3 = Category(11, "Sports")
    assert category1 < category2
    assert category2 < category3
    assert category3 > category1
    category_list = [category3, category2, category1]
    assert sorted(category_list) == [category1, category2, category3]


# Fixtures to reuse in multiple tests
@pytest.fixture
def my_author():
    return Author(1, "Joe Toste")


@pytest.fixture
def my_podcast(my_author):
    return Podcast(100, my_author, "Joe Toste Podcast - Sales Training Expert")


@pytest.fixture
def my_user():
    return User("Shyamli", "pw12345")


@pytest.fixture
def my_subscription(my_user, my_podcast):
    return PodcastSubscription(1, my_user, my_podcast)


def test_podcast_initialization():
    author1 = Author(1, "Doctor Squee")
    podcast1 = Podcast(2, author1, "My First Podcast")
    assert podcast1.id == 2
    assert podcast1.author == author1
    assert podcast1.title == "My First Podcast"
    assert podcast1.description == ""
    assert podcast1.website == ""

    assert repr(podcast1) == "<Podcast 2: 'My First Podcast' by Doctor Squee>"

    with pytest.raises(ValueError):
        podcast3 = Podcast(-123, "Todd Clayton")

    podcast4 = Podcast(123, " ")
    assert podcast4.title is 'Untitled'
    assert podcast4.image is None


def test_podcast_change_title(my_podcast):
    my_podcast.title = "TourMix Podcast"
    assert my_podcast.title == "TourMix Podcast"

    with pytest.raises(ValueError):
        my_podcast.title = ""


def test_podcast_add_category(my_podcast):
    category = Category(12, "TV & Film")
    my_podcast.add_category(category)
    assert category in my_podcast.categories
    assert len(my_podcast.categories) == 1

    my_podcast.add_category(category)
    my_podcast.add_category(category)
    assert len(my_podcast.categories) == 1


def test_podcast_remove_category(my_podcast):
    category1 = Category(13, "Technology")
    my_podcast.add_category(category1)
    my_podcast.remove_category(category1)
    assert len(my_podcast.categories) == 0

    category2 = Category(14, "Science")
    my_podcast.add_category(category1)
    my_podcast.remove_category(category2)
    assert len(my_podcast.categories) == 1


def test_podcast_title_setter(my_podcast):
    my_podcast.title = "Dark Throne"
    assert my_podcast.title == 'Dark Throne'

    with pytest.raises(ValueError):
        my_podcast.title = " "

    with pytest.raises(ValueError):
        my_podcast.title = ""


def test_podcast_eq():
    author1 = Author(1, "Author A")
    author2 = Author(2, "Author C")
    author3 = Author(3, "Author B")
    podcast1 = Podcast(100, author1, "Joe Toste Podcast - Sales Training Expert")
    podcast2 = Podcast(200, author2, "Voices in AI")
    podcast3 = Podcast(101, author3, "Law Talk")
    assert podcast1 == podcast1
    assert podcast1 != podcast2
    assert podcast2 != podcast3


def test_podcast_hash():
    author1 = Author(1, "Author A")
    author2 = Author(2, "Author C")
    author3 = Author(3, "Author B")
    podcast1 = Podcast(100, author1, "Joe Toste Podcast - Sales Training Expert")
    podcast2 = Podcast(100, author2, "Voices in AI")
    podcast3 = Podcast(101, author3, "Law Talk")
    podcast_set = {podcast1, podcast2, podcast3}
    assert len(podcast_set) == 2  # Since podcast1 and podcast2 have the same ID


def test_podcast_lt():
    author1 = Author(1, "Author A")
    author2 = Author(2, "Author C")
    author3 = Author(3, "Author B")
    podcast1 = Podcast(100, author1, "Joe Toste Podcast - Sales Training Expert")
    podcast2 = Podcast(200, author2, "Voices in AI")
    podcast3 = Podcast(101, author3, "Law Talk")
    assert podcast1 < podcast2
    assert podcast2 > podcast3
    assert podcast3 > podcast1


def test_user_initialization():
    user1 = User("Shyamli", "pw12345")
    user2 = User("asma", "pw67890")
    user3 = User("JeNNy  ", "pw87465")
    assert repr(user1) == "<User shyamli>"
    assert repr(user2) == "<User asma>"
    assert repr(user3) == "<User jenny>"
    assert user2.password == "pw67890"
    with pytest.raises(ValueError):
        user4 = User("xyz  ", "")
    with pytest.raises(ValueError):
        user4 = User("    ", "qwerty12345")


def test_user_eq():
    user1 = User("Shyamli", "pw12345")
    user2 = User("asma", "pw67890")
    user3 = User("JeNNy  ", "pw87465")
    user4 = User("Shyamli", "pw12345")
    assert user1 == user4
    assert user1 != user2
    assert user2 != user3


def test_user_hash():
    user1 = User("   Shyamli", "pw12345")
    user2 = User("asma", "pw67890")
    user3 = User("JeNNy  ", "pw87465")
    user_set = set()
    user_set.add(user1)
    user_set.add(user2)
    user_set.add(user3)
    assert sorted(user_set) == [user2, user3, user1]
    user_set.discard(user1)
    user_set.discard(user2)
    assert list(user_set) == [user3]


def test_user_lt():
    user1 = User("Shyamli", "pw12345")
    user2 = User("asma", "pw67890")
    user3 = User("JeNNy  ", "pw87465")
    assert user2 < user3
    assert user1 > user2
    assert user3 < user1
    user_list = [user3, user2, user1]
    assert sorted(user_list) == [user2, user3, user1]


def test_user_add_remove_favourite_podcasts(my_user, my_subscription):
    my_user.add_subscription(my_subscription)
    assert repr(my_user.subscription_list) == "[<PodcastSubscription 1: Owned by shyamli>]"
    my_user.add_subscription(my_subscription)
    assert len(my_user.subscription_list) == 1
    my_user.remove_subscription(my_subscription)
    assert repr(my_user.subscription_list) == "[]"


def test_podcast_subscription_initialization(my_subscription):
    assert my_subscription.id == 1
    assert repr(my_subscription.owner) == "<User shyamli>"
    assert repr(my_subscription.podcast) == "<Podcast 100: 'Joe Toste Podcast - Sales Training Expert' by Joe Toste>"

    assert repr(my_subscription) == "<PodcastSubscription 1: Owned by shyamli>"


def test_podcast_subscription_set_owner(my_subscription):
    new_user = User("asma", "pw67890")
    my_subscription.owner = new_user
    assert my_subscription.owner == new_user

    with pytest.raises(TypeError):
        my_subscription.owner = "not a user"


def test_podcast_subscription_set_podcast(my_subscription):
    author2 = Author(2, "Author C")
    new_podcast = Podcast(200, author2, "Voices in AI")
    my_subscription.podcast = new_podcast
    assert my_subscription.podcast == new_podcast

    with pytest.raises(TypeError):
        my_subscription.podcast = "not a podcast"


def test_podcast_subscription_equality(my_user, my_podcast):
    sub1 = PodcastSubscription(1, my_user, my_podcast)
    sub2 = PodcastSubscription(1, my_user, my_podcast)
    sub3 = PodcastSubscription(2, my_user, my_podcast)
    assert sub1 == sub2
    assert sub1 != sub3


def test_podcast_subscription_hash(my_user, my_podcast):
    sub1 = PodcastSubscription(1, my_user, my_podcast)
    sub2 = PodcastSubscription(1, my_user, my_podcast)
    sub_set = {sub1, sub2}  # Should only contain one element since hash should be the same
    assert len(sub_set) == 1


# TODO : Write Unit Tests for CSVDataReader, Episode, Review, Playlist classes
def test_episode_initialization():
    ep1 = Episode(1,32,
                  "test_title",
                  "http://www.test_link", 329,
                  "test_description",
                  "2017-12-01 00:09:47+00")
    assert ep1.episode_id == 1
    assert ep1.podcast_id == 32
    assert ep1.title == "test_title"
    assert ep1.audio_link == "http://www.test_link"
    assert ep1.audio_length == 329
    assert ep1.description == "test_description"
    assert ep1.pub_date == '2017-12-01 00:09:47+00'

    with pytest.raises(ValueError):
        ep2 = Episode(-2, 33,
                      "test_title",
                      "http://www.test_link", 329,
                      "test_description",
                      "2017-12-01 00:09:47+00")

    with pytest.raises(ValueError):
        ep3 = Episode(3, -34,
                      "test_title",
                      "http://www.test_link", 329,
                      "test_description",
                      "2017-12-01 00:09:47+00")

    with pytest.raises(ValueError):
        ep3 = Episode(4, 34,
                      "test_title",
                      "http://www.test_link", -329,
                      "test_description",
                      "2017-12-01 00:09:47+00")


def test_episode_parent_podcast_setter():
    ep1 = Episode(1, 32,
                  "test_title",
                  "http://www.test_link", 329,
                  "test_description",
                  "2017-12-01 00:09:47+00")
    ep1.podcast_id = 2
    assert ep1.podcast_id == 2

    with pytest.raises(ValueError):
        ep1.podcast_id = -2


def test_episode_title_setter():
    ep1 = Episode(1, 32,
                  "test_title",
                  "http://www.test_link", 329,
                  "test_description",
                  "2017-12-01 00:09:47+00")
    ep1.title = "Test new title"
    assert ep1.title == "Test new title"

    with pytest.raises(ValueError):
        ep1.title = ""


def test_episode_audio_length_setter():
    ep1 = Episode(1, 32,
                  "test_title",
                  "http://www.test_link", 329,
                  "test_description",
                  "2017-12-01 00:09:47+00")
    ep1.audio_length = 400
    assert ep1.audio_length == 400

    with pytest.raises(ValueError):
        ep1.audio_length = -400


def test_episode_pub_date_setter():
    ep1 = Episode(1, 32,
                  "test_title",
                  "http://www.test_link", 329,
                  "test_description",
                  "2017-12-01 00:09:47+00")
    ep1.pub_date = "2004-09-28 00:09:47+00"
    assert isinstance(ep1.pub_date, datetime)
    assert ep1.pub_date == datetime.strptime("2004-09-28 00:09:47+0000", "%Y-%m-%d %H:%M:%S%z")

    with pytest.raises(ValueError):
        ep1.pub_date = ""


def test_episode_lt():
    ep1 = Episode(1, 32,
                  "test_title",
                  "http://www.test_link", 329,
                  "test_description",
                  "2017-12-01 00:09:47+00")
    ep2 = Episode(2, 32,
                  "test_title",
                  "http://www.test_link", 400,
                  "test_description",
                  "2017-12-01 00:09:47+00")
    ep3 = Episode(3, 32,
                  "test_title",
                  "http://www.test_link", 329,
                  "test_description",
                  "2017-12-01 00:09:47+00")

    assert ep1 < ep2
    assert ep2 < ep3
    assert ep1 < ep3
    assert ep3 > ep2
    episode_list = [ep2, ep3, ep1]
    assert sorted(episode_list) == [ep1, ep2, ep3]


def test_episode_eq():
    ep1 = Episode(1, 32,
                  "test_title",
                  "http://www.test_link", 329,
                  "test_description",
                  "2017-12-01 00:09:47+00")
    ep2 = Episode(1, 32,
                  "test_title",
                  "http://www.test_link", 400,
                  "test_description",
                  "2017-12-01 00:09:47+00")
    ep3 = Episode(3, 32,
                  "test_title",
                  "http://www.test_link", 329,
                  "test_description",
                  "2017-12-01 00:09:47+00")

    assert ep1 == ep2
    assert ep1 != ep3
    assert ep2 != ep3

def test_episode_hash():
    ep1 = Episode(1, 32,
                  "test_title",
                  "http://www.test_link", 329,
                  "test_description",
                  "2017-12-01 00:09:47+00")
    ep2 = Episode(1, 32,
                  "test_title",
                  "http://www.test_link", 400,
                  "test_description",
                  "2017-12-01 00:09:47+00")
    ep3 = Episode(3, 32,
                  "test_title",
                  "http://www.test_link", 329,
                  "test_description",
                  "2017-12-01 00:09:47+00")

    episode_subset1 = {ep1, ep2}
    episode_subset2 = {ep1, ep3}
    assert len(episode_subset1) == 1
    assert len(episode_subset2) == 2


def test_episode_repr():
    ep1 = Episode(1, 32,
                  "test_title",
                  "http://www.test_link", 329,
                  "test_description",
                  "2017-12-01 00:09:47+00")

    assert repr(ep1) == (f"<Episode id: 1" +
                         f"Title: test_title, belongs to podcast: 32>")


def test_review_initialization():
    author1 = Author(1, "Author A")
    podcast1 = Podcast(200, author1, "Voices in AI")
    user1 = User("Apook231", "Lmor867@aucklanduni.ac.nz")
    review1 = Review(1, podcast1, user1, 5, "Great Podcast! I love Garfield!")

    assert review1.review_id == 1
    assert review1.podcast == podcast1
    assert review1.user == user1
    assert review1.rating == 5
    assert review1.comment == "Great Podcast! I love Garfield!"

    #check if rating is not between 1 and 5
    with pytest.raises(ValueError):
        Review(1, podcast1, user1, 0, "Yay!")

    #invalid type user
    with pytest.raises(TypeError):
        Review(1, podcast1, "user1", 5, "Yay!")

    #invalid type podcast
    with pytest.raises(TypeError):
        Review(1, "podcast1", user1, 5, "Yay!")


def test_review_podcast_setter():
    author1 = Author(1, "Author A")
    author2 = Author(2, "Author B")
    podcast1 = Podcast(200, author1, "Voices in AI")
    podcast2 = Podcast(300, author2, "Songs in Class")
    user1 = User("Apook231", "Lmor867@aucklanduni.ac.nz")
    review1 = Review(1, podcast1, user1, 5, "Great Podcast! I love Garfield!")
    review1.podcast = podcast2

    #change podcast setter
    assert review1.podcast == podcast2

    with pytest.raises(TypeError):
        review1.podcast = ""

    with pytest.raises(TypeError):
        review1.podcast = 123


def test_review_rating_setter():
    author1 = Author(1, "Author A")
    podcast1 = Podcast(200, author1, "Voices in AI")
    user1 = User("Apook231", "Lmor867@aucklanduni.ac.nz")
    review1 = Review(1, podcast1, user1, 5, "")
    # change rating from 5 to 1
    review1.rating = 1
    assert review1.rating == 1


def test_review_comment_setter():
    author1 = Author(1, "Author A")
    podcast1 = Podcast(200, author1, "Voices in AI")
    user1 = User("Apook231", "Lmor867@aucklanduni.ac.nz")
    review1 = Review(1, podcast1, user1, 5, "")
    # empty comment --> filled comment
    review1.comment = "new comment"
    assert review1.comment == "new comment"

    # filled comment --> empty comment --> ""
    review1.comment = "                 "
    assert review1.comment == ""


def test_review_lt():
    author1 = Author(1, "Author A")
    podcast1 = Podcast(200, author1, "Voices in AI")
    user1 = User("Apook231", "Lmor867@aucklanduni.ac.nz")

    review1 = Review(1, podcast1, user1, 1, "a")
    review2 = Review(6, podcast1, user1, 3, "b")
    review3 = Review(5, podcast1, user1, 5, "c")
    # based on rating
    assert review1 < review2
    assert review3 > review2
    assert review1 < review3
    assert review1 < review3
    review_list = [review3, review1, review2]
    assert sorted(review_list) == [review1, review2, review3]


def test_review_eq():
    # they are equal if they have the same review ID
    author1 = Author(1, "Author A")
    podcast1 = Podcast(200, author1, "Voices in AI")
    user1 = User("Apook231", "Lmor867@aucklanduni.ac.nz")

    review1 = Review(1, podcast1, user1, 5, "")
    review2 = Review(6, podcast1, user1, 5, "")
    review3 = Review(1, podcast1, user1, 5, "")

    assert review1 == review3  # id 1 and 1
    assert review1 != review2  # id 1 and 6
    assert review2 != review3  # id 6 and 1


def test_review_hash():
    author1 = Author(1, "Author A")
    podcast1 = Podcast(200, author1, "Voices in AI")
    user1 = User("Apook231", "Lmor867@aucklanduni.ac.nz")

    review1 = Review(1, podcast1, user1, 5, "")
    review2 = Review(1, podcast1, user1, 2, "dasdasd")
    sub_set = {review1, review2}  # Should only contain one element since hash (review id of 1) should be the same
    assert len(sub_set) == 1


def test_review_repr():
    author1 = Author(1, "Author A")
    podcast1 = Podcast(200, author1, "Voices in AI")
    user1 = User("Apook231", "Lmor867@aucklanduni.ac.nz")
    # usernames are converted to lowercase in User class, however, I capatilzed the user in repr of review
    review1 = Review(1, podcast1, user1, 5, "awesome podcast! :D")
    assert repr(review1) == ("<Review id: 1. Apook231 rated Voices in AI 5/5 stars. Comment: 'awesome podcast! :D'>")

Root_directory = get_project_root() / "podcast" / 'adapters' /'data'

dir_name = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.'))
podcast_filename = os.path.join(Root_directory / "podcasts.csv")
episode_filename = os.path.join(Root_directory / "episodes.csv")


csv_reader = CSVDataReader(podcast_filename, episode_filename)

csv_reader.podcasts_csv()
csv_reader.episodes_csv()

authors = csv_reader.authors
podcasts = csv_reader.podcast_list
categories = csv_reader.categories
episodes = csv_reader.episode_list

# CSV reader unit testing
def test_podcast_CSV_title():
    # testing podcast titles
    assert repr(podcasts[0].title) == "'D-Hour Radio Network'"
    assert repr(podcasts[1].title) == "'Brian Denny Radio'"
    assert repr(podcasts[2].title) == "'Onde Road - Radio Popolare'"

def test_podcast_CSV_author():
    authors = list(csv_reader._authors)
    assert repr(authors[0]) == "<Author 1: D Hour Radio Network>"
    assert repr(authors[1]) == "<Author 2: Brian Denny>"
    assert repr(authors[2]) == "<Author 3: Radio Popolare>"

def test_podcast_CSV_category():
    category = list(csv_reader._categories)
    assert repr(category[0]) == "<Category 1: Society & Culture>"
    assert repr(category[1]) == "<Category 2: Personal Journals>"
    assert repr(category[2]) == "<Category 3: Professional>"


def test_episode_CSV():
    episodes = csv_reader._episode_list
    assert len(episodes) > 0
    assert episodes[3].description == "1 CORINTHIANS 16:17-16:24"
    for episode in episodes:
        assert isinstance(episode.episode_id, int)
        assert episode.episode_id > 0
        assert isinstance(episode.title, str)
        assert episode.title.strip() != ""
        assert isinstance(episode.pub_date, datetime)
        assert isinstance(episode.podcast_id, int)
        assert episode.podcast_id > 0


def test_create_CSV_author():
    new_csv_reader = CSVDataReader(podcast_filename, episode_filename)
    A1 = new_csv_reader.create_author("A1")
    A2 = new_csv_reader.create_author("A2")
    A3 = new_csv_reader.create_author("A1")

    assert len(new_csv_reader._authors) == 2 # (SETS HAVE UNIQUE CONTENTS)
    assert A1.name == "A1"
    assert A2.name == "A2"
    assert A1 == A3

def test_create_CSV_category():
    new_csv_reader = CSVDataReader(podcast_filename, episode_filename)
    C1 = new_csv_reader.create_category("C1")
    C2 = new_csv_reader.create_category("C2")
    C3 = new_csv_reader.create_category("C1")

    assert len(new_csv_reader._categories) == 2 # (SETS HAVE UNIQUE CONTENTS)
    assert C1.name == "C1"
    assert C2.name == "C2"
    assert C1 == C3


def test_playlist_initialization():
    playlist_owner = User("test_dummy", "passwordtest")
    playlist1 = Playlist(1, playlist_owner, "playlist1")

    assert playlist1.playlist_id == 1
    assert playlist1.owner == playlist_owner
    assert playlist1.playlist_name == "playlist1"

    # invalid playlist_id type
    with pytest.raises(ValueError):
        Playlist("1", playlist_owner, "playlist1")

    # invalid owner_test type
    with pytest.raises(TypeError):
        Playlist(1, "playlist_owner", "playlist1")

    # invalid playlist_id range
    with pytest.raises(ValueError):
        Playlist(-1, playlist_owner, "playlist1")

    with pytest.raises(TypeError):
        Playlist(1, 123, "playlist1")

    with pytest.raises(TypeError):
        Playlist(1, playlist_owner, 123)

def test_playlist_playlist_name_setter():
    owner1 = User("usertest", "passwordtest")
    playlist1 = Playlist(1, owner1, "playlist1")

    playlist1.playlist_name = "playlist2"
    assert playlist1.playlist_name == "playlist2"

    with pytest.raises(ValueError):
        playlist1.playlist_name = " "

    with pytest.raises(ValueError):
        playlist1.playlist_name = ""

def test_playlist_eq():
    owner1 = User("usertest", "passwordtest")
    playlist1 = Playlist(1, owner1, "playlist1")
    playlist2 = Playlist(2, owner1, "playlist2" )

    assert playlist1.playlist_id != playlist2.playlist_id

def test_playlist_repr():
    owner1 = User("usertest", "passwordtest")
    playlist1 = Playlist(1, owner1, "playlist1")
    assert repr(playlist1) == "Playlist 1: Owned by usertest"

def test_playlist_hash():
    owner1 = User("usertest", "passwordtest")
    playlist1 = Playlist(1, owner1, "playlist1")
    playlist2 = Playlist(2, owner1, "playlist2")

    playlist_set = {playlist1.playlist_id, playlist2.playlist_id}
    assert len(playlist_set) == 2 #len(playlist_set) should be 2 because the hash of the two Playlist's are different

def test_category_lt():
    Aowner1 = User("usertest", "passwordtest")
    owner2 = User("usertest2", "passwordtest")
    Aowner3 = User("usertest3", "passwordtest")

    playlist1 = Playlist(1, Aowner1, "CbA")
    playlist2 = Playlist(2, owner2, "ABc")
    playlist3 = Playlist(3, Aowner3, "Abc")


    assert playlist1 < playlist3
    assert playlist1 < playlist2
    assert playlist3 > playlist2
    assert playlist2 < playlist3
    playlist_list = [playlist3, playlist1, playlist2]
    assert sorted(playlist_list) == [playlist1, playlist2, playlist3]




