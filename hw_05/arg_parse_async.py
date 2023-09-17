from argparse import ArgumentParser, ArgumentError
import asyncio
import platform
from  typing import Coroutine
try:
    from hw_05.currency_list import CurrencyListCacheAsync
except ImportError:
    from currency_list import CurrencyListCacheAsync

# currency_list = ['AUD', 'AZN', 'BYN', 'CAD', 'CHF', 'CNY', 'CZK', 'DKK', 'EUR', 'GBP', 
#                  'GEL', 'HUF', 'ILS', 'JPY', 'KZT', 'MDL', 'NOK', 'PLN', 'SEK', 'SGD', 
#                  'TMT', 'TRY', 'USD', 'UZS', 'XAU']

def validate_args(args: dict) -> tuple[bool, str]:
    try:
        check_days(args.get("days"))
        check_currency(args.get("currencies"))
        return True, "" 
    except ArgumentError as e:
       return False, e.message


def get_currency_list_cached():
    # return ",".join(currency_list)
    return asyncio.run(currency_list.get_list_async())
    # return currency_list

def get_currencies_str_cached():
    # return ",".join(currency_list)
    return asyncio.run(currency_list.get_str_async())
    # return currency_list

def get_currency_list_cached_async() -> Coroutine:
    return currency_list.get_str_async()


def check_days(value: str) -> int:
    if 1<= int(value) <=10:
        return int(value)
    raise ArgumentError(message="Wrong value, must be 1..10", argument=None)


def check_currency(value: str|list) -> list[str]:
    if isinstance(value, str):
        values = set(value.strip().split(","))
    else:
        values = value
    if all(item in currency_list.get_currency_list() for item in values):
        return list(values)
    raise ArgumentError(message="Wrong list of currency", argument=None)


async def arguments_parser():
    ap = ArgumentParser(
        description=f"Get exchangeRate from Bank: {await currency_list.get_str_async()}"
    )
    ap.add_argument(
        "--days",
        help="How many datys need to show reqults, max. 10 days, default: 2",
        default=2,
        type=check_days,
    )
    ap.add_argument(
        "--currencies",
        help=f'currencies for list. Allowed: items "{await currency_list.get_str_async()}". Please use coma separeted list. default: EUR,USD ',
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



currency_list =  CurrencyListCacheAsync()

# asyncio.run(currency_list.read_cache())

if __name__ == "__main__":
    if platform.system() == "Windows":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
#     asyncio.run(currency_list.read_cache())
# else:
#     currency_list.read_cache()