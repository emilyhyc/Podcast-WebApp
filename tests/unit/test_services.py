import pytest
from werkzeug.security import check_password_hash

from podcast.adapters.memory_repository import MemoryRepository
from podcast.domainmodel.model import User, Review, Playlist
from podcast.podcasts.services import NonExistentPodcastException, NonExistentEpisodeException, NonExistentPageException

from podcast.search import services as search_services
from podcast.review import services as review_services
from podcast.podcasts import services as podcast_services
from podcast.home import services as home_services
from podcast.categories import services as category_services
from podcast.browse import services as browse_services
from podcast.playlist import services as playlist_services
from podcast.authentication import services as auth_services

from podcast.playlist.services import NonExistentPlaylistException
from podcast.playlist.services import NonExistentPageException
from podcast.categories.services import NonExistentPageException
from podcast.search.services import NonExistentPageException
from podcast.authentication.services import NameNotUniqueException
from podcast.authentication.services import UnregisteredUserException
from podcast.authentication.services import UnauthenticatedUserException



repository = MemoryRepository()
all_podcasts = repository.get_all_podcasts()

dummy_user = User("user231", "dummy")
repository.add_user(dummy_user)

#for playlist_services testing
test_episode = repository.get_episode(1)
test_episode2 = repository.get_episode(2)
test_episode3 = repository.get_episode(3)

parent_podcast = repository.get_podcast(1)
parent_podcast2 = repository.get_podcast(4)

#SEARCH
def test_search_all_podcasts():
    list = search_services.get_all_podcasts(repository)
    assert list == all_podcasts
def test_search_get_podcasts_in_page():
    podcasts = search_services.get_podcasts_in_page(repository, 1,9)
    for i in range(len(podcasts)):
        assert podcasts[i] == all_podcasts[i]

def test_search_get_results():
    podcasts = search_services.get_results(repository, "sport", "title")
    assert podcasts[0].title == "100% Sports France Bleu Champagne-Ardenne"
    assert podcasts[1].title == "1SportsTalk"
    assert podcasts[7].title == "Seton Hall Sports Poll"

def test_search_get_pagination():
    podcasts, pages = search_services.get_pagination(repository, all_podcasts, 5, 9)
    assert pages == 112
    assert podcasts[0].title == 'He Loves Me Not'
    assert podcasts[3].title == 'Supercultured: We like what we like.'
    assert podcasts[4].title == "Danish and O'Neill"
    from podcast.search.services import NonExistentPageException
    with pytest.raises(NonExistentPageException):
        podcasts, pages = search_services.get_pagination(repository, all_podcasts, 531231231, 9)


#REVIEW
def test_review_all_podcasts():
    list = search_services.get_all_podcasts(repository)
    assert list == all_podcasts


def test_review_get_podcast():
    podcast = review_services.get_podcast(1, repository)
    assert (podcast.title) == 'D-Hour Radio Network'
    podcast = review_services.get_podcast(6, repository)
    assert (podcast.title) == 'Mike Safo'


def test_review_get_all_reviews_by_podcast():
    r = review_services.get_all_reviews_by_podcast(1, repository)
    assert len(r) == 0
    review1 = review_services.add_review(repository, all_podcasts[0], "user231", 5, "")
    r = review_services.get_all_reviews_by_podcast(1, repository)
    assert len(r) == 1
    repository.remove_review(review1)


def test_add_user():
    dummy_user_2 = User("dummy2", "user321")
    review_services.add_user(dummy_user_2, repository)
    user_list = repository.get_all_user()
    assert dummy_user_2 in user_list
    repository.remove_user(dummy_user_2)

def test_review_get_pagination():
    x=review_services.add_review(repository, all_podcasts[0], "user231", 5, "")
    y=review_services.add_review(repository, all_podcasts[0], "user231", 4, "hi")
    z=review_services.add_review(repository, all_podcasts[0], "user231", 3, "comment")
    reviews = repository.get_all_reviews_by_podcast(1)
    print(reviews)
    all_reviews, num_pages = review_services.get_pagination(repository, reviews, 1, 6)
    assert num_pages == 1
    assert len(all_reviews) == 3
    assert all_reviews[0].rating == 5
    assert all_reviews[1].comment == "hi"
    assert all_reviews[2].comment == "comment"
    from podcast.review.services import NonExistentPageException
    try:
        review_services.get_pagination(repository, reviews, 77777, 6)
    except NonExistentPageException:
        assert True
    repository.remove_review(x)
    repository.remove_review(y)
    repository.remove_review(z)



