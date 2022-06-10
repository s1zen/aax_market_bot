import hmac, hashlib, time, aiohttp

from dataclasses import dataclass, field

@dataclass
class Proxy:
    ip: str
    port: int
    
    login: str
    password: str
    
    def proxy(self) -> str:
        return f"http://{self.login}:{self.password}@{self.ip}:{self.port}"
    
@dataclass
class Order:
    id: str
    purchase_price: float
    expected_profit_percentage: int
    selling_price: float = field(init=False)

    def __post_init__(self):
        self.selling_price = self.purchase_price + (self.purchase_price / 100 * self.expected_profit_percentage)

@dataclass
class MarketBot:
    api_key: str
    api_secret: str
    params = {"symbol":"BTCUSDT"}
    api_url: str = "https://api.aax.com"
    

    async def get_order(self, proxy: Proxy.proxy, order: Order) -> dict:
        proxy: str
        
        path = "/v2/futures/trades"
        verb = "GET"
        nonce = str(int(1000 * time.time()))
        data = ''
        signature = hmac.new(self.api_secret.encode(), (nonce + ':' + verb + path + data).encode(), hashlib.sha256).hexdigest()
        
        headers = {
            "X-ACCESS-NONCE": nonce,
            "X-ACCESS-KEY": self.api_key,
            "X-ACCESS-SIGN": signature
        }
        
        
        async with aiohttp.ClientSession() as session:
            async with session.get(self.api_url + path, headers=headers, proxy=proxy) as response:
                data = await response.json()
                
        return Order(data["data"]["list"][0]["orderID"], float(data["data"]["list"][0]["filledPrice"]), 2)
    
    async def close_order(self, order: Order):
        path = f"/v2/futures/orders/cancel/{order.id}"
        
        async with aiohttp.ClientSession() as session:
            await session.delete(self.api_url + path, proxy=proxy)