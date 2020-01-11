from dataclasses import dataclass, field
from typing import Optional, Any

from bballer.scrapers.gamelog import GameLogScraper


@dataclass
class AdvancedStatLine:
    season: Any
    per: float
    tsp: float
    tpar: float
    ftar: float
    orb: float
    drb: float
    trb: float
    astp: float
    stlp: float
    blkp: float
    tovp: float
    usgp: float
    ows: float
    dws: float
    wsp48: float
    obpm: float
    dbpm: float
    vorp: float
    bpm: float = field(init=False)
    ws: float = field(init=False)

    def __repr__(self):
        return f"Statline({self.season})"

    def __post_init__(self):
        if self.dbpm and self.obpm:
            self.bpm = self.dbpm + self.obpm
        if self.ows and self.dws:
            self.ws = self.ows + self.dws


@dataclass
class StatLine:
    season: str
    age: int
    all_star: bool
    minutesPlayed: int
    position: str
    team: str
    gamesPlayed: int
    gamesStarted: int
    fg_made: int
    fg_attempted: int
    two_fg_made: int
    two_fg_attempted: int
    three_fg_made: int
    three_fg_attempted: int
    free_throw_made: int
    free_throw_attempted: int
    offensive_rebounds: int
    defensive_rebounds: int
    assists: int
    steals: int
    blocks: int
    turnovers: int
    fouls: int
    points: int
    effective_fg_percentage: int
    advanced: Optional[AdvancedStatLine] = field(init=False, repr=False)
    _player_url: str

    def __repr__(self):
        return f"Statline({self.season})"

    @property
    def two_fg_percentage(self):
        return self.two_fg_made / self.two_fg_attempted

    @property
    def game_logs(self):
        scr = GameLogScraper(
            self._player_url.rstrip(".html") + "/gamelog/" + str((int(self.season[0:4]) + 1)))
        return scr.get_game_logs()

    @property
    def three_fg_percentage(self):
        return self.three_fg_made / self.three_fg_attempted

    @property
    def fg_percentage(self):
        return self.fg_made / self.fg_attempted

    @property
    def free_throw_percentage(self):
        return self.free_throw_made / self.free_throw_attempted

    @property
    def rebounds(self):
        return self.defensive_rebounds + self.offensive_rebounds