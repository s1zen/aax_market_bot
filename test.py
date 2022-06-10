import asyncio

from services import Proxy, MarketBot, Order
from pprint import pprint

async def main():
    proxy = Proxy().proxy()
    Bot = MarketBot()
    order = await Bot.get_order(proxy, Order)
    pprint(order)
    
    
if __name__ == "__main__":   
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())