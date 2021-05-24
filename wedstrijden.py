import csv
from typing import Callable

from teams import Team, alle_teams
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


def wedstrijden_importeren(bestand, callback=None):
    from teams import get_team

    callback = callback if callback is not None else wedstrijd_toevoegen

    with open(bestand, 'r') as f:
        for row in csv.reader(f, dialect='excel', delimiter='\t'):
            with callback(int(row[0]), int(row[1]), int(row[2])) as wedstrijd:
                if len(row) > 3:
                    wedstrijd.team1(get_team(int(row[3]) - 1))

                if len(row) > 4:
                    wedstrijd.team2(get_team(int(row[4]) - 1))


def filter_wedstrijden(condition: Callable[[Wedstrijd], bool]) -> list[Wedstrijd]:
    return [wedstrijd for wedstrijd in __wedstrijden if condition(wedstrijd)]


def teams_met_aantal_wedstrijden(aantal: int):
    from collections import Counter

    teams = []

    for wedstrijd in __wedstrijden:
        if wedstrijd.has_team():
            teams.append(wedstrijd.team_1.nummer)
            teams.append(wedstrijd.team_2.nummer)

    return len([count for x, count in Counter(teams).items() if count == aantal])


def teams_met_aantal_wedstrijden_in_week(week: int, aantal: int, gte: bool = False):
    from collections import Counter

    teams_spelend_deze_week = []

    for wedstrijd in filter_wedstrijden(lambda w: w.week == week):
        if isinstance(wedstrijd.team_1, Team):
            teams_spelend_deze_week.append(wedstrijd.team_1.nummer)

        if isinstance(wedstrijd.team_2, Team):
            teams_spelend_deze_week.append(wedstrijd.team_2.nummer)

    return len([count for x, count in Counter(teams_spelend_deze_week).items() if
                count == aantal or (gte and count >= aantal)])


def heeft_teams_met_lange_pauzes_in_week(week: int, ronde: int, aantal: int) -> bool:
    counter = 0

    for team in alle_teams():
        laatste_ronde = team.laatste_ronde_in_week(week)

        if laatste_ronde is not None and (ronde - laatste_ronde) > aantal:
            counter += 1

    return counter > 0


def teams_in_wedstrijden(te_checken_wedstrijden: list[Wedstrijd]) -> list[Team]:
    unieke_teams_voor_wedstrijden = []

    for wedstrijd in te_checken_wedstrijden:
        for team in [wedstrijd.team_1, wedstrijd.team_2]:
            if team is not None and team not in unieke_teams_voor_wedstrijden:
                unieke_teams_voor_wedstrijden.append(team)

    return unieke_teams_voor_wedstrijden
