import concurrent.futures
from typing import Iterator

from bballer.models.player import Player
from bballer.scrapers.PlayerPageScraper import PlayerPageScraper
from bballer.scrapers.base import Scraper


class TotalMinutesScraper(Scraper):
    def get_content(self):
        return self.get_player_urls()

    def __init__(self, year: int):
        url = f"https://www.basketball-reference.com/leagues/NBA_{year}_totals.html"
        super().__init__(url)

    def get_player_urls(self):
        cells = self._parsed.find_all("td", {"data-stat": "player"})
        return ["https://www.basketball-reference.com" + cell.find_next("a").attrs["href"] for cell in cells]


class BulkScraper:
    def __init__(self, urls):
        self._urls = urls

    def scrape_all(self, _max: int = None) -> Iterator[Player]:
        urls = list(set(self._urls[0:_max] if _max else self._urls))
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for player in executor.map(lambda u: PlayerPageScraper(u).get_content(), urls):
                yield player
