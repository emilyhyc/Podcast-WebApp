import podcast.playlist.services as services
from flask import Blueprint, render_template, request, session, redirect, url_for
# from podcast.adapters.memory_repository import MemoryRepository
from podcast.authentication.authentication import login_required
import podcast.adapters.repository as repo # new implementation of repo.


playlist_blueprint = Blueprint('playlist_bp', __name__)
# repository = MemoryRepository() instead of making a new repo every blueprint, ive implemented a global repo.
# #Use repo.repo_instance instead of repository (see comment below)


@playlist_blueprint.route('/view_playlist', methods=['GET'])
@login_required
def view_playlist():
    username = session["username"]
    user_object = services.get_user_object(repo.repo_instance, username)
    playlist = services.get_playlist_by_user(repo.repo_instance, user_object)
    if playlist is None:
        services.set_playlist(repo.repo_instance, user_object)
        playlist = services.get_playlist(repo.repo_instance, user_object)

    episodes_in_playlist = playlist.episodes
    print(episodes_in_playlist)
    if playlist.owner != user_object:
        return "You do not have permission to access this playlist.", 403
    for episode in episodes_in_playlist:
        # made a temp place for the podcast details instead
        episode.podcast_details = services.get_podcast(repo.repo_instance, episode.podcast_id)

    page = request.args.get('page', 1, type=int)
    paged_results, num_pages = services.get_pagination(repo.repo_instance, episodes_in_playlist, page, 8)

    return render_template('playlist.html', playlist=playlist, episodes=paged_results, page=page, num_pages=num_pages)


@playlist_blueprint.route('/add_to_playlist/<int:episode_id>', methods=['GET', 'POST'])
@login_required
def add_to_playlist(episode_id):
    username = session["username"]
    user_object = services.get_user_object(repo.repo_instance, username)
    services.set_playlist(repo.repo_instance, user_object)
    episode = services.get_episode(repo.repo_instance, episode_id)
    user_playlist = services.get_playlist(repo.repo_instance, user_object)

    services.add_episode_to_playlist(repo.repo_instance, episode, user_object)

    return redirect(url_for('playlist_bp.view_playlist'))


@playlist_blueprint.route('/remove_episode/<int:episode_id>', methods=['GET', 'POST'])
@login_required
def remove_episode(episode_id):
    username = session["username"]
    user = services.get_user_object(repo.repo_instance, username)
    episode = services.get_episode(repo.repo_instance, episode_id)

    if not episode:
        return redirect(url_for('view_playlist', error="Episode not found"))


    try:
        services.remove_episode_from_playlist(repo.repo_instance, episode, user)
        return redirect(url_for('playlist_bp.view_playlist'))
    except services.NonExistentPlaylistException:
        return redirect(url_for('playlist_bp.view_playlist'))

@playlist_blueprint.route('/add_podcast_episodes/<int:podcast_id>', methods=['POST'])
@login_required
def add_podcast_episodes_to_playlist(podcast_id):
    username = session["username"]
    user_object = services.get_user_object(repo.repo_instance, username)
    services.set_playlist(repo.repo_instance, user_object)
    podcast = services.get_podcast(repo.repo_instance, podcast_id)
    if not podcast:
        return redirect(url_for('playlist_bp.view_playlist', error="Podcast not found"))

    services.add_podcast_to_playlist(repo.repo_instance, podcast, user_object)

    return redirect(url_for('playlist_bp.view_playlist'))