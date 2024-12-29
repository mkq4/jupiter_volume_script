from data.models import Token
import random
from loguru import logger
from utils import get_solana_price
SOLANA_TOKEN = Token('sol', 'So11111111111111111111111111111111111111112')
USDC_TOKEN = Token('usdc', 'EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v')
JUP_TOKEN = Token('jup', 'JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN')
GRASS_TOKEN = Token('grass', 'Grass7B4RdKfBCjTKgSqnXkqjwiGvQyFbuSCUJr3XXjs')
PARCL_TOKEN = Token('parcl', '4LLbsb5ReP3yEtYzmXewyGjcir5uXtKFURtaEUVC2AHs')
DRIFT_TOKEN = Token('drift', 'DriFtupJYLTosbwoN8koMbEYSx54aFAVLddWsbksjwg7')
USDT_TOKEN = Token('usdt', 'Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB')
RENDER_TOKEN = Token('render', 'rndrizKT3MK1iimdxRdWabcF7Zg7AR5T4nud4EkHBof')
RAY_TOKEN = Token('ray', '4k3Dyjzvzp8eMZWUXbBCjEvwSkkk59S5iCNLY3QrkX6R')
ZEUS_TOKEN = Token('zeus', 'ZEUS1aR7aX8DFFJf5QjWj2ftDDdNTroMNGo8YoQm3Gq')
ME_TOKEN = Token('me', 'MEFNBXixkEbait3xn9bkm8WsJzXtVsaJEn4c8Sam21u')
WIF_TOKEN = Token('wif', 'EKpQGSJtjMFqKZ9KQanSqYXRcF8fBopzLHYxdM65zcjm')
BONK_TOKEN = Token('bonk', 'DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263')
HNT_TOKEN = Token('hnt', 'hntyVP6YFm1Hg25TN9WGLqM12b8TQmcknKrdu1oxWux')
CHEX_TOKEN = Token('chex', '6dKCoWjpj5MFU5gWDEFdpUUeBasBLK3wLEwhUzQPAa1e')
KMNO_TOKEN = Token('kmno', 'KMNo3nJsBXfcpJTVhZcXLW7RmTwTt4GVFE7suUBo9sS')
JTO_TOKEN = Token('jto', 'jtojtomepa8beP8AuQc6eXt5FriJwfFMwQx2v2f9mCL')
# Список токенов
TOKENS = {
	'sol': SOLANA_TOKEN,
	'usdc': USDC_TOKEN,
	'jup': JUP_TOKEN,
	'grass': GRASS_TOKEN,
	'parcl': PARCL_TOKEN,
	'drift': DRIFT_TOKEN
}

TOKENS_ARR = [USDC_TOKEN, JUP_TOKEN, GRASS_TOKEN, PARCL_TOKEN, DRIFT_TOKEN, USDT_TOKEN]

async def generate_token_way(value: int, start_value: int):
    sol_price = await get_solana_price()
    trades_amount = round(value / (start_value * sol_price)) - 1
    way = [{'sol': SOLANA_TOKEN.address}]
    clear_way = [SOLANA_TOKEN.name]
    
    for _ in range(trades_amount):
        tokens = TOKENS_ARR.copy()
        
        if len(way) > 1:
            last_token_name = list(way[-1].keys())[0]
            tokens = [token for token in tokens if token.name != last_token_name]  # Удаляем последний токен
            
            if not tokens:
                logger.warning("No more tokens to choose from.")
                break
            
            random_item = random.choice(tokens)
        else:
            random_item = random.choice(tokens)
        
        way.append({random_item.name: random_item.address})
        clear_way.append(random_item.name)
  
    way.append({'sol': SOLANA_TOKEN.address})
    clear_way.append(SOLANA_TOKEN.name)
    
    logger.info(f"START SWAPPING | {value}$ | FLIPPING {start_value * sol_price}$ | TRADES: {len(way) - 1}")
    logger.info(f"Created way | {clear_way}")
    return way
