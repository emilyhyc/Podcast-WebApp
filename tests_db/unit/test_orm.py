from logging import raiseExceptions
from unittest import expectedFailure

import pytest
from unicodedata import category

from podcast.domainmodel.model import User, Podcast, Episode, Review, Playlist, Category, Author
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import text

from tests.unit.test_domainmodel import categories


# Adjust the parameters if needed
# INSERT METHODS

def insert_author(empty_session):
    empty_session.execute(text(
        'INSERT INTO authors (author_id, name) VALUES (1, "D Hour Radio Network")'
    ))
    author_id = empty_session.execute(text('SELECT author_id from authors')).fetchone()
    print(author_id[0])
    return author_id[0]


def insert_podcast(empty_session):
    podcast_author = Author(1, "test_author")

    empty_session.execute(text(
        'INSERT INTO podcasts (podcast_id, title, image_url, description, language, website_url, author_id, itunes_id) '
        'VALUES (:podcast_id, "test_post", "http://image", "description", "English", "http://www.website", :author_id, :itunes_id)'),
        {'podcast_id': 1, 'author_id': 1, 'itunes_id': 329}
    )
    podcast_id = empty_session.execute(text('SELECT podcast_id from podcasts')).fetchone()
    return podcast_id[0]

def insert_user(empty_session, values=None):
    new_name = "user"
    new_password = "password"
    if values is not None:
        new_name = values[0]
        new_password = values[1]

    empty_session.execute(text('INSERT INTO users (username, password) VALUES (:username, :password)'),
                          {'username': new_name, 'password': new_password})
    user_id = empty_session.execute(text('SELECT user_id from users where username = :username'),
                                {'username': new_name}).fetchone()
    return user_id[0]


def insert_users(empty_session, values):
    for value in values:
        empty_session.execute(text('INSERT INTO users (username, password) VALUES (:username, :password)'),
                              {'username': value[0], 'password': value[1]})
    rows = list(empty_session.execute(text('SELECT user_id from users')))
    user_ids = tuple(row[0] for row in rows)
    return user_ids


# TODO insert methods
def insert_episode(empty_session):
    episode_id = 1
    podcast_id = 32
    title = "test_title"
    audio_link = "http://www.test_link"
    audio_length = 329
    description= "test_description"
    pub_date = "2017-12-01 00:09:47+00"

    empty_session.execute(text(
        'INSERT INTO episodes (episode_id, podcast_id, title, audio_link, audio_length, description, pub_date) VALUES '
        '(:episode_id, :podcast_id, "test_title", "http://www.test_link", :audio_length, "test_description", "2017-12-01 00:09:47+00")'),
        {'episode_id': episode_id, 'podcast_id': podcast_id, 'audio_length': audio_length}
    )

    row = empty_session.execute(text('SELECT episode_id from episodes')).fetchone()
    return row[0]


def insert_categories(empty_session, categories):
    for category in categories:
        empty_session.execute(text(
            'INSERT INTO categories (category_name) VALUES (:category_name)'),{'category_name': category})
    empty_session.commit()


def insert_podcast_categories_associations(empty_session, podcast_id , categories_ids): # Change to more appropriate parameter name if needed
    stmt = text('INSERT INTO podcast_categories (podcast_id, category_id) VALUES (:podcast_id, :category_id)')

    for category_id in categories_ids:
        empty_session.execute(stmt, {'podcast_id': podcast_id, 'category_id': category_id})


def insert_review(empty_session, values=None):
    new_comment = "yes"
    new_rating = 5
    new_user_id = 1
    new_podcast_id = 1

    if values is not None:
        new_comment = values[0]
        new_rating = values[1]
        new_user_id = values[2]
        new_podcast_id = values[3]

    empty_session.execute(
        text(
            'INSERT INTO review (comment, rating, user_id, podcast_id) VALUES (:comment, :rating, :user_id, :podcast_id)'),
        {'comment': new_comment, 'rating': new_rating, 'user_id': new_user_id, 'podcast_id': new_podcast_id}
    )
    row = empty_session.execute(
        text('SELECT review_id FROM review WHERE comment = :comment'),
        {'comment': new_comment}).fetchone()
    return row[0]


def insert_reviews(empty_session, values):
    for value in values:
        print(value)
        comment, rating, user_id, podcast_id = value
        empty_session.execute(text(
            'INSERT INTO review (comment, rating, user_id, podcast_id) VALUES (:comment, :rating, :user_id, :podcast_id)'),
            {'comment': comment, 'rating': rating, 'user_id': user_id, 'podcast_id': podcast_id}
        )

    rows = list(empty_session.execute(text('SELECT review_id from review')))
    review_ids = tuple(row[0] for row in rows)
    return review_ids


