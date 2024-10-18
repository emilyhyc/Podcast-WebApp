from flask import Blueprint, render_template, abort, request, url_for
from podcast.adapters.memory_repository import MemoryRepository
import podcast.podcasts.services as services
import podcast.adapters.repository as repo


podcasts_blueprint = Blueprint('podcasts_bp', __name__)

#repository = MemoryRepository()

# unused for podcast.html (will keep if needed later)
# @podcasts_blueprint.route('/podcasts', methods=['GET'])
# def show_podcasts():
    # list_of_podcasts = services.get_all_podcasts(repository)
    # return render_template('podcasts.html', podcasts=list_of_podcasts)

# show description of podcast + episodes of podcast
@podcasts_blueprint.route('/<previous_url>/description/<int:podcast_id>', methods=['GET'])
def show_description(previous_url, podcast_id):

    try:
        selected_podcast = services.get_podcast(podcast_id, repo.repo_instance)
    except services.NonExistentPodcastException:
        abort(404)

    page = request.args.get('page', 1, int)
    try:
        episodes, num_pages = services.get_pagination(podcast_id, repo.repo_instance, page, 5)
    except services.NonExistentPodcastException:
        abort(404)

    #handelling previous page url.
    if previous_url == "search":
        search_query = request.args.get('q', '')
        print(f"search_query {search_query}")
        search_attribute = request.args.get('attribute', 'title')
        page = request.args.get('page', 1, int)

        previous_url = f"search?attribute={search_attribute}&q={search_query}&page={page}"

    avg_rating = services.get_average_rating(podcast_id, repo.repo_instance)

    return render_template(
        template_name_or_list="/podcastDescription.html",
        podcast=selected_podcast,
        episodes=episodes,
        page=page,
        num_pages=num_pages,
        avg_rating = avg_rating,
        previous=previous_url
    )


# accessing episodes
@podcasts_blueprint.route('/episode/<int:episode_id>', methods=['GET'])
def show_episode(episode_id):
    try:
        selected_episode = services.get_episode_by_id(episode_id, repo.repo_instance)
    except services.NonExistentEpisodeException:
        abort(404)

    try:
        podcast = services.get_podcast(selected_episode.podcast_id, repo.repo_instance)
    except services.NonExistentPodcastException:
        abort(404)

    return render_template(
        'episodeDescription.html', episode=selected_episode, podcast=podcast
    )
