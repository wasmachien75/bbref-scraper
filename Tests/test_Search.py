from unittest.case import TestCase

from Search import Search


class TestPlayerSearch(TestCase):
    def test_search(self):
        results = Search.search("Kobe")
        assert len(results) == 4
        assert 'Kobe Bryant (1997-2016)' in [_tuple[0] for _tuple in results]
        assert all([_tuple[1].startswith("https://www.basketball-reference.com/players/") for _tuple in results])

    def test_search_redirect(self):
        # sometimes the search engine does not return a result page, but redirects automatically
        results = Search.search("LeBron")
        assert isinstance(results, list)
        print(results)
