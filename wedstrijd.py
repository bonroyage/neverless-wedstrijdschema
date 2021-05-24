from __future__ import annotations

from typing import Optional, Callable, Union

from team import Team


class Wedstrijd:
    week: int
    ronde: int
    veld: int

    """
    Teams:
    - False als er nog geen team is toegewezen
    - True als er expliciet geen team is toegewezen
    - Team zodra een team is toegewezen
    """
    team_1: Union[bool, Team]
    team_2: Union[bool, Team]

    def __init__(self, week: int, ronde: int, veld: int):
        self.week = week
        self.ronde = ronde
        self.veld = veld
        self.team_1 = False
        self.team_2 = False

    def __enter__(self) -> Wedstrijd:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def needs_team(self):
        return self.team_1 is False

    def has_team(self):
        return isinstance(self.team_1, Team)

    def team1(self, team: Union[bool, Team]):
        if isinstance(self.team_1, Team):
            self.team_1.wedstrijden.remove(self)

        self.team_1 = team

        if isinstance(self.team_1, Team):
            self.team_1.wedstrijden.append(self)

    def team2(self, team: Union[bool, Team]):
        if isinstance(self.team_2, Team):
            self.team_2.wedstrijden.remove(self)

        self.team_2 = team

        if isinstance(self.team_2, Team):
            self.team_2.wedstrijden.append(self)

    def andere_team(self, team: Team) -> Team:
        return self.team_1 if self.team_2 == team else self.team_2

    def heeft_spelend_team(self, team: Team) -> bool:
        return self.team_1 == team or self.team_2 == team

    def is_zelfde_ronde_als(self, other: Wedstrijd) -> bool:
        return self.week == other.week and self.ronde == other.ronde

    def team_mag_spelen(self, team, eisen: Callable[[Wedstrijd, Team], Optional[bool]]) -> bool:
        # Team is ook het eerste team op deze wedstrijd, kan nooit
        if self.team_1 is not False and self.team_1 == team:
            return False

        # Een team kan natuurlijk niet twee wedstrijden op hetzelfde moment spelen.
        if team.speelt_in_ronde(self):
            return False

        response = eisen(self, team)
        return response if type(response) == bool else True
