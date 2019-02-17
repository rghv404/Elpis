import asyncio
import websockets


async def hello_world(websock, path):
    name = await websock.recv()
    print("Name: {}, Path: {}".format(name, path))
    while name is not None:
        name = await websock.recv()
        print("Name: {}, Path: {}".format(name, path))
        await websock.send("Hello {}".format(name))
    return True

if __name__ == "__main__":
    start_server = websockets.serve(hello_world, "localhost", 8000)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
