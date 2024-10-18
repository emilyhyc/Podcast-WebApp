import os
import csv
import re
from datetime import datetime
from podcast.domainmodel.model import Episode, Podcast, Author, Category


class CSVDataReader:
    def __init__(self, podcast_filename, episode_filename):
        self._podcast_file = podcast_filename
        self._episode_file = episode_filename
        self._podcast_list = []
        self._episode_list = []
        self._authors = set()
        self._categories = set()
        self._author_id = 1
        self._category_id = 1
    def podcasts_csv(self):
        #id (0),title (1),image (2),description (3),language (4),categories (5),
        #website (6),author (7),itunes_id (8)

        with open(self._podcast_file, 'r', encoding='utf-8-sig', errors='replace', newline='') as f:
            reader = csv.reader(f, delimiter=',')
            next(reader) #skippin the first row as it just initialises the CSV
            for row in reader:
                if len(row) < 9:  # Row needs 9 values.
                    print(f"Podcast id {row[0]} has less than 9 columns")
                    continue
                try:
                    author_name = row[7]
                    if not author_name:
                        author_object = self.create_author("Anonymous")
                    else:
                        author_object = self.create_author(author_name)

                    new_podcast = Podcast(
                        podcast_id=int(row[0]),
                        author=author_object,
                        title=row[1],
                        image=row[2],
                        description=row[3],
                        website=row[6],
                        itunes_id=int(row[8]),
                        language=row[4]
                    )

                    categories_multiple = row[5]
                    if categories_multiple:
                        categories = [category.strip() for category in categories_multiple.split('|')]
                        for category_name in categories:
                            category = self.create_category(category_name)
                            new_podcast.add_category(category)

                    self._podcast_list.append(new_podcast)


                except ValueError as e:
                    print(f"{e} error in Podcast id {row[0]}")
    def episodes_csv(self):
        if len(self._podcast_list) == 0:
            print("empty podcast_list")
            return
        #id (0),podcast_id (1),title (2),audio (3),audio_length (4),description (5),pub_date (6)
        with open(self._episode_file, 'r') as f:
            reader = csv.reader(f, delimiter=',')
            next(reader)
            for row in reader:
                parent_podcast_id = int(row[1])
                parent_podcast_ep = None
                for podcast in self._podcast_list:
                    if int(podcast.id) == int(parent_podcast_id):
                        parent_podcast_ep = podcast
                        break
                if parent_podcast_ep is None:
                    print(f"Podcast id {parent_podcast_id} doesnt exist for episode id {row[0]}")
                    continue

                pub_date_str = row[6]
                if pub_date_str:
                    if pub_date_str.endswith('00'):
                        pub_date_str = pub_date_str[:-3] + '+0000'

                    try:
                        pub_date = datetime.strptime(pub_date_str, '%Y-%m-%d %H:%M:%S%z')
                    except ValueError as e:
                        print(f"Error parsing pub_date {pub_date_str}: {e}")
                        pub_date = None
                else:
                    pub_date = None

                #remove html tags before and after some descriptions
                description = row[5]
                description = re.sub(r'^<[^>]+>', '', description)
                description = re.sub(r'<[^>]+>$', '', description)
                description = description.strip()

                if pub_date is not None:
                    new_episode = Episode(
                        episode_id=int(row[0]),
                        podcast_id=parent_podcast_id,
                        title=row[2],
                        audio_link=row[3],
                        audio_length=int(row[4]),
                        description=description,
                        pub_date=pub_date
                    )
                    self._episode_list.append(new_episode)
                else:
                    print(f"Episode id {row[0]} has an invalid date")

    def create_author(self, author_name: str) -> Author:
        for author in self._authors:
            if author.name == author_name:
                return author

        new_author = Author(author_id=self._author_id, name=author_name)
        self._authors.add(new_author)
        self._author_id += 1
        return new_author

    def create_category(self, category_name: str) -> Category:
        for category in self._categories:
            if category.name == category_name:
                return category
        new_category = Category(category_id=self._category_id, name=category_name)
        self._categories.add(new_category)
        self._category_id += 1
        return new_category

    @property
    def podcast_list(self):
        return self._podcast_list

    @property
    def episode_list(self):
        return self._episode_list

    @property
    def categories(self):
        return self._categories

    @property
    def authors(self) -> set:
        return self._authors
