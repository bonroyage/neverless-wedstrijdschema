import time
from typing import Callable, Any, Optional, Union

from oplossing import Oplossing
from team import Team
from teams import get_team, gesorteerde_nummers
from wedstrijd import Wedstrijd
from wedstrijden import alle_wedstrijden


def solve(
        with_solution: Callable[[Oplossing], Any],
        team_eisen: Callable[[Wedstrijd, Team], Optional[bool]],
        mag_leeg: Union[bool, Callable[[Wedstrijd], Optional[bool]]] = False,
        schema_compleet: Callable[[], Optional[bool]] = None,
        pre_solve: Callable = None
):
    __wedstrijden = alle_wedstrijden()

    def __do_solve():
        if pre_solve is not None:
            pre_solve()

        for wedstrijd in __wedstrijden:
            if wedstrijd.needs_team():
                for team1 in gesorteerde_nummers(None, wedstrijd.week):
                    if wedstrijd.team_mag_spelen(get_team(team1), team_eisen):
                        wedstrijd.team1(get_team(team1))

                        for team2 in gesorteerde_nummers(team1 + 1, wedstrijd.week, wedstrijd.team_1):
                            if wedstrijd.team_mag_spelen(get_team(team2), team_eisen):
                                wedstrijd.team2(get_team(team2))
                                __do_solve()
                                wedstrijd.team2(False)

                        wedstrijd.team1(False)

                if (type(mag_leeg) == bool and mag_leeg) or (callable(mag_leeg) and mag_leeg(wedstrijd)):
                    wedstrijd.team_1 = True
                    __do_solve()
                    wedstrijd.team_1 = False

                return

        if schema_compleet is None or schema_compleet():
            raise Oplossing(__wedstrijden)

    start_time = time.time()

    try:
        __do_solve()
    except Oplossing as oplossing:
        with_solution(oplossing)
        print("Oplossing gevonden in {} seconden".format((time.time() - start_time)))
        return

    print("Geen oplossing gevonden in {} seconden".format((time.time() - start_time)))
