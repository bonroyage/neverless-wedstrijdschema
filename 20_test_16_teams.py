from oplossing import Oplossing
from solver import solve
from team import Team
from teams import team_toevoegen, alle_teams
from wedstrijd import Wedstrijd
from wedstrijden import wedstrijd_toevoegen

"""
TEAMS
=====
Run team_toevoegen voor elk team dat toegevoegd moet worden. Optioneel een naam meegeven als parameter. Zonder naam zal
het "Team 1" etc heten.
"""

for team in range(1, 17):  # 1 tot 16
    team_toevoegen()

"""
WEDSTRIJDEN
===========
Run wedstrijd_toevoegen voor elke wedstrijd die toegevoegd moet worden met een week, ronde en veld nummer of
wedstrijden_importeren voor een tab delimited file met week, ronde en veld nummer en optioneel team nummers (vanaf 1).
"""


def wedstrijden_toevoegen(week, ronde, *velden):
    for veld in velden:
        wedstrijd_toevoegen(week, ronde, veld)


for week in range(1, 10):  # 1 tot 9
    wedstrijden_toevoegen(week, 1, 5, 6)
    wedstrijden_toevoegen(week, 2, 5, 6)
    wedstrijden_toevoegen(week, 3, 5, 6)
    wedstrijden_toevoegen(week, 4, 3, 4, 5, 6)
    wedstrijden_toevoegen(week, 5, 3, 4, 5, 6)
    wedstrijden_toevoegen(week, 6, 3, 4, 5, 6)
    wedstrijden_toevoegen(week, 7, 3, 4, 5, 6)

"""
CRITERIA
========
Deze functie bepaalt of een team mag spelen in een wedstrijd. Return False als dit niet het geval is. Het is niet
nodig om True te returnen aan het eind, het is automatisch True als de return geen False is.
"""

max_wedstrijden_per_team = 24
aantal_teams = len(alle_teams())
max_dubbele_wedstrijden = max_wedstrijden_per_team - aantal_teams + 1
max_wedstrijden_per_week = 3


def team_mag_spelen(wedstrijd: Wedstrijd, team: Team) -> bool:
    from wedstrijden import teams_met_aantal_wedstrijden_in_week

    """ Het team heeft al het max aantal wedstrijden gespeeld. """
    if team.aantal_wedstrijden() >= max_wedstrijden_per_team:
        return False

    deze_week: int = team.aantal_wedstrijden_in_week(wedstrijd.week)

    """ Het team heeft al 3 wedstrijden gespeeld deze week. """
    if deze_week >= max_wedstrijden_per_week:
        return False

    """ Er zijn al 12 teams die 3 wedstrijden spelen deze week, en dus kan dit team met 2 gespeelde wedstrijden er
    niet nog eentje bij krijgen. Als er meer dan 12 teams zijn die 3 wedstrijden spelen dan moet er een ander team
    zijn wat 0 of 1 wedstrijd speelt die week. """
    if deze_week == 2 and teams_met_aantal_wedstrijden_in_week(wedstrijd.week, 3) >= 12:
        return False

    """ Een team mag niet meer dan 2 rondes geen wedstrijd spelen. """
    laatste_ronde = team.laatste_ronde_in_week(wedstrijd.week)
    if laatste_ronde is not None and (wedstrijd.ronde - laatste_ronde) > 2:
        return False

    """ De volgende condities kunnen alleen gecheckt worden als het team dat gecheckt wordt moet worden toegewezen aan
    het tweede team en we dus informatie hebben over de twee teams die tegen elkaar spelen """
    if isinstance(wedstrijd.team_1, Team):

        """ Voorkomen dat twee teams in dezelfde week twee keer tegen elkaar spelen """
        if wedstrijd.team_1.heeft_gespeeld_tegen_in_week(team, wedstrijd.week):
            return False

        al_gespeeld = team.aantal_wedstrijden_tegen_team(wedstrijd.team_1)

        """ Voorkomen dat je meer dan twee keer tegen hetzelfde team speelt in de hele competitie """
        if al_gespeeld >= 2:
            return False

        """ Met 18 te spelen wedstrijden en 14 teams kan je er maar tegen 5 teams 2 keer spelen. 13 wedstrijden
        tegen elk team om 1x te spelen, dat houdt 5 over. Pas nu kunnen we dit checken voor team 1 omdat de kans
        bestaat dat dit team ingedeeld wordt tegen een team waar ze nog niet tegen hebben gespeeld """
        if al_gespeeld == 1:

            if wedstrijd.team_1.aantal_dubbele_wedstrijden >= max_dubbele_wedstrijden:
                return False

            if team.aantal_dubbele_wedstrijden >= max_dubbele_wedstrijden:
                return False


