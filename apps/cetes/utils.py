import sys
from datetime import datetime


def calculate_cetes(investment: int, term: int, reinvest: int) -> dict:
    """
    Calculates CETES investment, minus taxes (ISR).
    """

    date = datetime.now()

    cetes_rates = {
        28: {"price": 9.95, "rate": 5.52},
        91: {"price": 9.85, "rate": 5.98},
        182: {"price": 9.69, "rate": 6.40},
        364: {"price": 9.37, "rate": 7.03}
    }

    investment_projections = {
        date.year: investment
    }

    while reinvest >= 0:
        # Calculating Interest...
        interest_rate = cetes_rates[term]["rate"] / 100
        interest = (investment * term * interest_rate) / 360
        # print("Investment: ", investment)
        # print("Duration:   ", duration)
        # print("Rate:       ", interest_rate)
        # print("Interest:   ", interest)

        # Calculating Taxes...
        isr_rate = 0.97 / 100
        isr = (investment * isr_rate * term) / 365
        # print("\nISR rate:  ", isr_rate)
        # print("ISR:       ", isr)

        liquid_interest = interest - isr
        investment = investment + round(liquid_interest, 2)

        date = date.replace(year=date.year + 1)

        investment_projections[date.year] = investment

        # print("Liquid interest: ", liquid_interest)
        # print("Gain:            ", investment)

        reinvest -= 1

    return investment_projections
