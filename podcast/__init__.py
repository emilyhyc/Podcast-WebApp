"""Initialize Flask app."""
from pathlib import Path

#from .adapters.memory_repository import MemoryRepository
from .home import home
from .podcasts import podcasts
from .search import search
from .categories import categories
from .browse import browse
from .authentication import authentication
from .review import review
from .playlist import playlist

from pathlib import Path
from flask import Flask, session

# imports from SQLAlchemy
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, clear_mappers
from sqlalchemy.pool import NullPool

from podcast.domainmodel.model import Podcast
from podcast.browse import browse

# local imports
import podcast.adapters.repository as repo
from podcast.adapters import memory_repository, database_repository, repository_populate
from podcast.adapters.repository_populate import populate
from podcast.adapters.orm import mapper_registry, map_model_to_tables




def create_app(test_config=None):
    app = Flask(__name__)

    # clear cache when re flask run
    app.config['FIRST_REQUEST'] = True
    @app.before_request
    def clear_session_on_first_run():
        if app.config['FIRST_REQUEST']:
            session.clear()  # Clear session
            app.config['FIRST_REQUEST'] = False

    app.config.from_object('config.Config')
    data_path = Path('adapters') / 'data'

    if test_config is not None:
        # Load test configuration, and override any configuration settings.
        app.config.from_mapping(test_config)
        data_path = app.config['TEST_DATA_PATH']

    if app.config['REPOSITORY'] == 'memory':
        # Create the MemoryRepository implementation for a memory-based repository.
        repo.repo_instance = memory_repository.MemoryRepository()
        # fill the content of the repository from the provided csv files (has to be done every time we start app!)
        # database_mode = False
        # repository_populate.populate(data_path, repo.repo_instance)

    elif app.config['REPOSITORY'] == 'database':
        database_uri = app.config['SQLALCHEMY_DATABASE_URI']
        database_echo = app.config['SQLALCHEMY_ECHO']

    # Create a database engine and connect it to the specified database
        database_engine = create_engine(database_uri, connect_args={"check_same_thread": False}, poolclass=NullPool,
                                        echo=False)

    # Create the database session factory using sessionmaker (this has to be done once, in a global manner)
        session_factory = sessionmaker(autocommit=False, autoflush=True, bind=database_engine)

        # Create the SQLAlchemy DatabaseRepository instance for an sqlite3-based repository.
        repo.repo_instance = database_repository.SqlAlchemyRepository(session_factory)
        data_path = Path('adapters') / 'data'


        if len(inspect(database_engine).get_table_names()) == 0:
            print("REPOPULATING DATABASE...")
            # For testing, or first-time use of the web application, reinitialise the database.
            clear_mappers()
            # Conditionally create database tables.
            mapper_registry.metadata.create_all(database_engine)
            # Remove any data from the tables.
            for table in reversed(mapper_registry.metadata.sorted_tables):
                with database_engine.connect() as conn:
                    conn.execute(table.delete())

            # Generate mappings that map domain model classes to the database tables.
            map_model_to_tables()

            populate(data_path, repo.repo_instance, True)
            print("REPOPULATING DATABASE... FINISHED")

        else:
            # Solely generate mappings that map domain model classes to the database tables.
            map_model_to_tables()

    with app.app_context():
        app.register_blueprint(home.home_blueprint)
        app.register_blueprint(playlist.playlist_blueprint)
        app.register_blueprint(podcasts.podcasts_blueprint)
        app.register_blueprint(search.search_blueprint)
        app.register_blueprint(categories.categories_blueprint)
        app.register_blueprint(browse.browse_blueprint)
        app.register_blueprint(authentication.auth_blueprint)
        app.register_blueprint(review.review_blueprint)

    return app
