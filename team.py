from __future__ import annotations

from random import random
from typing import Any, Optional, Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from wedstrijd import Wedstrijd


class Team:
    wedstrijden: list[Any]
    naam: str
    nummer: int

    def __init__(self, nummer: int):
        self.nummer = nummer
        self.wedstrijden = []

    def __enter__(self) -> Team:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    @property
    def aantal_dubbele_wedstrijden(self) -> int:
        from collections import Counter

        teams = [wedstrijd.andere_team(self) for wedstrijd in self.wedstrijden]

        return len([count for x, count in Counter(teams).items() if count >= 2 and isinstance(x, Team)])

    def aantal_wedstrijden(self, callback: Optional[Callable[[Wedstrijd], bool]] = None) -> int:
        if callback is None:
            return len(self.wedstrijden)
        else:
            return len([wedstrijd for wedstrijd in self.wedstrijden if callback(wedstrijd)])

    def aantal_wedstrijden_tegen_team(self, team: Team) -> int:
        return self.aantal_wedstrijden(lambda w: w.heeft_spelend_team(team))

    def aantal_wedstrijden_in_week(self, week: int) -> int:
        return self.aantal_wedstrijden(lambda w: w.week == week)

    def speelt_in_ronde(self, other: Wedstrijd) -> bool:
        return self.aantal_wedstrijden(lambda w: w.is_zelfde_ronde_als(other)) > 0

    def heeft_gespeeld_tegen_in_week(self, team: Team, week: int) -> bool:
        return self.aantal_wedstrijden(lambda w: w.week == week and w.heeft_spelend_team(team)) > 0

    def weken_met_aantal_wedstrijden(self, aantal: int) -> int:
        weken = list(set([wedstrijd.week for wedstrijd in self.wedstrijden]))
        return len([week for week in weken if self.aantal_wedstrijden_in_week(week) == aantal])

    def laatste_ronde_in_week(self, week: int) -> int:
        rondes = [wedstrijd.ronde for wedstrijd in self.wedstrijden if wedstrijd.week == week]
        return max(rondes) if len(rondes) > 0 else None

    def sort(self, week: int = None, team: Team = None):
        laatste_ronde = self.laatste_ronde_in_week(week) if week is not None else None
        return (
            laatste_ronde * -1 if laatste_ronde is not None else 99,
            self.aantal_wedstrijden_in_week(week) if week is not None else 0,
            self.aantal_wedstrijden_tegen_team(team) if team is not None else 0,
            self.aantal_wedstrijden(),
            week % self.nummer if week is not None else random()
        )
