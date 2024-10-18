from podcast.adapters.repository import AbstractRepository

def get_all_podcasts_sorted(repo: AbstractRepository):
    all_podcasts = repo.get_all_podcasts()
    # dont need to use lambda due to __lt__ method in Podcast class
    x = sorted(all_podcasts)
    return x

def get_podcasts_in_page(repository, page, podcasts_per_page):
    all_podcasts = get_all_podcasts_sorted(repository)
    start = (page - 1) *podcasts_per_page
    end = start + podcasts_per_page

    return all_podcasts[start:end]

def get_num_pages(repository, podcasts_per_page):
    all_podcasts = get_all_podcasts_sorted(repository)
    return repository.pagination(all_podcasts, podcasts_per_page)