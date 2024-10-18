
#this was from lab08 as a template for orm.py I havent changed anythign


from sqlalchemy import (
    Table, Column, Integer, Float, String, DateTime, ForeignKey, Text,
    MetaData
)
from sqlalchemy.orm import registry, relationship
from datetime import datetime

from podcast.domainmodel.model import Podcast, Author, Category, User, Review, Episode, Playlist

# Global variable giving access to the MetaData (schema) information of the database
mapper_registry = registry()
metadata = MetaData()

authors_table = Table(
    'authors', mapper_registry.metadata,
    Column('author_id', Integer, primary_key=True),
    Column('name', String(255), nullable=False, unique=True)
)

podcast_table = Table(
    'podcasts', mapper_registry.metadata,
    Column('podcast_id', Integer, primary_key=True),
    Column('title', Text, nullable=True),
    Column('image_url', Text, nullable=True),
    Column('description', String(255), nullable=True),
    Column('language', String(255), nullable=True),
    Column('website_url', String(255), nullable=True),
    Column('author_id', ForeignKey('authors.author_id')),
    Column('itunes_id', Integer, nullable=True)
)

# Episodes should have links to its podcast through its foreign keys
episode_table = Table(
    'episodes', mapper_registry.metadata,
    Column('episode_id', Integer, primary_key=True),
    Column('podcast_id', ForeignKey('podcasts.podcast_id')),
    Column('title', Text, nullable=True),
    Column('audio_link', Text, nullable=True),
    Column('audio_length', Integer, nullable=True),
    Column('description', String(255), nullable=True),
    Column('pub_date', Text, nullable=True)
)

categories_table = Table(
    'categories', mapper_registry.metadata,
    Column('category_id', Integer, primary_key=True, autoincrement=True),
    Column('category_name', String(64), nullable=False)
)

podcast_categories_table = Table(
    'podcast_categories', mapper_registry.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('podcast_id', ForeignKey('podcasts.podcast_id')),
    Column('category_id', ForeignKey('categories.category_id'))
)

users_table = Table(
    'users', mapper_registry.metadata,
    Column('user_id', Integer, primary_key=True, autoincrement=True),
    Column('username', Text,  unique=True, nullable=False),
    Column('password', Text, nullable=False),
)

# Resolve definition for Review table and the necessary code that maps the table to its domain model class
# Reviews should have links to its podcast and user through its foreign keys
reviews_table = Table(
    'review', mapper_registry.metadata,
    Column('review_id', Integer, primary_key=True, autoincrement=True),
    Column('comment', String(255), nullable=True), #can be empty),
    Column('rating', Integer, nullable=False),
    Column('user_id',ForeignKey('users.user_id')),
    Column('podcast_id', ForeignKey('podcasts.podcast_id')),
)

playlist_table = Table(
    'playlist', mapper_registry.metadata,
    Column('playlist_id', Integer, primary_key=True, autoincrement=True, nullable=False),
    Column('user_id', ForeignKey('users.user_id')),
    Column('playlist_name', String(31), nullable=False),
)

playlist_episode_table = Table(
    'playlist_episode', mapper_registry.metadata,
    Column('playlist_id', Integer, ForeignKey('playlist.playlist_id'), primary_key=True),
    Column('episode_id', Integer, ForeignKey('episodes.episode_id'), primary_key=True)
)
def map_model_to_tables():

    mapper_registry.map_imperatively(Author, authors_table, properties={
        '_id': authors_table.c.author_id,
        '_name': authors_table.c.name,
    })

    mapper_registry.map_imperatively(Category, categories_table, properties={
        '_id': categories_table.c.category_id,
        '_name': categories_table.c.category_name,
        '_podcasts': relationship(Podcast, secondary=podcast_categories_table, back_populates='_categories'),
    })

    mapper_registry.map_imperatively(Podcast, podcast_table, properties={
        '_id': podcast_table.c.podcast_id,
        '_title': podcast_table.c.title,
        '_image': podcast_table.c.image_url,
        '_description': podcast_table.c.description,
        '_language': podcast_table.c.language,
        '_website': podcast_table.c.website_url,
        '_itunes_id': podcast_table.c.itunes_id,
        '_author': relationship(Author),
        # '_Podcast_episodes': relationship(Episode, back_populates='_Episode__podcast_id'),
        '_reviews': relationship(Review, back_populates='_podcast'),
        '_categories': relationship(Category, secondary=podcast_categories_table, back_populates='_podcasts'),
    })



    mapper_registry.map_imperatively(Episode, episode_table, properties={
        '_episode_id': episode_table.c.episode_id,
        '_podcast_id': episode_table.c.podcast_id, #relationship(Podcast, back_populates='_Podcast__episodes'),
        '_title': episode_table.c.title,
        '_audio_link': episode_table.c.audio_link, # check original csv file
        '_audio_length': episode_table.c.audio_length,
        '_description': episode_table.c.description,
        '_pub_date': episode_table.c.pub_date,
        '_playlists': relationship(Playlist, secondary=playlist_episode_table, back_populates='_episodes'),
    })

    mapper_registry.map_imperatively(User, users_table, properties={
        '_user_id': users_table.c.user_id,
        '_username': users_table.c.username,
        '_password': users_table.c.password,
        '_reviews': relationship(Review, back_populates='_user'),
        '_playlist': relationship(Playlist, back_populates='_owner'),


    })
    mapper_registry.map_imperatively(Review, reviews_table, properties={
        '_review_id': reviews_table.c.review_id,
        '_comment': reviews_table.c.comment,
        '_rating': reviews_table.c.rating,
        '_podcast': relationship(Podcast, back_populates='_reviews'),
        '_user': relationship(User, back_populates='_reviews'),
    })

    mapper_registry.map_imperatively(Playlist, playlist_table, properties={
        '_owner': relationship(User, back_populates='_playlist'),
        '_playlist_id': playlist_table.c.playlist_id,
        '_playlist_name': playlist_table.c.playlist_name,
        '_episodes': relationship(Episode, secondary=playlist_episode_table, back_populates='_playlists')
    })
