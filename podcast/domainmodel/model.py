from __future__ import annotations

from datetime import datetime


def validate_non_negative_int(value):
    if not isinstance(value, int) or value < 0:
        raise ValueError("ID must be a non-negative integer.")


def validate_non_empty_string(value, field_name="value"):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


class Author:
    def __init__(self, author_id: int, name: str):
        validate_non_negative_int(author_id)
        validate_non_empty_string(name, "Author name")
        self._id = author_id
        self._name = name.strip()
        self.podcast_list = []

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, new_name: str):
        validate_non_empty_string(new_name, "New name")
        self._name = new_name.strip()

    def add_podcast(self, podcast: Podcast):
        if not isinstance(podcast, Podcast):
            raise TypeError("Expected a Podcast instance.")
        if podcast not in self.podcast_list:
            self.podcast_list.append(podcast)

    def remove_podcast(self, podcast: Podcast):
        if podcast in self.podcast_list:
            self.podcast_list.remove(podcast)

    def __repr__(self) -> str:
        return f"<Author {self._id}: {self._name}>"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Author):
            return False
        return self.id == other.id

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Author):
            return False
        return self.name < other.name

    def __hash__(self) -> int:
        return hash(self.id)


class Podcast:
    def __init__(self, podcast_id: int, author: Author, title: str = "Untitled", image: str = None,
                 description: str = "", website: str = "", itunes_id: int = None, language: str = "Unspecified"):
        validate_non_negative_int(podcast_id)
        self._id = podcast_id
        self._author = author
        validate_non_empty_string(title, "Podcast title")
        self._title = title.strip()
        self._image = image
        self._description = description
        self._language = language
        self._website = website
        self._itunes_id = itunes_id
        self._categories = []
        self._episodes = []

    @property
    def id(self) -> int:
        return self._id

    @property
    def author(self) -> Author:
        return self._author

    @author.setter
    def author(self, author: Author):
        if isinstance(author, Author):
            self._author = author
        else:
            self._author = None

    @property
    def itunes_id(self) -> int:
        return self._itunes_id

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, new_title: str):
        validate_non_empty_string(new_title, "Podcast title")
        self._title = new_title.strip()

    @property
    def image(self) -> str:
        return self._image

    @image.setter
    def image(self, new_image: str):
        if new_image is not None and not isinstance(new_image, str):
            raise TypeError("Podcast image must be a string or None.")
        self._image = new_image

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, new_description: str):
        if not isinstance(new_description, str):
            validate_non_empty_string(new_description, "Podcast description")
        self._description = new_description

    @property
    def language(self) -> str:
        return self._language

    @language.setter
    def language(self, new_language: str):
        if not isinstance(new_language, str):
            raise TypeError("Podcast language must be a string.")
        self._language = new_language

    @property
    def website(self) -> str:
        return self._website

    @website.setter
    def website(self, new_website: str):
        validate_non_empty_string(new_website, "Podcast website")
        self._website = new_website

    @itunes_id.setter
    def itunes_id(self, value):
        self._itunes_id = value

    @property
    def categories(self) -> list:
        return self._categories


    def add_category(self, category: Category):
        if not isinstance(category, Category):
            raise TypeError("Expected a Category instance.")
        if category not in self._categories:
            self._categories.append(category)

    def remove_category(self, category: Category):
        if category in self._categories:
            self._categories.remove(category)

    def add_episode(self, episode: Episode):
        if not isinstance(episode, Episode):
            raise TypeError("Expected an Episode instance.")
        if episode not in self._episodes:
            self._episodes.append(episode)

    def remove_episode(self, episode: Episode):
        if episode in self._episodes:
            self._episodes.remove(episode)

    def __repr__(self):
        return f"<Podcast {self.id}: '{self.title}' by {self.author.name}>"

    def __eq__(self, other):
        if not isinstance(other, Podcast):
            return False
        return self.id == other.id

    def __lt__(self, other):
        if not isinstance(other, Podcast):
            return False
        return self.title < other.title
        #return self.id < other.id

    def __hash__(self):
        return hash(self.id)


