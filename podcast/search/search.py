from flask import Blueprint, render_template, request, redirect, url_for
import podcast.search.services as services
import podcast.adapters.repository as repo



search_blueprint = Blueprint('search_bp', __name__)

@search_blueprint.route('/search')
def search():
        query = request.args.get('q')
        search_by = request.args.get('attribute')
        search_results = []
        if query:
            search_results = services.get_results(repo.repo_instance, query, search_by)

        page = request.args.get('page', 1, type=int)

        paged_results, num_pages = services.get_pagination(repo.repo_instance, search_results, page, 9)

        return render_template('search.html', results=paged_results, search_by=search_by, query=query,page=page, num_pages=num_pages)

