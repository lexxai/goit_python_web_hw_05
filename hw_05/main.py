import asyncio
from argparse import ArgumentParser, ArgumentError
from datetime import date, timedelta
import platform
import logging

import aiohttp


currency_list = {
    "USD": "долар США",
    "EUR": "євро",
    "CHF": "швейцарський франк",
    "GBP": "британський фунт",
    "PLZ": "польський злотий",
    "SEK": "шведська крона",
    "XAU": "золото",
    "CAD": "канадський долар",
}


answer_code = {
    "baseCurrency": "Базова валюта",
    "currency": "Валюта угоди",
    "saleRateNB": " Курс продажу НБУ",
    "purchaseRateNB": "Курс купівлі НБУ",
    "saleRate": "Курс продажу ПриватБанку",
    "purchaseRate": "Курс купівлі ПриватБанку",
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


async def get_request(url: str):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                if response.status < 400:
                    json = await response.json()
                return json
        except (
            aiohttp.ClientConnectionError,
            aiohttp.ClientConnectorCertificateError,
        ) as e:
            logger.error( f"Error open {url}: {e}")
        except Exception as e:
            logger.error(e)


def date_calc(days: int) -> date:
    td = timedelta(days=days)
    date_c = date.today() - td
    return date_c.strftime("%d.%m.%Y")


def filter_result(data: dict):
    allowed = c


async def main(args):
    days = args.get("days")
    logger.info(f"Get request for {days} days")
    date_back = date_calc(days)
    BANK_API = f"https://api.privatbank.ua/p24api/exchange_rates?json&date={date_back}"
    result = await get_request(BANK_API)
    logger.info(f"API result: {result}")


if __name__ == "__main__":
    if platform.system() == "Windows":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    FORMAT = "%(asctime)s  %(message)s"
    logging.basicConfig(format=FORMAT, level=logging.INFO)
    logger = logging.getLogger(__name__)

    args = arguments_parser()
    asyncio.run(main(args), debug=False)
