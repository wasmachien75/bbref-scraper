from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class TeamSeason:
    season: str
    wins: int
    losses: int
    pace: float
    won_championship: bool
    made_playoffs: bool
    playoff_result: str
    rel_pace: float
    ortg: float
    rel_ortg: float
    drtg: float
    rel_drtg: float
    _team_code: str
    _roster: List[Dict] = field(init=False, default_factory=list)

    @property
    def roster(self) -> List[Dict]:
        if not self._roster:
            from bballer.scrapers.TeamScraper import TeamSeasonScraper
            scraper = TeamSeasonScraper(self._team_code, int(self.season[0:4]) + 1)
            self._roster = scraper.get_roster()
        return self._roster


@dataclass
class Team:
    name: str
    code: str
    seasons: List[TeamSeason]  # store in a list so we can easily get number of championships and playoff appearances
    wins: int
    losses: int
    championships: int = field(init=False)
    playoff_appearances: int = field(init=False)

    def __post_init__(self):
        self.playoff_appearances = len([s for s in self.seasons if s.made_playoffs])
        self.championships = len([s for s in self.seasons if s.won_championship])

    def season(self, year: str):
        season = [s for s in self.seasons if s.season.startswith(str(year))]
        return season[0] if season else None


@dataclass(frozen=True)
class TeamShell:
    name: str
    url: str

    def __repr__(self):
        return self.name

    def as_team(self) -> Team:
        from bballer.scrapers.TeamScraper import TeamPageScraper
        scr = TeamPageScraper(self.url)
        return scr.get_content()
