import asyncio
from datetime import date, timedelta
import platform
import logging
import json

import aiohttp
from tqdm import tqdm
from tqdm.contrib.logging import logging_redirect_tqdm

try:
    from arg_parse import arguments_parser, validate_args
except ImportError:
    from hw_05.arg_parse import arguments_parser, validate_args



async def get_request(url: str, allowed_list: list[str] = None) -> dict | None:
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                json = None
                if response.status < 400:
                    json = await response.json()
                else:
                    logger.error(f"{url}, response code:{response.status}")
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
                        "sale": er.get("saleRate"),
                        "purchase": er.get("purchaseRate"),
                    }
                # optimieze filter all found, stop
                if len(filtered_rate) >= len(allowed_list):
                    break
        result[date]=filtered_rate
        # print(cl)
        return result         
    
    
def filter_results(list_data: list[dict], allowed_list:list[str] = None) -> dict:
    result = []
    for data in list_data:
        filterd_result=filter_result(data, allowed_list)
        if filterd_result:
            result.append(filterd_result)
    return result


def date_calc(days: int) -> date:
    td = timedelta(days=days)
    date_c = date.today() - td
    return date_c.strftime("%d.%m.%Y")


async def get_currencies(days: int) -> str:
    tasks = []
    for d in range(1,days+1):
        date_back = date_calc(d)
        logger.info(f"Get request for: {date_back}")
        bank_api = f"https://api.privatbank.ua/p24api/exchange_rates?json&date={date_back}"
        task = asyncio.create_task(get_request(bank_api))
        tasks.append(task)
    # waiting all reults
    logger.info(f"Waing result for {len(tasks)} requests")
    if logger.getEffectiveLevel() == logging.INFO:
        with logging_redirect_tqdm():
            results = [await f
                    for f in tqdm(asyncio.as_completed(tasks), total=len(tasks))]
    else:
        results = await asyncio.gather(*tasks, return_exceptions=True)
    # logger.info(f"API result: {results}")
    return(results)



async def exchange(args: dict = None):
    if args is None:
        args = {
            "days": 2,
            "currencies": ["USD","EUR"],
            "verbose" : False
        }
    if not validate_args(args):
        logger.error("Bad arguments value")
        return "Bad arguments value"
    days = args.get("days", 2)
    currencies = args.get("currencies", ["USD","EUR"])
    verbose = args.get("verbose", False)
    if not verbose:
        logger.setLevel(logging.ERROR)
    logger.info(f"Get request for {days} days")
    results = await get_currencies(days)
    results = filter_results(results, currencies)
    if len(results) != days:
        logger.error(f"Some days was skipped, retuned only {len(results)} records from {days}")
    jonson_rich = json.dumps(results, indent=2)
    return jonson_rich


async def main_async(args: dict = None):
    jonson_rich = await exchange(args)
    print(jonson_rich)



logger = logging.getLogger(__name__)


def main(init_arg: dict = None):
    if platform.system() == "Windows":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    FORMAT = "%(asctime)s  %(message)s"
    logging.basicConfig(format=FORMAT, level=logging.INFO)
    args = arguments_parser()
    try:
        asyncio.run(main_async(args), debug=False)
    except KeyboardInterrupt:
        logger.info("Keyboard Interrupt")


if __name__ == "__main__":
    main()