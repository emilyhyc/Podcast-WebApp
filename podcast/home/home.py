from flask import Blueprint, render_template, session
import podcast.home.services as services
import podcast.adapters.repository as repo

home_blueprint = Blueprint('home_bp', __name__)


@home_blueprint.route('/', methods=['GET'])
def home():
    username = session.get('username')
    print("login:", username)

    # Check if the user exists in the session
    if username:
        user_exists = services.get_user(repo.repo_instance, username)
        print("service check:", user_exists)
    else:
        user_exists = False

    # If no user, clear the session and reset the repository session
    if not user_exists:
        session.clear()


    num_podcasts = services.get_number_of_podcasts(repo.repo_instance)
    num_episodes = services.get_number_of_episodes(repo.repo_instance)
    return render_template('home.html', num_podcasts=num_podcasts, num_episodes=num_episodes)