class Category:
    def __init__(self, category_id: int, name: str):
        validate_non_negative_int(category_id)
        validate_non_empty_string(name, "Category name")
        self._id = category_id
        self._name = name.strip()

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, new_name: str):
        validate_non_empty_string(new_name, "New name")
        self._name = new_name.strip()

    def __repr__(self) -> str:
        return f"<Category {self._id}: {self._name}>"

    def __eq__(self, other):
        if not isinstance(other, Category):
            return False
        return self.id == other.id

    def __lt__(self, other):
        if not isinstance(other, Category):
            return False
        return self._name < other.name

    def __hash__(self):
        return hash(self._id)


class User:
    def __init__(self, username: str, password: str):
        # validate_non_negative_int(user_id)
        validate_non_empty_string(username, "Username")
        validate_non_empty_string(password, "Password")
        # self._id = user_id
        self._username = username.lower().strip()
        self._password = password
        self._subscription_list = []

    # @property
    # def id(self) -> int:
    #     return self._id

    @property
    def username(self):
        return self._username

    @property
    def password(self):
        return self._password

    @property
    def subscription_list(self):
        return self._subscription_list

    def add_subscription(self, subscription: PodcastSubscription):
        if not isinstance(subscription, PodcastSubscription):
            raise TypeError("Subscription must be a PodcastSubscription object.")
        if subscription not in self._subscription_list:
            self._subscription_list.append(subscription)

    def remove_subscription(self, subscription: PodcastSubscription):
        if subscription in self._subscription_list:
            self._subscription_list.remove(subscription)

    def __repr__(self):
        return f"<User {self._username}>"

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self._username == other.username

    def __hash__(self):
        return hash(self._username)

    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self._username < other.username


class PodcastSubscription:
    def __init__(self, sub_id: int, owner: User, podcast: Podcast):
        validate_non_negative_int(sub_id)
        if not isinstance(owner, User):
            raise TypeError("Owner must be a User object.")
        if not isinstance(podcast, Podcast):
            raise TypeError("Podcast must be a Podcast object.")
        self._id = sub_id
        self._owner = owner
        self._podcast = podcast

    @property
    def id(self) -> int:
        return self._id

    @property
    def owner(self) -> User:
        return self._owner

    @owner.setter
    def owner(self, new_owner: User):
        if not isinstance(new_owner, User):
            raise TypeError("Owner must be a User object.")
        self._owner = new_owner

    @property
    def podcast(self) -> Podcast:
        return self._podcast

    @podcast.setter
    def podcast(self, new_podcast: Podcast):
        if not isinstance(new_podcast, Podcast):
            raise TypeError("Podcast must be a Podcast object.")
        self._podcast = new_podcast

    def __repr__(self):
        return f"<PodcastSubscription {self.id}: Owned by {self.owner.username}>"

    def __eq__(self, other):
        if not isinstance(other, PodcastSubscription):
            return False
        return self.id == other.id and self.owner == other.owner and self.podcast == other.podcast

    def __lt__(self, other):
        if not isinstance(other, PodcastSubscription):
            return False
        return self.id < other.id

    def __hash__(self):
        return hash((self.id, self.owner, self.podcast))


class Episode:
    def __init__(self, episode_id: int, podcast_id: int, title: str, audio_link: str,
                 audio_length: int, description: str, pub_date=datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S+00")):

        validate_non_negative_int(episode_id)
        self._episode_id = episode_id

        validate_non_negative_int(podcast_id)
        self._podcast_id = podcast_id

        validate_non_empty_string(title, "Episode title")
        self._title = title

        self._audio_link = audio_link

        validate_non_negative_int(audio_length)
        self._audio_length = audio_length
        self._description = description
        self._pub_date = pub_date

    @property
    def episode_id(self) -> int:
        return self._episode_id

    @property
    def podcast_id(self) -> int:
        return self._podcast_id

    @podcast_id.setter
    def podcast_id(self, new_podcast_id: int):
        validate_non_negative_int(new_podcast_id)
        self._podcast_id = new_podcast_id

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, new_title: str):
        validate_non_empty_string(new_title, "Episode title")
        self._title = new_title

    @property
    def audio_link(self) -> str:
        return self._audio_link

    @audio_link.setter
    def audio_link(self, new_audio_link: str):
        self._audio_link = new_audio_link

    @property
    def audio_length(self) -> int:
        return self._audio_length

    @audio_length.setter
    def audio_length(self, new_audio_length):
        validate_non_negative_int(new_audio_length)
        self._audio_length = new_audio_length

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, new_description: str):
        self._description = new_description

    @property
    def pub_date(self) -> str:
        return self._pub_date

    @pub_date.setter
    def pub_date(self, new_pub_date):
        validate_non_empty_string(new_pub_date, "Date published")
        new_pub_date += "00"
        self._pub_date = datetime.strptime(new_pub_date, "%Y-%m-%d %H:%M:%S%z")

    def __repr__(self):
        return (f"<Episode id: {self.episode_id}" +
                f"Title: {self.title}, belongs to podcast: {self.podcast_id}>")

    def __eq__(self, other):
        if not isinstance(other, Episode):
            return False
        return self.episode_id == other.episode_id

    def __lt__(self, other):
        if not isinstance(other, Episode):
            return False
        return self.episode_id < other.episode_id

    def __hash__(self):
        return hash(self.episode_id)



