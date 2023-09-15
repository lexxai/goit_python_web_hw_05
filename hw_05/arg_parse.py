from argparse import ArgumentParser, ArgumentError

currency_list = {
    "USD": "долар США",
    "EUR": "євро",
    "CHF": "швейцарський франк",
    "GBP": "британський фунт",
    "PLN": "польський злотий",
    "SEK": "шведська крона",
    "XAU": "золото",
    "CAD": "канадський долар",
}

def get_currency_list():
    return ",".join(currency_list.keys())

def check_days(value: str):
    if 1<= int(value) <=10:
        return int(value)
    raise ArgumentError

def check_currency(value: str):
    values = set(value.strip().split(","))
    if all(item in currency_list.keys() for item in values):
        return list(values)
    raise ArgumentError

def arguments_parser():
    ap = ArgumentParser(
        description=f"Get exchangeRate from Bank: {get_currency_list()}"
    )
    ap.add_argument(
        "--days",
        help="How many datys need to show reqults, max. 10 days, default: 2",
        default=2,
        type=check_days,
    )
    ap.add_argument(
        "--currencies",
        help=f'currencies for list. Allowed: items "{get_currency_list()}". Please use coma separeted list. default: EUR,USD ',
        default="EUR,USD",
        type=check_currency,
    )

    args = vars(ap.parse_args())
    return args