import asyncio
import platform
import websockets
import logging
from datetime import datetime

from aiofile import async_open
from aiopath import AsyncPath

try:
    from hw_05.exchange import exchange, get_currency_list_cached_async
except ImportError:
    from exchange import exchange, get_currency_list_cached_async


logs_dir = AsyncPath("logs")
logs_file = logs_dir.joinpath("server_socket.log")


def log_configure():
    FORMAT = "%(asctime)s  %(message)s"
    logging.basicConfig(format=FORMAT, level=logging.ERROR)


async def file_logger_request(msg: str, mgs_type: str = "", ws: websockets = None):
    if ws:
        # Get the client's IP address
        remote_ip, remote_port = ws.remote_address
        # get current datatime
        now_is = datetime.now()
        await logs_dir.mkdir(exist_ok=True, parents=True)
        async with logs_file.open("a") as afp:
            row = f"{now_is}: [{remote_ip}:{remote_port}] {mgs_type} {msg}\n"
            await afp.write(row)


async def websoket_send(mgs, ws):
    await ws.send(mgs)
    await file_logger_request(mgs, ">>>", ws=ws)
    print(f">>> {mgs}")


async def exchange_handler(command_arg: str = None) -> str:
    args = {"days": 2, "currencies": ["USD", "EUR"], "verbose": True}
    try:
        if len(command_arg) > 0:
            args["days"] = int(command_arg[0])
        if len(command_arg) > 1:
            args["currencies"] = command_arg[1].replace(" ","").split(",")
    except ValueError:
        ...
    # exchange external request
    excange_result = await exchange(args)
    return excange_result


async def exchange_cur_list_handler(command_arg: str = None) -> str:
    return get_currency_list_cached_async()


def parse_command(command: str):
    command_line = command.strip()
    if command_line:
        parts = command_line.split()
        command = parts[0].strip().lower()
        command_arg: list[str] = parts[1:]
        return command, command_arg
    return None,[]

LIST_COMMANDS = ["exchange", "list"]

async def exchange_service(websocket: websockets):
    command: str = await websocket.recv()
    print(f"<<< {command}")
    await file_logger_request(command, "<<<", websocket)
    command_action, command_arg = parse_command(command)
    if command_action in LIST_COMMANDS:
        response = f"Your command {command} accepetd. Waiting result..."
    else:
         response = f"Your command {command} not accepetd."
    await websoket_send(response, websocket)
    if command_action == "exchange":
        response = await exchange_handler(command_arg)
    elif command_action == "list":
        response = exchange_cur_list_handler()
    else:
        response = "Your command unknown!"

    await websoket_send(response, websocket)


async def main():
    async with websockets.serve(exchange_service, "0.0.0.0", 8080):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    if platform.system() == "Windows":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    logger = logging.getLogger(__name__)
    log_configure()
    asyncio.run(main())
