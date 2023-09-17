import asyncio
from datetime import datetime
import platform
from aiopath import AsyncPath
import logging


class CurrencyListCache:
    cache_file = AsyncPath("logs").joinpath("currency.dat")
    cache_life = 2 * 60 * 60 * 24  # 2 days
    # cache_life = 20
    logger = logging.getLogger(__name__)

    def __init__(self, debug: bool = False) -> None:
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
        self.log_configure(debug)

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return ",".join(self.currency_list)

    def get_currency_list(self) -> list[str]:
        return self.currency_list

    async def check_cache_life(self):
        if await self.cache_file.is_file():
            modidied = await self.cache_file.stat()
            now_time = datetime.now().timestamp()
            live_seconds = now_time - modidied.st_mtime
            self.logger.debug(f"{live_seconds=}")
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
                    self.logger.debug("read_cache done")

    async def update_cache(self, data: list[str], forse: bool = False):
        # self.logger.debug([data, self.currency_list] )
        if data != self.currency_list:
            if await self.check_cache_life() and not forse:
                return
            try:
                await self.cache_file.write_text(
                    ",".join(data), encoding="utf-8", newline=""
                )
                self.currency_list = data.copy()
                self.logger.debug("update_cache done")
                self.is_cached = True
            except OSError as e:
                self.logger.error(e)

    def log_configure(self, debug: bool = False):
        FORMAT = "%(asctime)s  %(message)s"
        logging.basicConfig(format=FORMAT, level=logging.DEBUG if debug else logging.INFO)


async def main_async(debug: bool = False):
    # global logger
    # logger = logging.getLogger(__name__)
    cl = CurrencyListCache(debug = debug)
    await cl.read_cache()
    cl.logger.info(cl)
    await cl.update_cache(["EUR", "GBP"])
    cl.logger.info(cl)
    await cl.update_cache(["EUR", "AAA"])
    cl.logger.info(cl)
    # await cl.update_cache(["EUR", "BBB"], forse=True)
    # self.logger.info(cl.currency_list)


if __name__ == "__main__":
    if platform.system() == "Windows":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main_async(debug = True))
