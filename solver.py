import time
from typing import Callable, Any, Optional

from oplossing import Oplossing
from team import Team
from teams import get_team, gesorteerde_nummers
from wedstrijd import Wedstrijd
from wedstrijden import alle_wedstrijden


def solve(with_solution: Callable[[Oplossing], Any], team_eisen: Callable[[Wedstrijd, Team], Optional[bool]], mag_leeg: Callable[[Wedstrijd], Optional[bool]]):
    __wedstrijden = alle_wedstrijden()

    def __do_solve():
        from tools import summary
        summary(True)

        for wedstrijd in __wedstrijden:
            if wedstrijd.team_1 is None:
                for team1 in gesorteerde_nummers(None, wedstrijd.week):
                    if wedstrijd.team_mag_spelen(get_team(team1), team_eisen):
                        wedstrijd.team1(get_team(team1))

                        for team2 in gesorteerde_nummers(team1 + 1, wedstrijd.week, wedstrijd.team_1):
                            if wedstrijd.team_mag_spelen(get_team(team2), team_eisen):
                                wedstrijd.team2(get_team(team2))
                                __do_solve()
                                wedstrijd.team2(None)

                        wedstrijd.team1(None)

                if mag_leeg(wedstrijd):
                    wedstrijd.team_1 = -1
                    __do_solve()
                    wedstrijd.team_1 = None

                return

        raise Oplossing(__wedstrijden)

    start_time = time.time()

    try:
        __do_solve()
    except Oplossing as oplossing:
        with_solution(oplossing)
        print("Oplossing gevonden in {} seconden".format((time.time() - start_time)))
        return

    print("Geen oplossing gevonden in {} seconden".format((time.time() - start_time)))
