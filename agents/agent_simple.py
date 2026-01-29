import asyncio


async def receiver(queue: asyncio.Queue):
    print("[Receiver] Starting")
    msg = await queue.get()
    print(f"[Receiver] Got message from {msg['from']}: {msg['body']}")


async def sender(queue: asyncio.Queue):
    print("[Sender] Starting")
    await asyncio.sleep(0.05)
    print("[Sender] Message sent")
    await queue.put({"from": "alice@localhost", "body": "Hello from alice!"})


async def main():
    q = asyncio.Queue()

    r_task = asyncio.create_task(receiver(q))
    await asyncio.sleep(0.01)
    s_task = asyncio.create_task(sender(q))

    await asyncio.gather(r_task, s_task)


if __name__ == "__main__":
    asyncio.run(main())