def insert_playlist(empty_session, values=None):
    new_playlist_id = 1
    new_user_id = 1
    new_playlist_name = "user's Playlist"

    if values is not None:
        new_playlist_id = values[0]
        new_user_id = values[1]
        new_playlist_name = values[2]

    empty_session.execute(text('INSERT INTO playlist (playlist_id, user_id, playlist_name) VALUES (:playlist_id, :user_id, :playlist_name)'),
        {'playlist_id': new_playlist_id, 'user_id': new_user_id, 'playlist_name': new_playlist_name})
    playlist_id = empty_session.execute(text('SELECT playlist_id FROM playlist where user_id = :user_id'),
        {'user_id': new_user_id}).fetchone()
    return playlist_id[0]



def insert_playlists(empty_session, values):
    for value in values:
        playlist_id, user_id, playlist_name = value
        empty_session.execute(text(
            'INSERT INTO playlist (playlist_id, user_id, playlist_name) VALUES (:playlist_id, :user_id, :playlist_name)'),
            {'playlist_id': playlist_id, 'user_id': user_id, 'playlist_name': playlist_name}
        )

    rows = list(empty_session.execute(text('SELECT playlist_id from playlist')))
    playlist_ids = tuple(row[0] for row in rows)
    return playlist_ids


def insert_playlist_episode_association(empty_session, playlist_id, episode_ids):
    stmt = text('INSERT INTO playlist_episode (playlist_id, episode_id) VALUES (:playlist_id, :episode_id)')

    for episode_id in episode_ids:
        empty_session.execute(stmt, {'playlist_id': playlist_id, 'episode_id': episode_id})


# MAKE METHODS

def make_user():
    user = User("user", "password")
    return user


def make_user2():
    user = User("user2", "password")
    return user


def make_author():
    author = Author(1, "D Hour Radio Network")
    return author


def make_podcast(): # Not sure if i did this one correct :')
    podcast_author = Author(1, "test_author")
    podcast = Podcast(1,
                      podcast_author,
                      "test_post",
                      "http://image",
                      'description',
                      "http://www.website",
                      329,
                      "English")
    return podcast


def make_episode():
    episode = Episode(1, 32,
                  "test_title",
                  "http://www.test_link", 329,
                  "test_description",
                  "2017-12-01 00:09:47+00")
    return episode


def make_category():
    category = Category(1, "category")
    return category


def make_review():
    review = Review(1, make_podcast(), make_user(), 5, "yes")
    return review


def make_playlist():
    playlist = Playlist(1, make_user(), "user's Playlist")
    return playlist


# TESTS

def test_loading_of_users(empty_session):
    users = list()
    users.append(("user", "password"))
    users.append(("resu", "Drop123"))
    insert_users(empty_session, users)

    expected = [
        User("user", "password"),
        User("resu", "Drop123")
    ]
    assert empty_session.query(User).all() == expected


def test_saving_of_users(empty_session):
    user = make_user()
    empty_session.add(user)
    empty_session.commit()

    rows = list(empty_session.execute(text('SELECT username, password FROM users')))
    assert rows == [("user", "password")]


def test_saving_of_users_with_common_user_name(empty_session):
    insert_user(empty_session, ("user", "password"))
    empty_session.commit()

    with pytest.raises(IntegrityError):
        user = User("user", "pass")
        empty_session.add(user)
        empty_session.commit()


# TODO unit tests
# AUTHOR
def test_loading_of_author(empty_session):
    author_id = insert_author(empty_session)
    empty_session.commit()
    expected_author = make_author()
    fetched_author = empty_session.query(Author).one()

    assert expected_author == fetched_author
    assert author_id == fetched_author.id


def test_saving_of_author(empty_session):
    author = make_author()
    empty_session.add(author)
    empty_session.commit()

    rows = list(empty_session.execute(text('SELECT author_id, name FROM authors')))
    assert rows == [(1, "D Hour Radio Network")]


# PODCAST
def test_loading_of_podcast(empty_session):
    podcast_id = insert_podcast(empty_session)
    empty_session.commit()
    expected_podcast = make_podcast()
    fetched_podcast = empty_session.query(Podcast).one()

    assert expected_podcast == fetched_podcast
    assert podcast_id == fetched_podcast.id


def test_saving_of_podcast(empty_session):
    podcast_author = Author(1, "test_author")
    podcast = Podcast(1,
                      podcast_author,
                      "test_post",
                      "http://image",
                      'description',
                      "http://www.website",
                      329,
                      "English")

    podcast = make_podcast()
    empty_session.add(podcast)
    empty_session.commit()

    rows = list(empty_session.execute(text('SELECT podcast_id, title, image_url, description, language, website_url, author_id, itunes_id FROM podcasts')))
    assert rows == [(1, "test_post", "http://image", "description", "English", "http://www.website", 1, 329)]


