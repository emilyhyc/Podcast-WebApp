import pytest

from flask import session
from podcast import create_app
from tests.conftest import auth


@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False

    with app.test_client() as client:
        yield client
def test_register(client):
    # Check that we retrieve the register page.
    response_code = client.get('/authentication/register').status_code
    assert response_code == 200

    # Check that we can register a user successfully, supplying a valid username and password.
    response = client.post(
        '/authentication/register',
        data={'username': 'xxx', 'password': 'Pass123'},
    )

    assert response.headers['Location'] == '/authentication/login'


@pytest.mark.parametrize(('username', 'password', 'message'), (
        ('', '', b'Username required'),
        ('tt', '', b"Username must be at least 3 characters long"),
        ('test', '', b'Password required'),
        ('test', 'test', b'Your password must contain at least one upper case letter, one lowercase letter, and one digit'),
        ('xxx', 'Pass123', b'Username is already taken')
))


def test_register_with_invalid_input(client, username, password, message):
    client.post(
        '/authentication/register',
        data={'username': 'xxx', 'password': 'Pass123'},
    )

    response = client.post(
        '/authentication/register',
        data={'username': username, 'password': password},
    )

    # check if invalid string of username and password triggers corresponding error messages
    assert message in response.data


def test_login(client, auth):
    client.post(
        '/authentication/register',
        data={'username': 'xxx', 'password': 'Pass123'},
    )

    response = auth.login(username='xxx', password='Pass123')

    # check if login redirects successfully
    assert response.status_code == 302
    assert response.headers['Location'] == '/authentication/redirect_login'

    response = client.get('/')
    assert session['username'] == 'xxx'


def test_index(client):
    # check that we can retrieve the home page.
    response = client.get('/')
    assert response.status_code == 200
    assert b'Home' in response.data


def test_login_required_to_review(client):
    # check redirect to login if user have not done so
    response = client.post('/categories1/review/1')
    assert response.headers['Location'] == '/authentication/login'


def test_logout(client, auth):
    # check successful log out
    client.post(
        '/authentication/register',
        data={'username': 'xxx', 'password': 'Pass123'},
    )

    auth.login(username='xxx', password='Pass123')

    auth.logout()
    assert 'username' not in session


def test_review(client, auth):
    client.post(
        '/authentication/register',
        data={'username': 'xxx', 'password': 'Pass123'},
    )

    auth.login(username='xxx', password='Pass123')

    # Check that we can retrieve the comment page.
    client.get('/categories1/review/1')

    response = client.post(
        '/categories1/review/1',
        data={'rating': '5', 'comment': 'lovely podcast'}
    )
    print("data: ", response.data)

    # check correct review comment has been passed by the user
    assert b'xxx' in response.data
    assert b'lovely podcast' in response.data

def test_playlist_view_add_remove(client, auth):
    client.post(
        '/authentication/register',
        data={'username': 'xxx', 'password': 'Pass123'},
    )
    auth.login(username='xxx', password='Pass123')

    # view playlist
    response = client.get('/view_playlist')
    assert response.status_code == 200

    # add and redirects to playlist
    episode_id = 1
    response = client.post(f'/add_to_playlist/{episode_id}')
    assert response.status_code == 302
    assert response.location.endswith('/view_playlist')
    response = client.get('/view_playlist')
    assert response.status_code == 200

    # remove and redirect to playlist
    response = client.post(f'/remove_episode/{episode_id}')
    assert response.status_code == 302
    assert response.location.endswith('/view_playlist')
    response = client.get('/view_playlist')
    assert response.status_code == 200

    # add entire podcast and redirect to playlist
    podcast_id = 1
    response = client.post(f'/add_podcast_episodes/{podcast_id}')
    assert response.status_code == 302
    assert response.location.endswith('/view_playlist')
    response = client.get('/view_playlist')
    assert response.status_code == 200