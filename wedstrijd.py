from __future__ import annotations

from typing import Optional, Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from team import Team


class Wedstrijd:
    week: int
    ronde: int
    veld: int
    team_1: Optional[Team]
    team_2: Optional[Team]

    def __init__(self, week: int, ronde: int, veld: int):
        self.week = week
        self.ronde = ronde
        self.veld = veld
        self.team_1 = None
        self.team_2 = None

    def __enter__(self) -> Wedstrijd:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def team1(self, team: Optional[Team]):
        if self.team_1 is not None:
            self.team_1.wedstrijden.remove(self)

        self.team_1 = team

        if self.team_1 is not None:
            self.team_1.wedstrijden.append(self)

    def team2(self, team: Optional[Team]):
        if self.team_2 is not None:
            self.team_2.wedstrijden.remove(self)

        self.team_2 = team

        if self.team_2 is not None:
            self.team_2.wedstrijden.append(self)

    def andere_team(self, team: Team) -> Optional[Team]:
        return self.team_1 if self.team_2 == team else self.team_2

    def heeft_spelend_team(self, team: Team) -> bool:
        return self.team_1 == team or self.team_2 == team

    def is_zelfde_ronde_als(self, other: Wedstrijd) -> bool:
        return self.week == other.week and self.ronde == other.ronde

    def team_mag_spelen(self, team, eisen: Callable[[Wedstrijd, Team], Optional[bool]]) -> bool:
        # Team is ook het eerste team op deze wedstrijd, kan nooit
        if self.team_1 is not None and self.team_1 == team:
            return False

        response = eisen(self, team)
        return response if type(response) == bool else True