def test_add_review():
    r = review_services.add_review(repository, all_podcasts[0], "user231", 5, "lol")
    reviews = review_services.get_all_reviews_by_podcast(all_podcasts[0].id, repository)
    assert len(reviews) == 1
    assert reviews[0].rating == 5
    assert reviews[0].comment == "lol"
    assert reviews[0].user.username == "user231"
    repository.remove_review(r)



#PODCASTS

def test_podcasts_get_podcast():
    podcast = podcast_services.get_podcast(1, repository)
    assert podcast.id == 1
    assert podcast.title == 'D-Hour Radio Network'

    with pytest.raises(NonExistentPodcastException):
        podcast_services.get_podcast(2363000, repository)

def test_podcasts_get_all_podcasts():
    podcasts = podcast_services.get_all_podcasts(repository)
    assert len(podcasts) == 1000
    assert podcasts[0].title == 'D-Hour Radio Network'

def test_get_episodes_by_podcast_id():
    episodes = podcast_services.get_episodes_by_podcast_id(1, repository)
    assert len(episodes) == 10
    assert episodes[0].title == "Say It! Radio"

def test_get_episode_by_id():
    episode = podcast_services.get_episode_by_id(2, repository)
    assert episode.episode_id == 2
    assert episode.title == 'Finding yourself in the character by justifying your actions'

    try:
        podcast_services.get_episode_by_id(31892381273012, repository)
    except NonExistentEpisodeException:
        assert True

def test_podcasts_get_pagination():
    episodes, num_pages = podcast_services.get_pagination(1, repository, 1, 9)
    assert len(episodes) == 9
    assert num_pages == 2
    from podcast.podcasts.services import NonExistentPageException
    with pytest.raises(NonExistentPageException):
        episodes, num_pages = podcast_services.get_pagination(1, repository, 21927191, 1)


def test_podcasts_get_average_rating():
    print(repository.get_all_reviews())
    print("yas")
    avg = podcast_services.get_average_rating(1, repository)
    assert avg == "N/A"
    review1 = review_services.add_review(repository, all_podcasts[0], "user231", 5, "lol")
    review2 = review_services.add_review(repository, all_podcasts[0], "user231", 3, "lol")
    avg = podcast_services.get_average_rating(1, repository)
    assert avg == 4.0
    repository.remove_review(review1)
    repository.remove_review(review2)

def test_podcasts_add_user():
    user = User("username", "password1888")
    podcast_services.add_user(user, repository)

    user_obj = repository.get_user_object("username")
    assert user_obj.username == "username"
    repository.remove_user(user)


#HOME

def test_home_get_number_of_episodes():
    num_episodes = home_services.get_number_of_episodes(repository)
    assert num_episodes == 5633

def test_home_get_number_of_podcasts():
    num_pod = home_services.get_number_of_podcasts(repository)
    assert num_pod == 1000


#CATEGORY
def test_get_all_categories():
    categories = category_services.get_all_categories(repository)
    categories = list(categories)
    assert len(categories) == 65
    assert categories[1].name == 'Personal Journals'
    assert categories[8].name == 'Amateur'

def test_get_category():
    category = category_services.get_category(repository, 1)
    assert category.name == 'Society & Culture'
    category = category_services.get_category(repository, 8)
    assert category.name == 'Christianity'

def test_get_podcasts_by_category():
    podcasts_cat_list = category_services.get_podcasts_by_category(repository, 1)
    assert podcasts_cat_list[0].title == 'D-Hour Radio Network'
    assert podcasts_cat_list[8].title == 'Kingdom Awakening with R. Loren Sandford'
    assert podcasts_cat_list[10].title == 'December 26er Podcast'

