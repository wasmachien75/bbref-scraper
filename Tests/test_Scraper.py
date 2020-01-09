from unittest import TestCase
from Scraper import *
from Statline import StatLine
from pathlib import Path

from TeamScraper import TeamPageScraper


def assert_equal(first, second):
    if first != second:
        raise AssertionError(f"AssertionError: {first} does not equal {second}")


def get_resource(fn):
    return str(Path(__file__).parent.joinpath("resources").joinpath(fn).absolute())


class TestScraper:
    carmelo_anthony = PlayerPageScraper(get_resource("carmelo_anthony.html"))
    lebron_james = PlayerPageScraper(get_resource("lebron_james.html"))
    julius_erving = PlayerPageScraper(get_resource("julius_erving.html"))
    ben_wallace = PlayerPageScraper(get_resource("ben_wallace.html"))

    def test_equality(self):
        this_player = self.carmelo_anthony.player()
        assert (this_player != self.lebron_james.player())
        _set = {this_player, this_player}
        assert len(_set) == 1

    def test__get_name(self):
        assert self.carmelo_anthony._get_name() == "Carmelo Anthony"

    def test_get_dob(self):
        assert self.carmelo_anthony._get_dob() == "1984-05-29"

    def test_get_career_stats(self):
        stats = self.carmelo_anthony._get_career_stats()
        assert isinstance(stats, StatLine)
        assert int(stats.gamesStarted) > 1000

    def test_get_id(self):
        assert self.carmelo_anthony._get_id() == "carmelo_anthony"

    def test_get_shooting_hand(self):
        assert self.carmelo_anthony._get_shooting_hand() == "Right"

    def test_get_college(self):
        assert self.carmelo_anthony._get_college() == "Syracuse"
        assert self.lebron_james._get_college() is None

    def test_player(self):
        player = self.carmelo_anthony.player()
        assert len(player.seasons) > 10
        rookie_season = player.seasons[0]
        assert rookie_season.position == "SF"
        assert_equal(rookie_season.season, "2003-04")
        assert_equal(rookie_season.gamesStarted, 82)
        assert_equal(rookie_season.gamesPlayed, 82)
        assert_equal(rookie_season.minutesPlayed, 2995)
        assert_equal(rookie_season.fg_attempted, 1465)
        assert_equal(rookie_season.fg_made, 624)
        assert_equal(rookie_season.three_fg_made, 69)
        assert_equal(rookie_season.three_fg_attempted, 214)
        assert_equal(rookie_season.two_fg_attempted, 1251)
        assert_equal(rookie_season.two_fg_made, 555)
        assert_equal(rookie_season.effective_fg_percentage, 0.449)
        assert_equal(rookie_season.free_throw_made, 408)
        assert_equal(rookie_season.free_throw_attempted, 525)
        assert_equal(rookie_season.offensive_rebounds, 183)
        assert_equal(rookie_season.defensive_rebounds, 315)
        assert_equal(rookie_season.rebounds, 498)
        assert_equal(rookie_season.all_star, False)
        assert_equal(rookie_season.assists, 227)
        assert_equal(rookie_season.blocks, 41)
        assert_equal(rookie_season.turnovers, 247)
        assert_equal(rookie_season.steals, 97)
        assert_equal(rookie_season.fouls, 225)
        assert_equal(rookie_season.points, 1725)

    def test_advanced_stats(self):
        player = self.carmelo_anthony.player()
        s = player.seasons[0]
        assert s.advanced.astp == 13.8
        assert s.advanced.per == 17.6
        assert s.advanced.tsp == 0.509
        assert s.advanced.tpar == 0.146
        assert s.advanced.ftar == 0.358
        assert s.advanced.orb == 6.8
        assert s.advanced.drb == 12.1
        assert s.advanced.trb == 9.4
        assert s.advanced.stlp == 1.7
        assert s.advanced.blkp == 1.0
        assert s.advanced.tovp == 12.7
        assert s.advanced.usgp == 28.5
        assert s.advanced.ows == 3.7
        assert s.advanced.dws == 2.4
        assert s.advanced.ws == 6.1
        assert s.advanced.wsp48 == 0.098
        assert s.advanced.obpm == 1.2
        assert s.advanced.dbpm == -1.2
        assert s.advanced.bpm == 0
        assert s.advanced.vorp == 1.6

    def test_seasons(self):
        seasons = self.julius_erving._get_regular_season_totals()
        assert len(seasons) == 11  # ABA seasons must be discarded

    def test_get_physicals(self):
        assert self.carmelo_anthony._get_physicals() == ("6-8", 240)

    def test_get_draft_pick(self):
        assert self.carmelo_anthony._get_draft_pick() == 3
        assert self.ben_wallace._get_draft_pick() is None

    def test_all_star(self):
        assert len([season for season in self.julius_erving._get_regular_season_totals() if season.all_star]) == 11

    def test_get_playoff_totals(self):
        assert len(self.julius_erving._get_playoffs_totals()) == 11
        assert sum([season.points for season in self.julius_erving._get_playoffs_totals()]) == 3088

    def test_historical_player(self):
        player = PlayerPageScraper("https://www.basketball-reference.com/players/h/hawkito01.html").player()
        assert player.name == "Tom Hawkins"
        assert player.date_of_birth == "1936-12-22"


class TestPlayerListScraper(TestCase):

    def test_scrape(self):
        s = PlayerListScraper(get_resource("w.html"))
        urls = s.get_player_urls()
        assert len(urls) == 364
        assert all([url.startswith("https://www.basketball-reference.com/players/") for url in urls])


class TestTotalMinutesListScraper:
    def test_scrape(self):
        s = TotalMinutesScraper(2000)
        urls = s.get_player_urls()
        assert len(urls) > 10
        assert all([url.startswith("https://www.basketball-reference.com/players/") for url in urls])


class TestBulkScraper:

    def test_scrape(self):
        logging.getLogger().setLevel(logging.DEBUG)
        bulk_scr = BulkScraper(map(get_resource, ["lebron_james.html", "carmelo_anthony.html"]))
        processed = bulk_scr.scrape_all()
        assert_equal(len(processed), 2)
        assert "Carmelo Anthony" in [p.name for p in processed]

    def test_double_scrape(self):
        bulk_scr = BulkScraper(map(get_resource, ["lebron_james.html", "lebron_james.html"]))
        players = bulk_scr.scrape_all()
        assert len(players) == 1


class TestTeamPageScraper:

    def test_team(self):
        scr = TeamPageScraper("CLE")
        team = scr.team()
        assert team.name == "Cleveland Cavaliers"
        assert team.code == "CLE"

    def test_team_with_url(self):
        team = TeamPageScraper(get_resource("cavs.html")).team()
        assert team.name == "Cleveland Cavaliers"
        assert team.wins == 1858
        assert team.losses == 2149
        assert team.playoff_appearances == 22
        assert team.championships == 1
        assert team.code == "CLE"
        assert len(team.seasons) == 50

    def test_season(self):
        team = TeamPageScraper(get_resource("cavs.html")).team()
        last_season = team.seasons[-1]
        assert last_season.losses == 27
        assert last_season.wins == 10
        assert last_season.pace == 98.8
        assert last_season.rel_pace == -1.6
        assert last_season.ortg == 105.6
        assert last_season.rel_ortg == -3.6
        assert last_season.season == "2019-20"
        assert not last_season.won_championship
        assert not last_season.made_playoffs
        team = TeamPageScraper(get_resource("cavs.html")).team()
        championship_season = team.season("2015-16")
        assert championship_season.wins == 57
        assert championship_season.won_championship
        assert championship_season.made_playoffs
