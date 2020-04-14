from functools import lru_cache
from typing import Optional, Iterator

from bballer.models.player import Player
from bballer.scrapers.PlayerPageScraper import PlayerPageScraper
from bballer.scrapers.Search import Search
from bballer.scrapers.misc import TotalMinutesScraper, BulkScraper


@lru_cache(maxsize=10)
def get_by_name(name: str) -> Optional[Player]:
    result = Search.search_players(name)
    if not len(result):
        return None
    url = result[0][-1]
    return PlayerPageScraper(url).player()


@lru_cache(maxsize=10)
def all_in_season(season: int) -> Iterator[Player]:
    url_scraper = TotalMinutesScraper(season)
    urls = url_scraper.get_player_urls()
    scraper = BulkScraper(urls)
    return scraper.scrape_all()


@lru_cache(maxsize=10)
def search(term: str):
    return Search.search_players(term)


@lru_cache(maxsize=10)
def get_by_url(url: str) -> Player:
    return PlayerPageScraper(url).player()


@lru_cache(maxsize=10)
def get_by_id(_id: str) -> Player:
    url = f"https://www.basketball-reference.com/players/{_id[0]}/{_id}.html"
    return PlayerPageScraper(url).player()
