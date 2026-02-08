import asyncio
import sys
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour, CyclicBehaviour
from spade.message import Message


class ReceiverAgent(Agent):
    class RecvBehav(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=3)  # short timeout
            if msg:
          
                sender_jid = getattr(msg.sender, 'bare', None) or str(msg.sender).split('/')[0]
                print(f"[Receiver] Got message from {sender_jid}: {msg.body}")
           
            await self.agent.stop()

    async def setup(self):
        print("[Receiver] Starting")
        self.add_behaviour(self.RecvBehav())


class SenderAgent(Agent):
    class SendBehav(OneShotBehaviour):
        async def run(self):
            msg = Message(to="bob@localhost")
            msg.body = "Hello from alice!"
            await self.send(msg)
            print("[Sender] Message sent")
            # Stop after sending
            await self.agent.stop()

    async def setup(self):
        print("[Sender] Starting")
        self.add_behaviour(self.SendBehav())


async def main():
  
    receiver = ReceiverAgent("bob@localhost", "secret2")
    sender = SenderAgent("alice@localhost", "secret1")

    try:
       
        await receiver.start(auto_register=False)
        
        await asyncio.sleep(0.5)
        await sender.start(auto_register=False)

       
        await asyncio.sleep(2)

    except Exception as e:
        print(f"[error] Exception during agent run: {e}")
        sys.exit(1)

    finally:
        
        await sender.stop()
        await receiver.stop()


if __name__ == "__main__":
    asyncio.run(main())
