from flask import Blueprint, render_template, request, session, abort
import podcast.review.services as services
from podcast.adapters.memory_repository import MemoryRepository
from podcast.authentication.authentication import login_required
from podcast.domainmodel.model import User
import podcast.adapters.repository as repo

review_blueprint = Blueprint('review_bp', __name__)
#repository = MemoryRepository()


@review_blueprint.route('/<previous_url>/review/<int:podcast_id>', methods=['GET', 'POST'])
@login_required
def review(previous_url, podcast_id):
    #username = session['user_name']

    # #dummy user for testing
    # user = User(1, "username", "password")
    # services.add_user(user, repo.repo_instance)
    # username = "username"

    username = session["username"]
    error = None
    comment = ""

    try:
        selected_podcast = services.get_podcast(podcast_id, repo.repo_instance)
    except services.NonExistentPodcastException:
        abort(404)

    if request.method == 'POST':
        rating = (request.form.get('rating'))
        comment = str(request.form.get('comment', ''))
        if len(comment) > 500:
            error = f"Error: Comment must be less than 500 characters."
        else:
            try:
                rating = int(rating)
                services.add_review(repo.repo_instance, selected_podcast, username, rating, comment)
                comment = ""
            except:
                error = "Error: Rating must be between 1 and 5."
    all_reviews = list(reversed(services.get_all_reviews_by_podcast(podcast_id, repo.repo_instance)))

    page = request.args.get('page', 1, type=int)

    paged_results, num_pages = services.get_pagination(repo.repo_instance, all_reviews, page, 6)

    return render_template('review.html',
                           podcast=selected_podcast,
                           all_reviews=paged_results,
                           error=error,
                           previous=previous_url, comment=comment, page=page,num_pages=num_pages)
