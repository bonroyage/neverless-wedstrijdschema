from oplossing import Oplossing
from solver import solve
from team import Team
from teams import team_toevoegen
from wedstrijd import Wedstrijd
from wedstrijden import wedstrijden_importeren, wedstrijd_toevoegen as base_wedstrijd_toevoegen

"""
TEAMS
=====
Run team_toevoegen voor elk team dat toegevoegd moet worden. Optioneel een naam meegeven als parameter. Zonder naam zal
het "Team 1" etc heten.
"""

team_toevoegen("FlamingVo's")
team_toevoegen("DHL")
team_toevoegen("Hot Shots")
team_toevoegen("Kroegtijgers")
team_toevoegen("UiTerAardbei")
team_toevoegen("In 't coronetje")
team_toevoegen("Grey Goose")
team_toevoegen("Ice Ice Baby")
team_toevoegen("Blue Balls")
team_toevoegen("Black Eyed Pils")
team_toevoegen("GoalDiggers")
team_toevoegen("Pino Noir")
team_toevoegen("Always More")
team_toevoegen("LSD")

"""
WEDSTRIJDEN
===========
Run wedstrijd_toevoegen voor elke wedstrijd die toegevoegd moet worden met een week, ronde en veld nummer of
wedstrijden_importeren voor een tab delimited file met week, ronde en veld nummer en optioneel team nummers (vanaf 1).
"""


def wedstrijd_toevoegen(week, ronde, veld):
    with base_wedstrijd_toevoegen(week, ronde, veld) as wedstrijd:
        wedstrijd.groep = "A" if wedstrijd.ronde <= 3 else "B"
        return wedstrijd


wedstrijden_importeren('20_voorjaar_tot_week_17.txt', wedstrijd_toevoegen)


def wedstrijden_toevoegen(week, ronde, *velden):
    for veld in velden:
        wedstrijd_toevoegen(week, ronde, veld)


for week in range(18, 23):
    wedstrijden_toevoegen(week, 1, 5, 6)
    wedstrijden_toevoegen(week, 2, 5, 6)
    wedstrijden_toevoegen(week, 3, 5, 6)
    wedstrijden_toevoegen(week, 4, 3, 4, 5, 6)
    wedstrijden_toevoegen(week, 5, 3, 4, 5, 6)
    wedstrijden_toevoegen(week, 6, 3, 4, 5, 6)
    wedstrijden_toevoegen(week, 7, 3, 4, 5, 6)

# 21 wedstrijden
# wedstrijden_toevoegen(22, 4, 5, 6)
# wedstrijden_toevoegen(22, 5, 5, 6)
# wedstrijden_toevoegen(22, 6, 5, 6)
# wedstrijden_toevoegen(22, 7, 3, 4, 5, 6)

# 22 wedstrijden
# wedstrijden_toevoegen(22, 1, 5, 6)
# wedstrijden_toevoegen(22, 4, 5, 6)
# wedstrijden_toevoegen(22, 5, 5, 6)
# wedstrijden_toevoegen(22, 6, 3, 4, 5, 6)
# wedstrijden_toevoegen(22, 7, 3, 4, 5, 6)

"""
CRITERIA
========
Deze functie bepaalt of een team mag spelen in een wedstrijd. Return False als dit niet het geval is. Het is niet
nodig om True te returnen aan het eind, het is automatisch True als de return geen False is.
"""


def wedstrijd_is_zelfde_groep_als(wedstrijd1: Wedstrijd, wedstrijd2: Wedstrijd) -> bool:
    return wedstrijd1.week == wedstrijd2.week and wedstrijd1.groep == wedstrijd2.groep


def team_speelt_in_groep(team: Team, wedstrijd: Wedstrijd) -> bool:
    return team.aantal_wedstrijden(lambda w: wedstrijd_is_zelfde_groep_als(w, wedstrijd)) > 0


max_wedstrijden_per_team = 21


