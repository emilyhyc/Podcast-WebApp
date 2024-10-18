from abc import ABC
from typing import List, Type
from podcast.adapters.orm import podcast_categories_table
from util import get_project_root as Path
from datetime import date, datetime

from sqlalchemy import func
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm.exc import NoResultFound

from podcast.adapters.repository import AbstractRepository
from podcast.domainmodel.model import Podcast, Author, Category, User, Review, Episode, Playlist

from werkzeug.security import generate_password_hash


# feature 1 test
class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        # this method can be used e.g. to allow Flask to start a new session for each http request,
        # via the 'before_request' callback
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory)

    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()


class SqlAlchemyRepository(AbstractRepository, ABC):

    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

    def add_user(self, user: User):
        password_hash = generate_password_hash(user.password)
        new_user = User(user.username, password_hash)

        print(f"new user object created: {new_user}")

        with self._session_cm as scm:
            scm.session.add(new_user)
            scm.session.commit()

    def remove_user(self, user: User):
        with self._session_cm as scm:
            scm.session.delete(user)
            scm.session.commit()

    def get_user(self, username: str):
        user = None
        try:
            username = username.strip().lower()
            query = self._session_cm.session.query(User).filter(
                User._username == username)
            user = query.one()
        except NoResultFound:
            print(f'User {username} was not found')

        return user

    def get_user_object(self, username: str):
        username = username.lower()
        user_obj = None
        try:
            query = self._session_cm.session.query(User).filter(User._username == username)
            user_obj = query.one()
        except NoResultFound:
            print(f'{username} was not found')
        return user_obj

    def get_all_user(self):
        return self._session_cm.session.query(User).all()


    # Podcast

    def add_podcast(self, podcast: Podcast):
        with self._session_cm as scm:
            scm.session.merge(podcast)
            scm.commit()

    def add_multiple_podcasts(self, podcasts: List[Podcast]):
        with self._session_cm as scm:
            for podcast in podcasts:
                scm.session.add(podcast)
            scm.commit()

    def get_podcast(self, podcast_id: int) -> Podcast:
        podcast = None
        try:
            query = self._session_cm.session.query(Podcast).filter(
                Podcast._id == podcast_id)
            podcast = query.one()
        except NoResultFound:
            print(f'Podcast {podcast_id} was not found')

        return podcast

    def get_all_podcasts(self) -> list[Type[Podcast]]:
        podcasts = self._session_cm.session.query(Podcast).all()
        return sorted(podcasts)

    def add_episode(self, episode: Episode):
        with self._session_cm as scm:
            scm.session.merge(episode)
            scm.commit()

    def add_multiple_episodes(self, episode: List[Episode]):
        with self._session_cm as scm:
            for episode in episode:
                scm.session.add(episode)
            scm.commit()



    def get_episode(self, episode_id: int) -> Episode:
        try:
            query = self._session_cm.session.query(Episode).filter(Episode._episode_id == episode_id)
            episode = query.one()
        except NoResultFound:
            print(f'Episode {episode_id} was not found')
            episode = None
        return episode

    def get_all_episodes(self) -> list:
        return self._session_cm.session.query(Episode).all()

    #def get_episodes_by_id(self, list_of_ids):
        #pass
            #im not too sure if we need to do this because im not sure if we used this.
            # we might just be able to remove it from the abstract repo. if not needed. lmk

    #def get_podcasts_by_id(self, list_of_ids):
        # im not too sure if we need to do this because im not sure if we used this.
        # we might just be able to remove it from the abstract repo. if not needed. lmk
        #pass

    #def get_episode_by_date(self, target_date: date) -> List[Episode]:
        #pass
        # im not too sure if we need to do this because im not sure if we used this.
        # we might just be able to remove it from the abstract repo. if not needed. lmk
        #we have never needed to search episode by date? IDK
        # can remove if you guys don't need it


    def get_number_of_episodes(self) -> int:
        num_episodes =  self._session_cm.session.query(Episode).count()
        return num_episodes

    def get_number_of_podcasts(self) -> int:
        num_podcasts = self._session_cm.session.query(Podcast).count()
        return num_podcasts

    #def get_previous_episode_by_date(self, episode: Episode):
        #pass
    #  im not too sure if we need to do this because im not sure if we used this.
    # this too idk if i need this. Because I use services to search for episodes in podcast by date.
    # can remove if you guys don't need it


    #def get_next_episode_by_date(self, episode: Episode):
        #pass
    #  im not too sure if we need to do this because im not sure if we used this.
    # can remove if you guys don't need it


    def pagination(self, item_list: list, item_per_page: int) -> int:
        num_items = len(item_list)
        if num_items < item_per_page:
            num_pages = 1
        elif num_items % item_per_page != 0:
            num_pages = num_items // item_per_page + 1
        else:
            num_pages = num_items // item_per_page

        return num_pages

    def get_episodes_by_podcast(self, podcast_id: int):
        """Get all episodes for a specific podcast by podcast_id."""
        all_episodes = (self._session_cm.session.query(Episode).filter(Episode._podcast_id == podcast_id).all())
        return all_episodes

    def get_all_categories(self) -> list[Type[Category]]:
        categories = self._session_cm.session.query(Category).all()
        return categories

    def get_category(self, category_id: int) -> Category:
        try:
            category = self._session_cm.session.query(Category).filter(Category._id == category_id).one()
        except NoResultFound:
            category = None
        return category

    def add_category(self, category: Category):
        with self._session_cm as scm:
            scm.session.merge(category)
            scm.commit()

    def get_podcasts_by_category(self, category_id: int):
        return self._session_cm.session.query(Podcast).join(podcast_categories_table).filter(
            podcast_categories_table.c.category_id == category_id
        ).all()

    def add_multiple_categories(self, categories: List[Category]):
        with self._session_cm as scm:
            with scm.session.no_autoflush:
                for category in categories:
                    scm.session.add(category)
            scm.commit()

        #review section
    def get_all_reviews(self) -> list:
        return self._session_cm.session.query(Review).all()

    def add_review(self, podcast: Podcast, user: User, rating: int, comment: str = "") -> Review:
        print(f"review {podcast} user{user}, rating{rating}, comment{comment}")
        session = self._session_cm.session
        ids = session.query(func.max(Review._review_id))
        maximum_id = ids.first()

        if maximum_id is None or maximum_id[0] is None:
            ID_counter = 0
        else:
            ID_counter = maximum_id[0]
        review_id = ID_counter + 1

        new_review = Review(review_id, podcast, user, rating, comment)
        session.add(new_review)
        session.commit()
        return new_review

    def get_all_reviews_by_podcast(self, podcast_id: int) -> list:
        all_reviews = (
            self._session_cm.session.query(Review).filter(Review._podcast.has(Podcast._id == podcast_id)).all()
        )
        return all_reviews

    def remove_review(self, review: Review):
        with self._session_cm as scm:
            scm.session.delete(review)
            scm.commit()

    # playlist section
    def check_for_playlist(self, user: User) -> bool:
        return self.get_playlist_by_user(user) is not None

    def set_playlist(self, user: User):
        with self._session_cm as scm:
            existing_playlist = self.get_playlist_by_user(user)
            if existing_playlist:
                return existing_playlist

            user_playlist_id = len(self.get_all_playlists()) + 1
            new_playlist = Playlist(user_playlist_id, user, f"{user.username}'s Playlist")
            scm.session.add(new_playlist)
            scm.commit()

    def get_playlist(self, user: User) -> Type[Playlist]:
        with self._session_cm as scm:
            playlist = scm.session.query(Playlist).filter_by(_owner=user).first()
            if not playlist:
                playlist = self.set_playlist(user)
            return playlist

    def add_episode_to_playlist(self, episode: Episode, user: User):
        with self._session_cm as scm:
            if self.get_playlist_by_user(user) is None:
                self.set_playlist(user)
            playlist = self.get_playlist_by_user(user)
            if episode not in playlist.episodes:
                print("Added")
                playlist.add_episode(episode)
                scm.session.commit()

    def remove_episode_from_playlist(self, episode: Episode, user: User):
        with self._session_cm as scm:
            playlist = self.get_playlist_by_user(user)
            if playlist and episode in playlist.episodes:
                playlist.remove_episode(episode)
                scm.session.commit()

    def add_podcast_to_playlist(self, podcast: Podcast, user: User):
        with self._session_cm as scm:
            if self.get_playlist_by_user(user) is None:
                self.set_playlist(user)
            playlist = self.get_playlist_by_user(user)

            pod_episodes = self.get_episodes_by_podcast(podcast.id)
            for episode in pod_episodes:
                if episode not in playlist.episodes:
                    playlist.add_episode(episode)
            scm.session.commit()

    def add_playlist(self, playlist: Playlist):
        with self._session_cm as scm:
            scm.session.add(playlist)
            scm.commit()

    def get_all_playlists(self) -> list[Type[Playlist]]:
        with self._session_cm as scm:
            return scm.session.query(Playlist).all()

    def get_playlist_by_user(self, user: User) -> Type[Playlist]:
        with self._session_cm as scm:
            return scm.session.query(Playlist).filter_by(_owner=user).first()

    # region Author data
    def add_multiple_authors(self, authors: List[Author]):
        with self._session_cm as scm:
            with scm.session.no_autoflush:
                for author in authors:
                    if author.name is None:
                        raise ValueError("Author name cannot be None")
                    scm.session.add(author)
            scm.commit()

    def search_podcast_by_title(self, title_string: str) -> List[Podcast]:
        # Retrieve podcast whose title contains the title_string passed by the user.
        # This is a case-insensitive search without trailing spaces.
        searched_podcasts = self._session_cm.session.query(Podcast).filter(
            (Podcast._title).contains(title_string.strip().lower())
        ).all()
        return searched_podcasts

    def search_podcast_by_author(self, author_name: str) -> List[Podcast]:
        """Retrieve podcasts whose author name matches the author_name passed by the user."""
        searched_podcasts = self._session_cm.session.query(Podcast).join(Author).filter(
            (Author._name).contains(author_name.strip().lower())
        ).all()
        return searched_podcasts

    def search_podcast_by_category(self, category_string: str) -> List[Podcast]:
        """Retrieve podcasts that belong to a category matching the category_string passed by the user."""
        searched_podcasts = self._session_cm.session.query(Podcast).join(podcast_categories_table).join(
            Category).filter(
            (Category._name).contains(category_string.strip().lower())).all()
        return searched_podcasts