def test_cat_pagination():
    podcasts_cat_list = repository.get_podcasts_by_category(1) # 'Society & Culture'
    podcasts, pages = category_services.get_pagination(repository, podcasts_cat_list, 5, 9)
    assert pages == 17
    assert podcasts[0].title == 'Merry Podcast' #first podcast on page 5
    assert podcasts[3].title == 'Essay Questions'  #fourth podcast on page 5
    assert podcasts[4].title == 'MurderCast'
    from podcast.categories.services import NonExistentPageException
    with pytest.raises(NonExistentPageException):
        podcasts, pages = category_services.get_pagination(repository, podcasts_cat_list, 11111, 9)


#BROWSE

def test_get_all_podcasts_sorted():
    sorted_podcasts = browse_services.get_all_podcasts_sorted(repository)
    assert sorted_podcasts[0].title == '#AroundThePoolTable'
    assert sorted_podcasts[1].title == '#THE 51%'
    assert sorted_podcasts[10].title == '30 Minute Additions'


def test_get_podcasts_in_page():
    podcasts = browse_services.get_podcasts_in_page(repository, 5, 9)
    assert podcasts[1].title == 'After Party With Aubrey and Kylie'
    podcasts = browse_services.get_podcasts_in_page(repository, 2, 9)
    assert podcasts[1].title == '30 Minute Additions'
    podcasts = browse_services.get_podcasts_in_page(repository, 1, 9)
    assert podcasts[0].title == '#AroundThePoolTable'
    assert podcasts[1].title == '#THE 51%'

def test_get_num_pages():
    num_pages = browse_services.get_num_pages(repository, 9)
    assert num_pages == 112
    num_pages = browse_services.get_num_pages(repository, 10)
    assert num_pages == 100


#PLAYLIST
def test_get_user_object():
    user = playlist_services.get_user_object(repository, "user231")
    assert user == User("user231", "dummy")


def test_check_for_playlist():
    dummy_tester = User("dummy_tester", "user231")
    assert playlist_services.check_for_playlist(repository, dummy_tester) == False
    playlist_services.set_playlist(repository, dummy_tester)
    assert playlist_services.check_for_playlist(repository, dummy_tester) == True


def test_set_playlist():
    dummy_tester = User("dummy_tester", "user231")
    if not playlist_services.check_for_playlist(repository, dummy_tester):
        with pytest.raises(ValueError, match="No playlist has been set."):
            playlist_services.get_playlist(repository, dummy_tester)
        playlist_services.set_playlist(repository, dummy_tester)

    assert playlist_services.get_playlist(repository, dummy_tester) is not None
    assert type(playlist_services.get_playlist(repository, dummy_tester)) == Playlist


def test_get_playlist():
    dummy_tester = User( "dummy_tester", "user231")
    playlist_services.set_playlist(repository, dummy_tester)

    playlist = playlist_services.get_playlist(repository, dummy_tester)
    assert playlist.playlist_id == 1
    assert playlist._owner == dummy_tester
    assert playlist._playlist_name == "dummy_tester's Playlist"


def test_add_episode_to_playlist():
    dummy_tester = User("dummy_tester", "user231")
    playlist_services.set_playlist(repository, dummy_tester)
    playlist_services.add_episode_to_playlist(repository, test_episode, dummy_tester)
    playlist = playlist_services.get_playlist(repository, dummy_tester)

    list_of_eps = playlist.episodes
    assert list_of_eps[0].title == 'The Mandarian Orange Show Episode 74- Bad Hammer Time, or: 30 Day MoviePass Challenge Part 3'
    assert list_of_eps[0].episode_id == 1
    assert len(list_of_eps) == 1


def test_remove_episode_from_playlist():
    dummy_tester = User("dummy_tester", "user231")
    playlist_services.set_playlist(repository, dummy_tester)
    playlist_services.add_episode_to_playlist(repository, test_episode, dummy_tester)
    playlist = playlist_services.get_playlist(repository, dummy_tester)

    list_of_eps = playlist.episodes
    assert len(list_of_eps) == 1
    playlist_services.remove_episode_from_playlist(repository, test_episode, dummy_tester)
    assert len(list_of_eps) == 0

