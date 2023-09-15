
import asyncio
import platform
import websockets
import logging

try:
    from hw_05.exchange import exchange 
except ImportError:
    from main import exchange 


async def exchange_service(websocket):
    command:str = await websocket.recv()
    print(f"<<< {command}")
    if command.strip().lower() == "exchange":
        excange_result = await exchange()
        response = f"Your command {command} accepetd. Result:\n {excange_result}"
    else:
        response = "Your command unknown!"

    await websocket.send(response)
    print(f">>> {response}")


async def main():
    async with websockets.serve(exchange_service, "localhost", 8765):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    if platform.system() == "Windows":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    logger = logging.getLogger(__name__)
    asyncio.run(main())
