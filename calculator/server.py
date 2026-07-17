import asyncio
import json
import websockets

async def calculator(websocket):
    async for message in websocket:
        data = json.loads(message)

        a = float(data["a"])
        b = float(data["b"])
        op = data["op"]

        if op == "+":
            result = a + b
        elif op == "-":
            result = a - b
        elif op == "*":
            result = a * b
        elif op == "/":
            result = a / b if b != 0 else "Cannot divide by zero"

        await websocket.send(json.dumps({
            "result": result
        }))

async def main():
    async with websockets.serve(calculator, "localhost", 8765):
        print("Server running...")
        await asyncio.Future()

asyncio.run(main())
