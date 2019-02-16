import asyncio
import websockets


async def hello_world(websock, path):
    name = await websock.recv()
    print("Name: {}".format(name))
    await websock.send("Hello {}".format(name))

if __name__ == "__main__":
    start_server = websockets.serve(hello_world, "localhost", 8000)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
