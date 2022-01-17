from datetime import datetime
from dateutil.relativedelta import relativedelta


def calculate_cetes(investment: int, term: int, reinvest: int) -> dict:
    """
    Calculates CETES investment, minus taxes (ISR).
    """

    date = datetime.now()

    cetes_rates = {
        28: {"price": 9.95, "rate": 5.52},
        91: {"price": 9.85, "rate": 5.97},
        182: {"price": 9.68, "rate": 6.40},
        364: {"price": 9.33, "rate": 7.03}
    }

    investment_projections = {
        date.year if term == 364 else date.strftime("%Y-%m"): investment
    }

    while reinvest >= 0:
        # Calculating Gross Interest...
        interest_rate = cetes_rates[term]["rate"] / 100
        gross_interest = (investment * term * interest_rate) / 360

        # Calculating ISR (income tax)
        isr_rate = 0.97 / 100
        isr = (investment * isr_rate * term) / 365

        # Calculating liquid interest - ISR (income tax)
        liquid_interest = gross_interest - isr
        investment = investment + round(liquid_interest, 2)

        # The percents that multiply the investments, are a workaround in order to provide better
        # precision when calculating the investment.
        # FIXME: review the formulas that calculate interests,
        #  in order to be compliance with CETES calculator numbers...
        if term == 28:
            date = datetime.now() + relativedelta(month=+1)
            investment_projections[date.strftime("%Y-%m")] = (0.070465546 * investment) / 100 + investment
        elif term == 91:
            date = datetime.now() + relativedelta(month=+3)
            investment_projections[date.strftime("%Y-%m")] = (0.221862184 * investment) / 100 + investment
        elif term == 182:
            date = datetime.now() + relativedelta(month=+6)
            investment_projections[date.strftime("%Y-%m")] = (0.140931092 * investment) / 100 + investment
        else:
            date = date.replace(year=date.year + 1)
            investment_projections[date.year] = round((0.845586552 * investment) / 100 + investment, 2)

        reinvest -= 1

    return investment_projections
