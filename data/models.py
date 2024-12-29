class Wallet:
    def __init__(self, address: str, private_key: str = '', seed: str = '', proxy: str = '', amount: str = '', user_agent=''):
        self.address = address
        self.private_key = private_key
        self.proxy = proxy
        self.amount = amount
        self.user_agent = user_agent

    def __str__(self):
        return (f"Wallet("
                f"address='{self.address}', "
                f"private_key='{self.private_key[:3]}***{self.private_key[-3:]}'"
                f"proxy='{self.proxy}"
                f")")
        
        
class Swap:
    def __init__(self, amount: int, from_token: str, to_token: str):
        self.amount = amount
        self.from_token = from_token
        self.to_token = to_token
    
    def __str__(self):
        return (f"TRADE | {self.from_token} to {self.to_token} | {self.amount}")
    
class Token:
    def __init__(self, name, address):
        self.name = name
        self.address = address