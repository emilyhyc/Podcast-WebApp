from podcast.adapters.repository import AbstractRepository

class NonExistentPageException(Exception):
    pass
def get_all_podcasts(repo: AbstractRepository):
    return repo.get_all_podcasts()


def get_podcasts_in_page(repo: AbstractRepository, page, podcasts_per_page):
    all_podcasts = get_all_podcasts(repo)
    start = (page - 1) * podcasts_per_page
    end = start + podcasts_per_page

    return all_podcasts[start:end]

def get_pagination(repository, results, page, podcasts_per_page):
    num_pages = repository.pagination(results, podcasts_per_page)
    if page < 1 or page > num_pages:
        raise NonExistentPageException("Page out of range")
    page_start = (page - 1) * podcasts_per_page
    page_end = page_start + podcasts_per_page
    return results[page_start:page_end], num_pages

def get_results(repository, query, search_by):
    query = query.strip().lower()
    if search_by=='title':
        search_results = repository.search_podcast_by_title(query)
    elif search_by=='category':
        search_results = repository.search_podcast_by_category(query)
    elif search_by=='author':
        search_results = repository.search_podcast_by_author(query)
    else:
        return []
    return sorted(search_results)