class Review:
    def __init__(self, review_id: int, podcast: Podcast, user: User, rating: int, comment: str = ""):
        validate_non_negative_int(review_id)
        self._review_id = review_id

        if not isinstance(podcast, Podcast):
            raise TypeError("You can only review a Podcast object")
        self._podcast = podcast

        if not isinstance(user, User):
            raise TypeError(f"Owner must be a User object, instead {type(user)}")
        self._user = user

        if not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5 stars")
        self._rating = rating

        self._comment = comment

    @property
    def review_id(self) -> int:
        return self._review_id

    @property
    # You can only review a podcast, not individual episodes
    def podcast(self) -> Podcast:
        return self._podcast

    @property
    def user(self) -> User:
        return self._user

    @property
    def rating(self) -> int:
        return self._rating

    @property
    def comment(self) -> str:
        return self._comment

    @podcast.setter
    def podcast(self, new_podcast: Podcast):
        if not isinstance(new_podcast, Podcast):
            raise TypeError("Review must be for a Podcast object.")
        self._podcast = new_podcast

    @rating.setter
    def rating(self, new_rating: int):
        if not (1 <= new_rating <= 5):
            raise TypeError("Rating must be between 1 and 5 stars")
        self._rating = new_rating

    @comment.setter
    # Comment can be empty
    def comment(self, new_comment: str):
        self._comment = new_comment.strip()

    def __repr__(self):
        return (f"<Review id: {self.review_id}. "
                f"{self.user.username.capitalize()} rated {self.podcast.title} {self._rating}/5 stars. "
                f"Comment: '{self.comment}'>")

    def __eq__(self, other):
        if not isinstance(other, Review):
            return False
        return self.review_id == other.review_id

    def __lt__(self, other):
        if not isinstance(other, Review):
            return False
        return self.rating < other.rating

    def __hash__(self):
        return hash(self.review_id)


class Playlist:
    def __init__(self, playlist_id: int, owner: User, playlist_name: str):
        if not isinstance(playlist_id, int):
            raise ValueError("Playlist id must be an integer")
        if not isinstance(owner, User):
            raise TypeError("Owner must be a User object")
        self._playlist_name = playlist_name
        if not isinstance(playlist_id, int):
            raise TypeError("playlist_id must be an integer")
        if not isinstance(playlist_name, str):
            raise TypeError("playlist_name must be a string")
        if playlist_id < 0:
            raise ValueError("playlist_id must be non-negative")
        self._playlist_id = playlist_id
        self._owner = owner
        self._username = owner.username
        self._episodes = []

    def add_episode(self, episode: Episode):
        if episode not in self._episodes:
            self._episodes.append(episode)

    def remove_episode(self, episode: Episode):
        if episode in self._episodes:
            self._episodes.remove(episode)

    @property
    def owner(self) -> User:
        return self._owner

    @property
    def playlist_name(self) -> str:
        return self._playlist_name

    @property
    def playlist_id(self) -> int:
        return self._playlist_id

    @property
    def episodes(self) -> list:
        return self._episodes
    @playlist_name.setter
    def playlist_name(self, new_name: str):
        validate_non_empty_string(new_name, "Playlist name")
        self._playlist_name = new_name.strip()

    def __repr__(self):
        return f"Playlist {self.playlist_id}: Owned by {self.owner.username}"

    def __eq__(self, other):
        if not isinstance(other, Playlist):
            return False
        return self.playlist_id == other.playlist_id

    def __hash__(self):
        return hash(self.playlist_id)

    def __lt__(self, other):
        if not isinstance(other, Playlist):
            return False
        return self.playlist_id < other.playlist_id

    pass
