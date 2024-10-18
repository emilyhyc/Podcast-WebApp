import abc
from typing import List
from datetime import date
from podcast.domainmodel.model import Podcast, Episode, User, Review, Playlist, Category, Author

repo_instance = None

class AbstractRepository(abc.ABC):

    #users
    @abc.abstractmethod
    def add_user(self, user: User):
        """ Adds a user to the repository """
        raise NotImplementedError

    @abc.abstractmethod
    def remove_user(self, user: User):
        """
            clears users for unit testing
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, username: str):
        """
        Returns user (username, not user) with given username from the repository
        If no user is found, return None
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_user_object(self, username: str):
        """
            Returns user obj with given username from the repository
            If no user is found, return None
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_all_user(self):
        """
        Return all users' username in a list
        """
        raise NotImplementedError

    #podcast

    @abc.abstractmethod
    def add_podcast(self, podcast: Podcast):
        """ Adds a Podcast to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_podcast(self, podcast_id: int) -> Podcast:
        """ Returns Podcast with id from the repository.
        If no Podcast with the given id exists, this method returns None.
        """
        raise NotImplementedError

    #episode

    @abc.abstractmethod
    def add_episode(self, episode: Episode):
        """ Adds an episode to the repository """
        raise NotImplementedError

    #@abc.abstractmethod
    #def get_episodes_by_id(self, id_list):
        #""" Gets a list of episodes in the repository that match the ids in the id_list
        #If no such episodes exist, this returns an empty list """
        #raise NotImplementedError

    #@abc.abstractmethod
    #def get_podcasts_by_id(self, id_list):
        #""" Gets a list of podcasts in the repository that match the ids in the id_list
        #If no such podcasts exist, this returns an empty list """
        #raise NotImplementedError

    @abc.abstractmethod
    def get_episode(self, episode_id: int) -> Episode:
        """ Returns Episode with id from the repository.
        If no Episode with the given id exists, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_all_episodes(self) -> list:
        """
        returns all episodes in library
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_all_podcasts(self) -> list:
        """
        returns all podcast in library
        """
        raise NotImplementedError

    #@abc.abstractmethod
    #def get_episode_by_date(self, target_date: date) -> List[Episode]:
        #""" Returns a list of Episodes that were published on target_date.
        #If there are no Episodes on the given date, this method returns an empty list.
        #"""
        #raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_episodes(self) -> int:
        """ Returns number of episodes in the repository """
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_podcasts(self) -> int:
        """ Returns number of podcasts in the repository """
        raise NotImplementedError


    #@abc.abstractmethod
    #def get_previous_episode_by_date(self, episode: Episode):
        #""" Returns the previous episode in a podcast by date
        #If no such episode exists, returns None"""
        #raise NotImplementedError

    #@abc.abstractmethod
    #def get_next_episode_by_date(self, episode: Episode):
        #""" Returns the next episode in a podcast by date
        #If no such episode exists, returns None """
        #raise NotImplementedError

    @abc.abstractmethod
    def pagination(self, num_items: list, item_per_page: int) -> int:
        """
        pagination function for browsing all podcasts and episodes
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_episodes_by_podcast(self, podcast_id: int) -> List[Episode]:
        """
        returns episode list in podcast from specific podcast id
        """
        raise NotImplementedError

    #category

    @abc.abstractmethod
    def get_all_categories(self) -> set:
        """ get set of all categories
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_category(self, category_id: int):
        """
        get category by category id
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_category(self, category: Category):
        """
       add category
        """
        raise NotImplementedError
    @abc.abstractmethod
    def get_podcasts_by_category(self, category_id: int):
        """
        get all podcasts in that category_id
        """
        raise NotImplementedError
    @abc.abstractmethod
    def add_multiple_categories(self, categories: List[Category]):
        """
        add all Categories to category list
        """
        raise NotImplementedError

    #review
    @abc.abstractmethod
    def get_all_reviews(self) -> list:
        """
        get all reviews in that category_id
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_review(self, podcast: Podcast, user: User, rating: int, comment: str = "") -> Review:
        """
        assign review id and create new review
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_all_reviews_by_podcast(self, podcast_id: int) -> list:
        """
        get all [reviews] from a specific podcast id.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def remove_review(self, review: Review):
        """
            removes review from review list
        """
        raise NotImplementedError

    #playlist

    @abc.abstractmethod
    def check_for_playlist(self, user: User) -> bool:
        """
        Checks if user has a playlist.
        """
        raise NotImplementedError

    def set_playlist(self, user: User):
        """
        Sets user playlist.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_playlist(self, user: User) -> list:
        """
        Returns all Episodes in a playlist.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_episode_to_playlist(self, episode: Episode, user: User):
        """
        Add an episode to the playlist, if episode already exists then it does not add again.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_podcast_to_playlist(self, podcast: Podcast, user: User):
        """
        Adds an entire podcasts episodes to the playlist, if an episode from the podcast is already in there, it does not add again.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def remove_episode_from_playlist(self, episode: Episode, user: User):
        """
        If such an episode exists in playlist, episode will be removed.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_playlist(self, playlist: Playlist):
        """
        Adds a playlist to memory repository that contains all existing playlists.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_all_playlists(self) -> List[Playlist]:
        """
        Gets a list of playlists of all users
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_playlist_by_user(self, user: User) -> Playlist:
        """
        Returns playlist by user, if none exists, returns none.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_multiple_episodes(self, episode: List[Episode]):
        """ Add multiple episodes to the repository of episode. """
        raise NotImplementedError

    #authors
    @abc.abstractmethod
    def add_multiple_podcasts(self, podcasts: List[Podcast]):
        """
        add a list of podcasts to the main list of podcasts
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_multiple_authors(self, author: set[Author]):
        """ Add multiple authors to the repository. """
        raise NotImplementedError

    #search
    @abc.abstractmethod
    def search_podcast_by_title(self, title_string: str) -> List[Podcast]:
        """Search for the podcast whose title includes the parameter title_string.
        It searches for the podcast title in case-insensitive and without trailing space.
        For example, the title 'Empire' will be searched if the title_string is 'empir'. """
        raise NotImplementedError

    @abc.abstractmethod
    def search_podcast_by_author(self, author_name: str) -> List[Podcast]:
        """Search for the podcast whose author contains the input author_name string.
        It searches for author names in case-insensitive and without trailing spaces.
        Returns searched podcast as a list
        """
        raise NotImplementedError

    @abc.abstractmethod
    def search_podcast_by_category(self, category_string: str) -> List[Podcast]:
        """Search for the podcast whose categories contain the input category_string.
        If any of the podcast's categories contain the substring category_string, that podcast should be selected for the search.
        It searches for category names in case-insensitive and without trailing spaces.
        Returns searched podcast as a list
        """
        raise NotImplementedError



