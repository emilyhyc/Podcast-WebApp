from podcast.adapters.repository import AbstractRepository

class NonExistentPageException(Exception):
    pass
class NonExistentCategoryException(Exception):
    pass


def get_all_categories(repo: AbstractRepository) -> set:
    return repo.get_all_categories()


def get_category(repo: AbstractRepository, category_id: int):
    category = repo.get_category(category_id)
    if category is None:
        raise NonExistentCategoryException
    return category


def get_podcasts_by_category(repo: AbstractRepository, category_id: int):
    return repo.get_podcasts_by_category(category_id)


def get_pagination(repository, results, page, podcasts_per_page):
    num_pages = repository.pagination(results, podcasts_per_page)
    if page < 1 or page > num_pages:
        raise NonExistentPageException("Page out of range")
    page_start = (page - 1) * podcasts_per_page
    page_end = page_start + podcasts_per_page
    return results[page_start:page_end], num_pages