def team_mag_spelen(wedstrijd: Wedstrijd, team: Team) -> bool:
    from wedstrijden import heeft_teams_met_lange_pauzes_in_week

    """ Een team kan natuurlijk niet twee wedstrijden op hetzelfde moment spelen. """
    if team.speelt_in_ronde(wedstrijd):
        return False

    # is_vroege_groep: bool = wedstrijd.groep == "A"

    """ Het team heeft al 18 wedstrijden gespeeld. """
    if team.aantal_wedstrijden() >= max_wedstrijden_per_team:
        return False

    deze_week: int = team.aantal_wedstrijden_in_week(wedstrijd.week)

    """ Het team heeft al 3 wedstrijden gespeeld deze week. """
    if deze_week >= 3:
        return False

    # """ Het team heeft al 4 weken gehad waarin het 3 wedstrijden speelden. Om aan de 18 wedstrijden te komen
    # zonder dat er weken tussen zitten met maar 0 of 1 wedstrijden moeten er van de 7 weken 4 zijn met 3
    # wedstrijden en 3 met 2 wedstrijden. """
    # if deze_week == 3 and team.weken_met_aantal_wedstrijden(4) >= 1:
    #     return False
    #
    # """ Er zijn al 8 teams die 3 wedstrijden spelen deze week, en dus kan dit team met 2 gespeelde wedstrijden er
    # niet nog eentje bij krijgen. Als er meer dan 8 teams zijn die 3 wedstrijden spelen dan moet er een ander team
    # zijn wat 0 of 1 wedstrijd speelt die week. """
    # if deze_week == 3 and teams_met_aantal_wedstrijden_in_week(wedstrijd.week, 4) >= 2:
    #     return False

    if heeft_teams_met_lange_pauzes_in_week(wedstrijd.week, wedstrijd.ronde, 2):
        return False

    # if is_vroege_groep and not team_speelt_in_groep(team, wedstrijd):
    #     teams = teams_in_wedstrijden(filter_wedstrijden(lambda w: wedstrijd_is_zelfde_groep_als(wedstrijd, w)))
    #
    #     """ Afhankelijk van de groep (vroeg of laat) is er een limiet aan het aantal teams dat tegelijkertijd
    #     aanwezig mag zijn. In de vroege groep zijn dit 5 teams, in de late groep 10 teams. Als het limiet is bereikt
    #     en dit team zit niet in die groep, dan mag deze niet bij deze wedstrijd worden toegewezen. Hiervoor moet er
    #     uit de teams gekozen worden die reeds in de groep zaten. """
    #     if len(teams) >= 5:
    #         return False

    """ Een team mag niet meer dan 2 rondes geen wedstrijd spelen. """
    laatste_ronde = team.laatste_ronde_in_week(wedstrijd.week)
    if laatste_ronde is not None and (wedstrijd.ronde - laatste_ronde) > 2:
        return False

    """ De volgende condities kunnen alleen gecheckt worden als het team dat gecheckt wordt moet worden toegewezen aan
    het tweede team en we dus informatie hebben over de twee teams die tegen elkaar spelen """
    if wedstrijd.team_1 is not None:

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

            if wedstrijd.team_1.aantal_dubbele_wedstrijden >= (max_wedstrijden_per_team - 14) + 1:
                return False

            if team.aantal_dubbele_wedstrijden >= (max_wedstrijden_per_team - 14) + 1:
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
        wedstrijd.team_1.nummer if wedstrijd.team_1 is not None else "",
        wedstrijd.team_2.nummer if wedstrijd.team_2 is not None else "",
        wedstrijd.team_1.naam if wedstrijd.team_1 is not None else "",
        wedstrijd.team_2.naam if wedstrijd.team_2 is not None else ""
    ])

    oplossing.wedstrijden_tonen_op_scherm([
        "Week",
        "Ronde",
        "Veld",
        "Team 1",
        "Team 2"
    ], lambda wedstrijd: [
        wedstrijd.week,
        wedstrijd.ronde,
        wedstrijd.veld,
        "[ {nummer: >2} ] {naam}".format(nummer=wedstrijd.team_1.nummer,
                                         naam=wedstrijd.team_1.naam) if wedstrijd.team_1 is not None else "",
        "[ {nummer: >2} ] {naam}".format(nummer=wedstrijd.team_2.nummer,
                                         naam=wedstrijd.team_2.naam) if wedstrijd.team_2 is not None else ""
    ])


def mag_leeg(wedstrijd):
    from wedstrijden import teams_met_aantal_wedstrijden_in_week, teams_met_aantal_wedstrijden

    return (
            teams_met_aantal_wedstrijden_in_week(wedstrijd.week, 3) == 14
            or
            teams_met_aantal_wedstrijden(max_wedstrijden_per_team) == 14
    )


"""
SOLVE
=====
De solve functie start de berekeningen. De functies zodra er een oplossing is en of een team mag spelen worden hierin 
meegegeven.
"""

solve(opgelost, team_mag_spelen, mag_leeg)
