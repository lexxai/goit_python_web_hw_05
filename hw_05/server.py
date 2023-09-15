
import asyncio
import platform
import websockets
import logging

try:
    from hw_05.exchange import exchange 
except ImportError:
    from exchange import exchange 


async def exchange_service(websocket):
    command:str = await websocket.recv()
    print(f"<<< {command}")
    command_line = command.strip()
    commands=command_line.split()
    command = commands[0]
    command_arg = commands[1:]
    if command.strip().lower() == "exchange":
        args = {
            "days": 2,
            "currencies": ["USD","EUR"],
            "verbose" : True
        }
        try:
            if len(command_arg) > 0:
                args["days"] = int(command_arg[0])
            if len(command_arg) > 1:
                args["currencies"] = command_arg[1].split(",")
        except ValueError:
            ...
        response = f"Your command {command} accepetd. Waiting result..."
        await websocket.send(response)
        excange_result = await exchange(args)
        response = excange_result
    else:
        response = "Your command unknown!"

    await websocket.send(response)
    print(f">>> {response}")


async def main():
    async with websockets.serve(exchange_service, "localhost", 8080):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    if platform.system() == "Windows":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    logger = logging.getLogger(__name__)
    asyncio.run(main())
