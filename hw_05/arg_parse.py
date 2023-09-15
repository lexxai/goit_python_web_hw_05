from argparse import ArgumentParser, ArgumentError

currency_list = ['AUD', 'AZN', 'BYN', 'CAD', 'CHF', 'CNY', 'CZK', 'DKK', 'EUR', 'GBP', 
                 'GEL', 'HUF', 'ILS', 'JPY', 'KZT', 'MDL', 'NOK', 'PLN', 'SEK', 'SGD', 
                 'TMT', 'TRY', 'USD', 'UZS', 'XAU']

def validate_args(args):
    try:
        check_days(args.get("days"))
        check_currency(args.get("currencies"))
        return True 
    except ArgumentError:
       return False


def get_currency_list():
    return ",".join(currency_list)


def check_days(value: str) -> int:
    if 1<= int(value) <=10:
        return int(value)
    raise ArgumentError(message="Wrong value, must be 1..10", argument=None)


def check_currency(value: str|list) -> list[str]:
    if isinstance(value, str):
        values = set(value.strip().split(","))
    else:
        values = value
    if all(item in currency_list for item in values):
        return list(values)
    raise ArgumentError(message="Wrong list of currency", argument=None)


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
    ap.add_argument(
        "--verbose",
        help="print deailed log",
        action="store_true"
    )

    args = vars(ap.parse_args())
    return args