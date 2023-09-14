import asyncio
from argparse import ArgumentParser
import platform
import logging

import aiohttp


def arguments_parser():
    ap = ArgumentParser(description="Get currency rate from Bank")
    ap.add_argument(
        "--days",
        help="How many datys need to show reqults, default: 2",
        default=2,
        type=int,
    )

    args = vars(ap.parse_args())
    return args


async def main(args):
    days = args.get("days")
    logger.info(f"Get request for {days} days")
    await asyncio.sleep(1)


if __name__ == "__main__":
    if platform.system() == "Windows":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    FORMAT = "%(asctime)s  %(message)s"
    logging.basicConfig(format=FORMAT, level=logging.INFO)
    logger = logging.getLogger(__name__)

    args = arguments_parser()
    asyncio.run(main(args), debug=False)
