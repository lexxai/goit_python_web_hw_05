import asyncio
from datetime import datetime
import platform
from aiopath import AsyncPath
import logging


class CurrencyList:
    cache_file = AsyncPath("logs").joinpath("currency.dat")
    # cache_life = 2 * 60 * 60 * 24  # 2 days
    cache_life = 20

    def __init__(self) -> None:
        self.currency_list: list[str] = [
            "AUD",
            "AZN",
            "BYN",
            "CAD",
            "CHF",
            "CNY",
            "CZK",
            "DKK",
            "EUR",
            "GBP",
            "GEL",
            "HUF",
            "ILS",
            "JPY",
            "KZT",
            "MDL",
            "NOK",
            "PLN",
            "SEK",
            "SGD",
            "TMT",
            "TRY",
            "USD",
            "UZS",
            "XAU",
        ]
        self.is_cached: bool = False

    async def check_cache_life(self):
        if await self.cache_file.is_file():
            modidied = await self.cache_file.stat()
            now_time = datetime.now().timestamp()
            live_seconds = now_time - modidied.st_mtime
            logger.debug(f"{live_seconds=}")
            return live_seconds < self.cache_life
        return self.is_cached

    async def read_cache(self):
        if await self.check_cache_life():
            text = await self.cache_file.read_text(encoding="utf-8-sig")
            if text:
                data = text.strip().split(",")
                if data:
                    self.currency_list = data
                    self.is_cached = True
                    logger.debug("read_cache done")

    async def update_cache(self, data: list[str], forse: bool = False):
        if await self.check_cache_life() and not forse:
            return
        if data != self.currency_list:
            try:
                await self.cache_file.write_text(
                    ",".join(data), encoding="utf-8", newline=""
                )
                self.currency_list = data.copy()
                logger.debug("update_cache done")
                self.is_cached = True
            except OSError as e:
                logger.error(e)


def log_configure():
    FORMAT = "%(asctime)s  %(message)s"
    logging.basicConfig(format=FORMAT, level=logging.DEBUG)


async def main_async():
    global logger
    logger = logging.getLogger(__name__)
    cl = CurrencyList()
    await cl.read_cache()
    logger.info(cl.currency_list)
    await cl.update_cache(["EUR", "GBP"])
    logger.info(cl.currency_list)
    await cl.update_cache(["EUR", "AAA"])
    logger.info(cl.currency_list)
    # await cl.update_cache(["EUR", "BBB"], forse=True)
    # logger.info(cl.currency_list)


if __name__ == "__main__":
    if platform.system() == "Windows":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    log_configure()
    asyncio.run(main_async())
