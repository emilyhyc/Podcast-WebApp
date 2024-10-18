import random
from typing import Iterable
from podcast.adapters.repository import AbstractRepository
from podcast.domainmodel.model import Episode, Podcast, Author, Category


def get_random_episode(quantity, repo: AbstractRepository):
    episode_count = repo.get_number_of_episodes()
    if quantity >= episode_count:
        quantity = episode_count - 1

    random_episode_ids = random.sample(range(1, episode_count), quantity)
    episodes = repo.get_episodes_by_id(random_episode_ids)
    return episodes_dictionary(episodes)

def get_random_podcast(quantity, repo: AbstractRepository):
    podcast_count = repo.get_number_of_podcasts()
    if quantity >= podcast_count:
        quantity = podcast_count - 1

    random_podcast_ids = random.sample(range(1, podcast_count), quantity)
    podcasts = repo.get_podcasts_by_id(random_podcast_ids)
    return podcasts_dictionary(podcasts)

def episode_dictionary(episode: Episode):
    episode_dict = {
        'episode_id': episode.episode_id,
        'parent_podcast': episode.parent_podcast,
        'title': episode.title,
        'audio_link': episode.audio_link,
        'audio_length': episode.audio_length,
        'description': episode.description,
        'pub_date': episode.pub_date,
    }
    return episode_dict


def episodes_dictionary(episodes: Iterable[Episode]):
    return [episode_dictionary(episode) for episode in episodes]

def podcast_dictionary(podcast: Podcast):
    podcast_dict = {
        'podcast_id': podcast.id,
        'author': podcast.author,
        'title': podcast.title,
        'image': podcast.image,
        'description': podcast.description,
        'language': podcast.language,
        'website': podcast.website,
        'itunes_id': podcast.itunes_id,
        'categories': podcast.categories,
        'episodes': podcast.episodes
    }
    return podcast_dict


def podcasts_dictionary(podcasts: Iterable[Podcast]):
    return [podcast_dictionary(podcast) for podcast in podcasts]