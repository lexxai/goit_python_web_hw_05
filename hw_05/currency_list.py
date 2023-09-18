import asyncio
from datetime import datetime
import platform
from aiopath import AsyncPath
import logging


class CurrencyListCacheAsync:
    cache_file = AsyncPath("logs").joinpath("currency.dat")
    cache_life = 2 * 60 * 60 * 24  # 2 days
    # cache_life = 20
    logger = logging.getLogger(__name__)

    def __init__(self, debug: bool = False) -> None:
        # AUD,AZN,BYN,CAD,CHF,CNY,CZK,DKK,EUR,GBP,GEL,HUF,ILS,JPY,KZT,MDL,NOK,PLN,SEK,SGD,TMT,TRY,UAH,USD,UZS,XAU
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
        self.is_cached: float = None
        self.log_configure(debug)

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return ",".join(self.currency_list)

    def get_currency_list(self) -> list[str]:
        return self.currency_list

    async def get_list_async(self) -> list[str]:
        await self.read_cache()
        return self.currency_list
    
    async def get_str_async(self) -> str:
        await self.read_cache()
        return str(self)

    async def check_cache_life(self):
        result = False
        now_time = datetime.now().timestamp()
        if self.is_cached is not None:
            live_seconds = now_time - self.is_cached
            result = live_seconds < self.cache_life
        # self.logger.debug(f"check_cache_life {result=}")
        return result

    async def read_cache(self):
        state_cache = await self.check_cache_life()
        if not state_cache and await self.cache_file.is_file():
            text = await self.cache_file.read_text(encoding="utf-8-sig")
            if text:
                data = text.strip().split(",")
                if data:
                    self.currency_list = data
                    modidied = await self.cache_file.stat()
                    self.is_cached = modidied.st_mtime
                    self.logger.debug("read_cache done")

    async def update_cache(self, data: list[str], forse: bool = False):
        # self.logger.debug([data, self.currency_list] )
        if data != self.currency_list:
            try:
                await self.cache_file.write_text(
                    ",".join(data), encoding="utf-8", newline=""
                )
                self.currency_list = data.copy()
                self.logger.debug("update_cache done")
                modidied = await self.cache_file.stat()
                self.is_cached = modidied.st_mtime
            except OSError as e:
                self.logger.error(e)

    def log_configure(self, debug: bool = False):
        FORMAT = "%(asctime)s  %(message)s"
        # logging.basicConfig(format=FORMAT, level=logging.DEBUG if debug else logging.INFO)
        self.logger.setLevel(level=logging.DEBUG if debug else logging.INFO)



async def main_async(debug: bool = False):
    # global logger
    # logger = logging.getLogger(__name__)
    cl = CurrencyListCacheAsync(debug = debug)
    # await cl.read_cache()
    cl.logger.info(await cl.get_list_async())
    await cl.update_cache(["EUR", "GBP"])
    cl.logger.info(await cl.get_list_async())
    await cl.update_cache(["EUR", "GBP"])
    cl.logger.info(await cl.get_list_async())
    await cl.update_cache(["USD","PLN","CAD", "EUR"])
    cl.logger.info(await cl.get_list_async())
    # await cl.update_cache(["EUR", "BBB"], forse=True)
    # self.logger.info(cl.currency_list)


if __name__ == "__main__":
    debug = False
    FORMAT = "%(asctime)s  %(message)s"
    logging.basicConfig(format=FORMAT, level=logging.DEBUG if debug else logging.INFO)
    if platform.system() == "Windows":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main_async(debug = debug))
