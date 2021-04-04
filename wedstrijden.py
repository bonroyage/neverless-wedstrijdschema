from typing import Callable

from teams import Team
from wedstrijd import Wedstrijd

__wedstrijden = []


def alle_wedstrijden() -> list[Wedstrijd]:
    global __wedstrijden
    return __wedstrijden


def wedstrijd_toevoegen(week: int, ronde: int, veld: int) -> Wedstrijd:
    global __wedstrijden
    wedstrijd = Wedstrijd(week, ronde, veld)
    __wedstrijden.append(wedstrijd)
    return wedstrijd


def filter_wedstrijden(condition: Callable[[Wedstrijd], bool]) -> list[Wedstrijd]:
    return [wedstrijd for wedstrijd in __wedstrijden if condition(wedstrijd)]


def teams_met_aantal_wedstrijden_in_week(week: int, aantal: int):
    from collections import Counter

    teams_spelend_deze_week = []

    for wedstrijd in filter_wedstrijden(lambda w: w.week == week):
        if wedstrijd.team_1 is not None:
            teams_spelend_deze_week.append(wedstrijd.team_1.nummer)

        if wedstrijd.team_2 is not None:
            teams_spelend_deze_week.append(wedstrijd.team_2.nummer)

    return len([count for x, count in Counter(teams_spelend_deze_week).items() if count == aantal])


def teams_in_wedstrijden(te_checken_wedstrijden: list[Wedstrijd]) -> list[Team]:
    unieke_teams_voor_wedstrijden = []

    for wedstrijd in te_checken_wedstrijden:
        for team in [wedstrijd.team_1, wedstrijd.team_2]:
            if team is not None and team not in unieke_teams_voor_wedstrijden:
                unieke_teams_voor_wedstrijden.append(team)

    return unieke_teams_voor_wedstrijden
