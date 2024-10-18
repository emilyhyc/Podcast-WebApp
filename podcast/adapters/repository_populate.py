import os, csv
from pathlib2 import Path

from podcast.adapters.repository import AbstractRepository
from podcast.adapters.datareader.csvdatareader import CSVDataReader


def populate(data_path: Path, repo: AbstractRepository, database_mode: bool):
    dir_name = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.'))
    podcast_filename = os.path.join(dir_name, str(Path(data_path) / "podcasts.csv"))
    episode_filename = os.path.join(dir_name, str(Path(data_path) / "episodes.csv"))

    reader = CSVDataReader(podcast_filename, episode_filename)

    reader.podcasts_csv()
    reader.episodes_csv()

    authors = reader.authors
    podcasts = reader.podcast_list
    categories = reader.categories
    episodes = reader.episode_list

    repo.add_multiple_authors(authors)
    repo.add_multiple_categories(categories)
    repo.add_multiple_podcasts(podcasts)
    repo.add_multiple_episodes(episodes)