# EPISODE
def test_loading_of_episodes(empty_session):
    ep_id = insert_episode(empty_session)
    empty_session.commit()
    expected_episode = make_episode()
    fetched_episode = empty_session.query(Episode).one()

    assert expected_episode == fetched_episode
    assert ep_id == fetched_episode.episode_id


def test_saving_of_episodes(empty_session):
    episode = make_episode()
    empty_session.add(episode)
    empty_session.commit()

    rows = list(empty_session.execute(text('SELECT episode_id, podcast_id, title, audio_link, audio_length, description, pub_date FROM episodes')))
    assert rows == [(1, 32, "test_title", "http://www.test_link", 329, "test_description", "2017-12-01 00:09:47+00")]


# CATEGORIES
def test_loading_of_category(empty_session):
    categories = [
        ("Anteater"),
        ("NewZealand"),
    ]
    insert_categories(empty_session, categories)
    cat = empty_session.query(Category).all()
    expected = [
        Category(1, "Anteater"),
        Category(2, "NewZealand"),
    ]
    assert cat == expected

def test_saving_of_category(empty_session):
    category = make_category()
    empty_session.add(category)
    empty_session.commit()

    rows = list(empty_session.execute(text('SELECT category_id, category_name FROM categories')))
    assert rows == [(1, "category")]


# REVIEW

def test_loading_of_review(empty_session):
    get_review_id = insert_review(empty_session)
    expected_review = make_review()
    fetched_review = empty_session.query(Review).one()

    assert expected_review == fetched_review
    assert get_review_id == fetched_review.review_id


def test_loading_of_reviews(empty_session):
    reviews = list()
    reviews.append(("NewReview", 5, 1, 1))
    reviews.append(("another_review", 3, 1, 1))
    ids = insert_reviews(empty_session, reviews)

    fetched_reviews = empty_session.query(Review).all()
    expected_reviews = [
        Review(ids[0], make_podcast(), make_user(), 5, "NewReview"),
        Review(ids[1], make_podcast(), make_user(), 3, "another_review")
    ]
    assert fetched_reviews == expected_reviews


def test_saving_of_review(empty_session):
    review = make_review()
    empty_session.add(review)
    empty_session.commit()

    rows = list(empty_session.execute(text('SELECT review_id, comment FROM review')))
    assert rows == [(1, "yes")]


# PLAYLIST
def test_loading_of_playlist(empty_session):
    get_playlist_id = insert_playlist(empty_session)
    expected_playlist = make_playlist()
    fetched_playlist = empty_session.query(Playlist).one()

    assert expected_playlist == fetched_playlist
    assert get_playlist_id == fetched_playlist.playlist_id


def test_loading_of_playlists(empty_session):
    playlists = list()
    playlists.append((1, 1,"user's Playlist"))
    playlists.append((2, 2, "user2's Playlist"))
    playlist_ids = insert_playlists(empty_session, playlists)

    fetched_playlists = empty_session.query(Playlist).all()
    expected_playlists = [
        Playlist(playlist_ids[0], make_user(), "user's Playlist"),
        Playlist(playlist_ids[1], make_user2(), "user2's Playlist")
    ]
    assert fetched_playlists == expected_playlists

def test_saving_of_playlist(empty_session):
    playlist = make_playlist()
    empty_session.add(playlist)
    empty_session.commit()

    rows = list(empty_session.execute(text('SELECT playlist_id, playlist_name FROM playlist')))
    assert rows == [(1, "user's Playlist")]


def test_saving_episode_under_playlist(empty_session):
    playlist = make_playlist()
    episode = make_episode()
    playlist.add_episode(episode)
    empty_session.add(playlist)
    empty_session.commit()

    rows = list(empty_session.execute(text('SELECT playlist_id from playlist')))
    playlist_id = rows[0][0]

    rows = list(empty_session.execute(text('SELECT episode_id from episodes')))
    episode_id = rows[0][0]

    rows = list(empty_session.execute(text('SELECT playlist_id, episode_id FROM playlist_episode')))
    playlist_key = rows[0][0]
    episode_key = rows[0][1]

    assert playlist_id == playlist_key
    assert episode_id == episode_key



# PODCAST CATEGORY ASSOCIATION
def test_saving_podcast_under_category(empty_session):
    podcast = make_podcast()
    category = make_category()

    podcast.add_category(category)

    empty_session.add(podcast)
    # empty_session.add(category)
    empty_session.commit()

    rows = list(empty_session.execute(text('SELECT podcast_id FROM podcasts')))
    # print("number of rows:", rows)
    podcast_id = rows[0][0]

    rows = list(empty_session.execute(text('SELECT category_id FROM categories')))
    category_id = rows[0][0]

    rows = list(empty_session.execute(text('SELECT podcast_id, category_id FROM podcast_categories')))
    podcast_key = rows[0][0]
    category_key = rows[0][1]

    assert podcast_id == podcast_key
    assert category_id == category_key

