from flask import Blueprint, render_template, request
from podcast.adapters.memory_repository import MemoryRepository
import podcast.browse.services as services
import podcast.adapters.repository as repo

browse_blueprint = Blueprint('browse_bp', __name__)

#repository = MemoryRepository()


@browse_blueprint.route('/browse<int:page>', methods=['GET'])
def browse(page):
    podcasts_per_page = 9
    podcasts = services.get_podcasts_in_page(repo.repo_instance, page, podcasts_per_page)
    num_pages = services.get_num_pages(repo.repo_instance, podcasts_per_page)

    return render_template('browse.html',
                           podcasts=podcasts,
                           page=page,
                           num_pages=num_pages)