import functools
import operator
from money import Money

class Portfolio:

    def __init__(self, *moneys):
        self.moneys = []
        self._eur_to_usd = 1.2

    def add(self, *moneys):
        self.moneys.extend(moneys)

    def evaluate(self, bank, currency):
        total = 0.0
        failures = []
        for m in self.moneys:
            try:
                total += bank.convert(m, currency).amount
            except KeyError as ke:
                failures.append(ke)
        
        if len(failures) == 0:
            return Money(total, currency)

        failureMessage = ",".join(f.args[0] for f in failures)
        raise Exception("Missing exchange rate(s):[" + failureMessage + "]")

    def __convert(self, aMoney, aCurrency):
        if aMoney.currency == aCurrency:
            return aMoney.amount

        exchangeRates = {'EUR->USD': 1.2, 'USD->KRW': 1100}
        key = aMoney.currency + '->' + aCurrency
        return aMoney.amount * exchangeRates[key]