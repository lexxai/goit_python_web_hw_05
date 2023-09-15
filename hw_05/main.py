import asyncio
from datetime import date, timedelta
import platform
import logging
import json

import aiohttp

try:
    from arg_parse import arguments_parser
except ImportError:
    from hw_05.arg_parse import arguments_parser



async def get_request(url: str, allowed_list: list[str] = None) -> dict | None:
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                if response.status < 400:
                    json = await response.json()
                    if json:
                        json = filter_result(json, allowed_list)
                return json
        except (
            aiohttp.ClientConnectionError,
            aiohttp.ClientConnectorCertificateError,
        ) as e:
            logger.error( f"Error open {url}: {e}")
        except Exception as e:
            logger.error(e)


def filter_result(data_json: dict, allowed_list:list[str] = None) -> dict:
    if allowed_list is None:
        allowed_list = ["EUR","USD"]
    result={}
    if data_json:
        date = data_json.get("date")
        if date:
            filtered_rate = {}   
            # cl = []
            exch_rate =  data_json.get("exchangeRate")
            for er in exch_rate:
                currency = er.get("currency")
                # cl.append(currency)
                # logger.info(currency)
                if currency in allowed_list:
                    filtered_rate[currency] = {
                        "sale": er.get("saleRateNB"),
                        "purchase": er.get("purchaseRateNB"),
                    }
                # optimieze filter all found, stop
                if len(filtered_rate) >= len(allowed_list):
                    break
        result[date]=filtered_rate
        # print(cl)
        return result         


def date_calc(days: int) -> date:
    td = timedelta(days=days)
    date_c = date.today() - td
    return date_c.strftime("%d.%m.%Y")


async def get_currencies(days: int, currencies: list[str]) -> str:
    tasks = []
    for d in range(1,days+1):
        date_back = date_calc(d)
        logger.info(f"Get request for: {date_back}")
        bank_api = f"https://api.privatbank.ua/p24api/exchange_rates?json&date={date_back}"
        task = asyncio.create_task(get_request(bank_api, currencies))
        tasks.append(task)
    # waiting all reults
    logger.info(f"Waing result for {len(tasks)} requests")
    results = await asyncio.gather(*tasks, return_exceptions=True)
    # logger.info(f"API result: {results}")
    return(json.dumps(results, indent=2))


async def main(args):
    days = args.get("days")
    currencies = args.get("currencies")
    logger.info(f"Get request for {days} days")
    result = await get_currencies(days, currencies)
    print(result)


if __name__ == "__main__":
    if platform.system() == "Windows":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    FORMAT = "%(asctime)s  %(message)s"
    logging.basicConfig(format=FORMAT, level=logging.INFO)
    logger = logging.getLogger(__name__)

    args = arguments_parser()
    asyncio.run(main(args), debug=False)
