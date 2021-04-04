from team import Team

_teams: list[Team] = []


def gesorteerde_nummers(start=None, week: int = None, team: Team = None) -> [int]:
    global _teams
    lijst_van_team_nummers = list(range(len(_teams) - 1) if start is None else range(start, len(_teams)))
    lijst_van_team_nummers.sort(key=lambda id: _teams[id].sort(week, team))
    return lijst_van_team_nummers


def team_toevoegen(naam: str = None) -> Team:
    global _teams
    team = Team(len(_teams) + 1)
    team.naam = naam if naam is not None else "Team {}".format(team.nummer)
    _teams.append(team)
    return team


def get_team(id) -> Team:
    global _teams
    return _teams[id]


def alle_teams() -> list[Team]:
    global _teams
    return _teams