def test_add_podcast_to_playlist():
    dummy_tester = User("dummy_tester", "user231")
    playlist_services.set_playlist(repository, dummy_tester)
    playlist = playlist_services.get_playlist(repository, dummy_tester)
    list_of_eps = playlist.episodes

    assert len(list_of_eps) == 0

    playlist_services.add_podcast_to_playlist(repository, parent_podcast, dummy_tester)
    assert len(list_of_eps) == 10

    playlist_services.add_podcast_to_playlist(repository, parent_podcast2, dummy_tester)
    assert len(list_of_eps) == 16



def test_get_playlist_by_user():
    dummy_tester = User("dummy_tester", "user231")
    dummy_tester2 = User("dummy_tester2", "user231")

    playlist_services.set_playlist(repository, dummy_tester)
    playlist_services.set_playlist(repository, dummy_tester2)

    playlist1 = playlist_services.get_playlist_by_user(repository, dummy_tester)
    playlist2 = playlist_services.get_playlist_by_user(repository, dummy_tester2)

    assert playlist1.playlist_id == 1
    assert playlist1.playlist_name == "dummy_tester's Playlist"
    assert playlist1.owner == User("dummy_tester", "user231")

    assert playlist2.playlist_id == 2
    assert playlist2.playlist_name == "dummy_tester2's Playlist"
    assert playlist2.owner == User("dummy_tester2", "user231")


def test_get_podcast():
    podcast = playlist_services.get_podcast(repository, 1)
    assert podcast.id == 1
    assert podcast.title == "D-Hour Radio Network"
    assert podcast.author.id == 1
    assert podcast.author.name == "D Hour Radio Network"

def test_get_episode():
    episode = playlist_services.get_episode(repository, 1)
    assert episode.episode_id == 1
    assert episode.title == "The Mandarian Orange Show Episode 74- Bad Hammer Time, or: 30 Day MoviePass Challenge Part 3"
    assert episode.podcast_id == 14

def test_playlist_get_pagination():
    user0 = User("123", "pass")
    playlist = playlist_services.set_playlist(repository, user0)
    playlist_services.add_episode_to_playlist(repository, test_episode, user0)
    playlist_services.add_episode_to_playlist(repository, test_episode2, user0)
    playlist_services.add_podcast_to_playlist(repository, parent_podcast, user0)

    playlist_object = playlist_services.get_playlist(repository, user0)
    playlist_list_of_eps = playlist_object.episodes

    podcasts, pages = search_services.get_pagination(repository, playlist_list_of_eps, 1, 9)
    assert pages == 2
    assert playlist_list_of_eps[0].title == 'The Mandarian Orange Show Episode 74- Bad Hammer Time, or: 30 Day MoviePass ' 'Challenge Part 3'
    assert playlist_list_of_eps[3].title == 'Say It! Radio'
    assert playlist_list_of_eps[6].title == 'Say It! Radio (Alter Ego Friday) Feat...Paul Mabon'
    from podcast.playlist.services import NonExistentPageException
    with pytest.raises(NonExistentPageException):
        podcasts, pages = playlist_services.get_pagination(repository, playlist_list_of_eps, 1111, 9)

# AUTHENTICATION
def test_can_add_user():
    username1 = "dummyuser1"
    password1 = "Dummypass1"

    auth_services.add_user(username1, password1, repository)
    added_user = auth_services.get_user(username1, password1, repository)

    assert added_user["username"] == username1
    assert check_password_hash(added_user['password'], password1)

def test_cannot_add_existing_user():
    username1 = "user231"
    password1 = "dummy"

    with pytest.raises(NameNotUniqueException):
        auth_services.add_user(username1, password1, repository)

def test_auth_valid_credentials():
    username2 = "dummyuser2"
    password2 = "Dummypass2"

    auth_services.add_user(username2, password2, repository)

    try:
        auth_services.auth_user(username2, password2, repository)
    except UnauthenticatedUserException:
        assert False

def test_auth_invalid_credentials():
    username3 = "dummyuser3"
    password3 = "Dummypass3"

    auth_services.add_user(username3, password3, repository)

    with pytest.raises(UnregisteredUserException):
        auth_services.auth_user("dummyuser4", 'Dummypass3', repository)

    with pytest.raises(UnauthenticatedUserException):
        auth_services.auth_user(username3, 'zyx123', repository)






