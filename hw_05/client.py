import asyncio
import platform
import websockets




async def hello():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        while True:
            try:
                command = input("What's your command (exchange, exit)? ")
                if command.strip().lower() == "exit":
                    break
            except (KeyboardInterrupt, EOFError):
                break
            if command:
                await websocket.send(command)
                print(f">>> {command}")

                response = await websocket.recv()
                print(f"<<< {response}")


if __name__ == "__main__":
    if platform.system() == "Windows":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(hello())
