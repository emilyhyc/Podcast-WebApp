from sqlalchemy import select, inspect, create_engine
from sqlalchemy.orm import sessionmaker
import pytest

from podcast.adapters.orm import mapper_registry

def test_database_populate_inspect_table_names(database_engine):
    inspector = inspect(database_engine)
    assert inspector.get_table_names() == ['authors', 'categories', 'episodes', 'playlist', 'playlist_episode',
                                           'podcast_categories', 'podcasts', 'review', 'users']

def test_database_populate_select_all_podcasts(database_engine):
    inspector = inspect(database_engine)
    name_of_podcasts_table = inspector.get_table_names()[6]
    select_statement = select(mapper_registry.metadata.tables[name_of_podcasts_table])

    with database_engine.connect() as connection:
        result = connection.execute(select_statement)
        all_podcasts = []
        for row in result:
            all_podcasts.append((row[0], row[1]))  # id and title
    assert all_podcasts[0] == (1, 'D-Hour Radio Network')
    assert all_podcasts[1] == (2, 'Brian Denny Radio')
    assert all_podcasts[2] == (3, 'Onde Road - Radio Popolare')


def test_database_populate_select_all_authors(database_engine):
    inspector = inspect(database_engine)
    name_of_authors_table = inspector.get_table_names()[0]
    select_statement = select(mapper_registry.metadata.tables[name_of_authors_table])

    with database_engine.connect() as connection:
        result = connection.execute(select_statement)
        all_authors = []
        for row in result:
            all_authors.append(row[1])  # title
    assert all_authors[0] == ('D Hour Radio Network')
    assert all_authors[1] == ('Brian Denny')
    assert all_authors[2] == ('Radio Popolare')



def test_database_populate_select_all_episodes(database_engine):
    inspector = inspect(database_engine)
    name_of_episodes_table = inspector.get_table_names()[2]
    select_statement = select(mapper_registry.metadata.tables[name_of_episodes_table])

    with database_engine.connect() as connection:
        result = connection.execute(select_statement)
        all_episodes = []
        for row in result:
            all_episodes.append((row[0], row[2]))  # id and title

    assert all_episodes[0] == (1, 'The Mandarian Orange Show Episode 74- Bad Hammer Time, or: 30 Day MoviePass Challenge Part 3')
    assert all_episodes[1] == (2, 'Finding yourself in the character by justifying your actions')
    assert all_episodes[2] == (3, 'Episode 182 - Lyrically Weak')

def test_database_populate_select_all_categories(database_engine):
    inspector = inspect(database_engine)
    name_of_categories_table = inspector.get_table_names()[1]
    select_statement = select(mapper_registry.metadata.tables[name_of_categories_table])

    with database_engine.connect() as connection:
        result = connection.execute(select_statement)

        all_categories = []
        for row in result:
            all_categories.append((row[0], row[1]))  # id and category name

    print(all_categories)
    assert all_categories[0] == (1, "Society & Culture")
    assert all_categories[1] == (2, "Personal Journals")
    assert all_categories[2] == (3, "Professional")