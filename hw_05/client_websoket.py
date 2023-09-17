import asyncio
import platform
import websockets


async def hello():
    uri = "ws://localhost:8080"
    try:
        async with websockets.connect(uri) as websocket:
            while True:
                try:
                    command = input("What's your command (exchange, list ,exit)? ")
                    if command.strip().lower() == "exit":
                        break
                except (KeyboardInterrupt, EOFError):
                    break
                if command:
                    try:
                        await websocket.send(command)
                        print(f">>> {command}")

                        response = await websocket.recv()
                        print(f"<<< {response}")

                        response = await websocket.recv()
                        print(f"<<< {response}")
                    except websockets.exceptions.ConnectionClosedOK as e:
                         print("ERROR", e)

    except OSError as e:
        print("ERROR", e)

if __name__ == "__main__":
    if platform.system() == "Windows":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(hello())
