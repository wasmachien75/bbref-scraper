from typing import List, Tuple

from bballer.scrapers.base import Scraper


class SearchPageScraper(Scraper):

    def __init__(self, url: str):
        super().__init__(url)

    def get_content(self):
        # Returns all search results, use get_results_in_table to specify table id (e.g. players or teams)
        return self.get_results_in_table(True)

    def get_results_in_table(self, table_id) -> List[Tuple]:
        if self._parsed.find("div", id="info"):
            # sometimes the search automatically redirects to a specific player page.
            redirected_url = self._parsed.find("link", rel="canonical").attrs["href"]
            name = self._parsed.find("h1", itemprop="name").text
            return [(name, redirected_url)]
        results = []
        result_table = self._parsed.find("div", id=table_id)
        if result_table is not None:
            for result in result_table.find_all("div", class_="search-item"):
                name = result.find("div", class_="search-item-name").find("a")
                results.append((name.string.strip(), "https://www.basketball-reference.com" + name.attrs["href"]))
        return results


class Search:

    @classmethod
    def _new_scraper(cls, search_item):
        return SearchPageScraper(
            f"https://www.basketball-reference.com/search/search.fcgi?search={search_item}")

    @classmethod
    def search_players(cls, name: str) -> List[Tuple]:
        return cls._new_scraper(name).get_results_in_table("players")

    @classmethod
    def search_teams(cls, name: str) -> List[Tuple]:
        return cls._new_scraper(name).get_results_in_table("teams")