"""
OPGELOST
========
Als er een oplossing gevonden is dan wordt deze functie aangeroepen. Hierin kan worden geexporteerd naar een CSV bestand
of het wedstrijdschema tonen op het scherm in een tabel.
"""


def opgelost(oplossing: Oplossing):
    oplossing.exporteren_naar_csv(lambda wedstrijd: [
        wedstrijd.week,
        wedstrijd.ronde,
        wedstrijd.veld,
        wedstrijd.team_1.nummer if wedstrijd.has_team() else "",
        wedstrijd.team_2.nummer if wedstrijd.has_team() else "",
        wedstrijd.team_1.naam if wedstrijd.has_team() else "",
        wedstrijd.team_2.naam if wedstrijd.has_team() else ""
    ])


"""
MAG LEEG
========
Checkt of een wedstrijd leeg mag blijven, dit kan een callable zijn of een boolean.
"""


def mag_leeg(wedstrijd: Wedstrijd):
    from wedstrijden import teams_met_aantal_wedstrijden, teams_met_aantal_wedstrijden_in_week
    return (
            teams_met_aantal_wedstrijden(max_wedstrijden_per_team) == aantal_teams
            or
            teams_met_aantal_wedstrijden_in_week(wedstrijd.week, 2, True) == aantal_teams
    )


"""
SCHEMA COMPLEET
========
Checkt of het schema compleet is volgens de eisen.
"""


def schema_compleet():
    from wedstrijden import teams_met_aantal_wedstrijden
    return teams_met_aantal_wedstrijden(max_wedstrijden_per_team) == aantal_teams


"""
SOLVE
=====
De solve functie start de berekeningen
"""


def summary():
    from teams import alle_teams
    from wedstrijden import filter_wedstrijden
    from tabulate import tabulate
    data = [[
        team.naam,
        team.aantal_wedstrijden(),
        team.aantal_dubbele_wedstrijden,
        team.aantal_wedstrijden_in_week(1),
        team.aantal_wedstrijden_in_week(2),
        team.aantal_wedstrijden_in_week(3),
        team.aantal_wedstrijden_in_week(4),
        team.aantal_wedstrijden_in_week(5),
        team.aantal_wedstrijden_in_week(6),
        team.aantal_wedstrijden_in_week(7),
        team.aantal_wedstrijden_in_week(8),
        team.aantal_wedstrijden_in_week(9)
    ] for team in alle_teams()]
    data.append([
        "Blank",
        "",
        "",
        len(filter_wedstrijden(lambda w: w.week == 1 and not w.has_team())),
        len(filter_wedstrijden(lambda w: w.week == 2 and not w.has_team())),
        len(filter_wedstrijden(lambda w: w.week == 3 and not w.has_team())),
        len(filter_wedstrijden(lambda w: w.week == 4 and not w.has_team())),
        len(filter_wedstrijden(lambda w: w.week == 5 and not w.has_team())),
        len(filter_wedstrijden(lambda w: w.week == 6 and not w.has_team())),
        len(filter_wedstrijden(lambda w: w.week == 7 and not w.has_team())),
        len(filter_wedstrijden(lambda w: w.week == 8 and not w.has_team())),
        len(filter_wedstrijden(lambda w: w.week == 9 and not w.has_team()))
    ])

    print("\033[F" * (len(data) + 4))

    print(tabulate(data, headers=["Team", "Totaal", "Dubbel", "1", "2", "3", "4", "5", "6", "7", "8", "9"]))


solve(
    opgelost,
    team_mag_spelen,
    mag_leeg,
    schema_compleet,
    # summary
)
