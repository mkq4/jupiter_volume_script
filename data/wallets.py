import requests
import random
from fake_useragent import FakeUserAgent
from solathon import Client, PublicKey, Keypair
from data.models import Wallet
from data.config import AMOUNT_RANGE
wallets_path = './private_keys.txt'
proxie_path = './proxies.txt'

WALLETS = []

client = Client("https://api.mainnet-beta.solana.com")


def get_pc_user_agent():
    ua = FakeUserAgent()
    user_agent = ua.random
    while "Mobile" in user_agent or "Android" in user_agent:
        user_agent = ua.random  # Генерируем новый, если текущий для мобильных устройств
    return user_agent

def get_amount(wallet_address: str):
    try:
        public_key = PublicKey(wallet_address)
        balance_lamports = client.get_balance(public_key)
        balance_sol = balance_lamports / 1_000_000_000
        percent_from_amount = random.randint(AMOUNT_RANGE[0], AMOUNT_RANGE[1])
        amount = balance_sol * (percent_from_amount / 100)
        amount = str(round(amount, 2))
        return amount
    
    except Exception as e:
        print(f"Error getting balance for {wallet_address}: {e}")
        return None

def load_proxies(file_path):
    with open(file_path, 'r') as f:
        proxies = f.readlines()
    return [proxy.strip() for proxy in proxies]

def load_wallets(wallet_file_path, proxy_file_path):
    proxies = load_proxies(proxy_file_path)
    
    with open(wallet_file_path, 'r') as f:
        private_keys = f.readlines()
    
    for i, private_key in enumerate(private_keys):
        private_key = private_key.strip()
        
        wallet = Keypair.from_private_key(private_key)
        address = str(wallet.public_key)
        
        proxy = proxies[i % len(proxies)]  # Привязка прокси по кругу
        amount = get_amount(address)
        user_agent = get_pc_user_agent()
        wallet_obj = Wallet(address=address, private_key=private_key, proxy=proxy, amount=amount, user_agent=user_agent)
        WALLETS.append(wallet_obj)
load_wallets(wallets_path, proxie_path)