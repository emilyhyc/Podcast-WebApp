import csv, os
from pathlib import Path
from datetime import date, datetime
from typing import List
from podcast.adapters.datareader.csvdatareader import CSVDataReader
from podcast.domainmodel.model import Episode, Podcast, Author, Category, User, Review, Playlist
from podcast.adapters.repository import AbstractRepository
from util import get_project_root

from werkzeug.security import generate_password_hash


class MemoryRepository(AbstractRepository):
    def __init__(self):
        data_path = Path('adapters') / 'data'
        dir_name = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.'))
        podcast_filename = os.path.join(dir_name, str(Path(data_path) / "podcasts.csv"))
        episode_filename = os.path.join(dir_name, str(Path(data_path) / "episodes.csv"))

        csv_reader = CSVDataReader(podcast_filename, episode_filename)
        csv_reader.podcasts_csv()
        csv_reader.episodes_csv()
        self.__podcasts = csv_reader.podcast_list
        self.__episodes = csv_reader.episode_list
        self.__categories = csv_reader.categories
        self.__reviews = []
        self.__review_counter = 0
        self.__users = []
        self.__playlist = None
        self.__playlists = []

    def add_user(self, user: User):
        password_hash = generate_password_hash(user.password)
        new_user = User(user.username, password_hash)
        self.__users.append(new_user)

    #this one returns the username if it exists in self.users
    def get_user(self, username: str):
        for u in self.__users:
            if u.username == username:
                return u.username
        return None

    #this one returns the user object if it exists in self.users
    def get_user_object(self, username: str):
        for u in self.__users:
            if u.username == username:
                return u
        return None

    #this one returns list of all users' username
    def get_all_user(self):
        return self.__users

    def add_podcast(self, podcast: Podcast):
        self.__podcasts.append(podcast)

    def get_podcast(self, podcast_id: int):
        for podcast in self.__podcasts:
            if podcast.id == podcast_id:
                return podcast
        return None

    def get_all_podcasts(self) -> list:
        return self.__podcasts

    def add_episode(self, episode: Episode):
        self.__episodes.append(episode)

    def get_episode(self, episode_id: int) -> Episode:
        for episode in self.__episodes:
            if episode.episode_id == episode_id:
                return episode


    def get_all_episodes(self) -> list:
        return self.__episodes

    #def get_episodes_by_id(self, list_of_ids):
        #episodes_with_id = []
        #for ids in list_of_ids:
            #for episode in self.__episodes:
                #if episode.episode_id == ids:
                    #episodes_with_id.append(episode)
                    #break
        #return episodes_with_id

    #def get_podcasts_by_id(self, list_of_ids):
        #podcasts_with_id = []
        #for ids in list_of_ids:
            #for podcast in self.__podcasts:
                #if podcast.id == ids:
                    #podcasts_with_id.append(podcast)
                    #break
        #return podcasts_with_id

    #def get_episode_by_date(self, target_date: date) -> List[Episode]:
        #matching_episodes = list()
        #if len(self.__episodes) != 0:
            #for episode in self.__episodes:
                #check_date = date(int(episode.pub_date.strftime("%Y")),
                                  #int(episode.pub_date.strftime("%m")),
                                  #int(episode.pub_date.strftime("%d")))
                #if check_date == target_date:
                    #matching_episodes.append(episode)

        #return matching_episodes

    def get_number_of_episodes(self) -> int:
        return len(self.__episodes)

    def get_number_of_podcasts(self) -> int:
        return len(self.__podcasts)

    #def get_previous_episode_by_date(self, episode: Episode):
       # podcast_episodes = list()
        #previous_episode = episode
        #for checking_episode in self.__episodes:
            #if checking_episode.podcast_id == episode.podcast_id:
                #podcast_episodes.append(checking_episode)
        #sorted_podcast_episodes = sorted(podcast_episodes,
                                         #key=lambda e: e.pub_date)  # oldest to newest

        #current_index = sorted_podcast_episodes.index(episode)
        #if current_index == 0:
            # There is no previous episode, current 'previous_episode' is the oldest episode in the podcast
            #return None
        #previous_episode = sorted_podcast_episodes[current_index - 1]
        #return previous_episode

    #def get_next_episode_by_date(self, episode: Episode):
       # podcast_episodes = list()
        #next_episode = episode

        #for checking_episode in self.__episodes:
            #if checking_episode.podcast_id == episode.podcast_id:
                #podcast_episodes.append(checking_episode)
        #sorted_podcast_episodes = sorted(podcast_episodes,
                                         #key=lambda e: e.pub_date)  # oldest to newest
        #current_index = sorted_podcast_episodes.index(episode)
        #try:
            #next_episode = sorted_podcast_episodes[current_index + 1]
        #except IndexError:
            # There are no episodes after this episode, 'next_episode' is the newest episode in the podcast
            #return None
        #return next_episode

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
        episode_list = []
        for episode in self.__episodes:
            if episode.podcast_id == podcast_id:
                episode_list.append(episode)
        return episode_list

    def get_all_categories(self) -> set:
        return self.__categories

    def add_category(self, category: Category):
        self.__categories.add(category)

    def get_category(self, category_id: int):
        for category in self.__categories:
            if category.id == category_id:
                return category
        return None

    def get_podcasts_by_category(self, category_id: int):
        podcasts_with_category = []
        for podcast in self.__podcasts:
            for cat in podcast.categories:
                if cat.id == category_id:
                    podcasts_with_category.append(podcast)
        return podcasts_with_category

    def get_all_reviews(self) -> list:
        return self.__reviews

    def add_review(self, podcast: Podcast, user: User, rating: int, comment: str = "") -> Review:
        self.__review_counter += 1
        new_review = Review(review_id=self.__review_counter, podcast=podcast, user=user, rating=rating, comment=comment)
        self.__reviews.append(new_review)
        return new_review

    def get_all_reviews_by_podcast(self, podcast_id: int) -> list:
        all_reviews = []
        print(self.__reviews)
        print("yop")
        for review in self.__reviews:
            if review.podcast.id == podcast_id:
                all_reviews.append(review)
        print(f"Reviews for podcast {podcast_id}: {all_reviews}")
        print(f"users {self.__users}")
        return all_reviews

    def check_for_playlist(self, user: User) -> bool:
        return self.get_playlist_by_user(user) is not None

    def set_playlist(self, user: User):
        existing_playlist = self.get_playlist_by_user(user)
        if existing_playlist:
            self.__playlist = existing_playlist

        else:
            new_playlist_id = len(self.__playlists) + 1
            playlist_username = f"{user.username}'s Playlist"
            new_playlist = Playlist(new_playlist_id, user, playlist_username)
            self.add_playlist(new_playlist)
            self.__playlist = new_playlist

    def get_playlist(self, user: User) -> Playlist:
        print(self.__playlists)
        playlist = self.get_playlist_by_user(user)
        if playlist:
            return playlist
        else:
            raise ValueError(f"No playlist has been set for user {user.username}.")

    def add_episode_to_playlist(self, episode: Episode, user: User):
        if not isinstance(episode, Episode):
            raise TypeError("Expected an Episode instance.")
        if self.__playlist is None:
            self.set_playlist(user)
        if self.__playlist is not None and self.__playlist.owner == user:
            if episode not in self.__playlist.episodes:
                self.__playlist.episodes.append(episode)

    def remove_episode_from_playlist(self, episode: Episode, user: User):
        if self.__playlist is not None and self.__playlist.owner == user:
            if episode in self.__playlist.episodes:
                self.__playlist.episodes.remove(episode)


    def add_podcast_to_playlist(self, podcast: Podcast, user: User):
        if not isinstance(podcast, Podcast):
            raise TypeError("Expected a Podcast instance.")
        if podcast not in self.__podcasts:
            raise ValueError("Podcast does not exist.")
        if self.__playlist is not None and self.__playlist.owner == user:
            for episode in self.__episodes:
                if episode not in self.__playlist.episodes and episode.podcast_id == podcast.id:
                    self.__playlist.episodes.append(episode)


    # Managing all user playlists

    def add_playlist(self, playlist: Playlist):
        if not isinstance(playlist, Playlist):
            raise TypeError("Expected a Playlist instance.")
        self.__playlists.append(playlist)
        self.__playlist = None

    def get_all_playlists(self) -> List[Playlist]:
        return self.__playlists

    def get_playlist_by_user(self, user: User) -> Playlist:
        for playlist in self.__playlists:
            if playlist.owner == user:
                return playlist
        return None
        # raise ValueError("Playlist does not exist.")

    def remove_review(self, review:Review):
        if self.__reviews:
            for r in self.__reviews:
                if review.review_id == r.review_id:
                    self.__reviews.remove(r)

    def remove_user(self, user:User):
        if self.__users:
            for u in self.__users:
                if (user.username).lower() == (u.username).lower():
                    self.__users.remove(u)



    # the below functions are added to due the database function

    def add_multiple_categories(self, categories: List[Category]):
        pass

    def add_multiple_episodes(self, episode: List[Episode]):
        pass

    def add_multiple_podcasts(self, podcasts: List[Podcast]):
        pass

    def add_multiple_authors(self, author: set[Author]):
        pass

    def search_podcast_by_author(self, author_name: str) -> List[Podcast]:
        search_results = []
        for podcast in self.__podcasts:
            if str(author_name.lower()) in str(podcast.author.name.lower()):
                search_results.append(podcast)
        return search_results

    def search_podcast_by_category(self, category_string: str) -> List[Podcast]:
        search_results = []
        print(category_string)
        for podcast in self.__podcasts:
            if any(category_string.lower() in category.name.lower() for category in podcast.categories):
                search_results.append(podcast)
        return search_results

    def search_podcast_by_title(self, title_string: str) -> List[Podcast]:
        search_results = []
        for podcast in self.__podcasts:
            if title_string.lower() in podcast.title.lower():
                search_results.append(podcast)
        return search_results


def read_csv_file(filename: str):
    with open(filename, encoding='utf-8-sig') as infile:
        reader = csv.reader(infile)

        # Read first line of the the CSV file.
        headers = next(reader)

        # Read remaining rows from the CSV file.
        for row in reader:
            # Strip any leading/trailing white space from data read.
            row = [item.strip() for item in row]
            yield row

def load_users(data_path: Path, repo: MemoryRepository):
    users = dict()

    users_filename = str(Path(data_path) / "users.csv")
    for data_row in read_csv_file(users_filename):
        user = User(
            username=data_row[1],
            password=generate_password_hash(data_row[2])
        )
        repo.add_user(user)
        users[data_row[0]] = user
    return users

def populate(data_path: Path, repo: MemoryRepository):
    # Load users into the repository.
    users = {""}





