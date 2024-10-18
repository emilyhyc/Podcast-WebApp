from flask import Blueprint, render_template, abort, request
from podcast.adapters.memory_repository import MemoryRepository
import podcast.categories.services as services
import podcast.adapters.repository as repo


categories_blueprint = Blueprint('categories_bp', __name__)
#repository = MemoryRepository()

@categories_blueprint.route('/categories', methods=['GET'])
def categories():
    category_set = sorted(services.get_all_categories(repo.repo_instance))
    return render_template('categories.html', categories=category_set)
    # return a list of all the categories available.


@categories_blueprint.route('/categories<int:category_id>', methods=['GET'])
def category_detail(category_id):
    # Find the category by ID using repo
    category = services.get_category(repo.repo_instance,category_id)
    if category is None:
        abort(404)

    # using memory repo, get all podcasts by specific category
    podcasts_with_category = sorted(services.get_podcasts_by_category(repo.repo_instance, category_id))

    page = request.args.get('page', 1, type=int)

    paged_results, num_pages = services.get_pagination(repo.repo_instance, podcasts_with_category, page, 9)

    return render_template('category_detail.html',
                           category=category,
                           category_id=category_id,
                           podcasts=paged_results,page=page,num_pages=num_pages)