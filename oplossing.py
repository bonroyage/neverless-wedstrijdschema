import csv
from datetime import datetime
from pathlib import Path
from typing import Any, Callable

from tabulate import tabulate

from wedstrijd import Wedstrijd


class Oplossing(BaseException):
    def __init__(self, wedstrijden):
        self.wedstrijden = wedstrijden

    def exporteren_naar_csv(self, callback: Callable[[Wedstrijd], list[Any]], path: str = None):
        path = path \
            if path is not None \
            else "{}/wedstrijdschema_{}.csv".format(Path.home(), datetime.now().strftime("%Y-%m-%d_%H%M%S"))

        writer = csv.writer(open(path, 'w'))
        for row in self.wedstrijden:
            writer.writerow(callback(row))

        print("Geexporteerd naar csv: {}".format(path))

    def wedstrijden_tonen_op_scherm(self, headers: list[str], callback: Callable[[Wedstrijd], list[Any]]):
        data = map(callback, self.wedstrijden)
        print(tabulate(data, headers=headers))
