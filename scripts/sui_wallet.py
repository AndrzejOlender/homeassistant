#!/usr/bin/env python3
"""
SUI Wallet Portfolio Tracker for Home Assistant
Fetches all tokens from a SUI wallet and calculates total USD value.
Uses DeFi Llama for prices (single source, no API key needed).
"""
import json
import sys
import urllib.request
import urllib.error

# Configuration
WALLET = "0xcf50d5f093fd78b0e3f785e792ee67ffa0fafbd5642e672042f656c7c7ef724b"
SUI_RPC = "https://fullnode.mainnet.sui.io:443"
DEFILLAMA_API = "https://coins.llama.fi/prices/current"
TIMEOUT = 30


def http_post(url: str, data: dict, timeout: int = TIMEOUT) -> dict:
    """Make HTTP POST request."""
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def http_get(url: str, timeout: int = TIMEOUT) -> dict:
    """Make HTTP GET request."""
    req = urllib.request.Request(url, headers={"User-Agent": "HomeAssistant/SUI-Wallet"})
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def rpc_call(method: str, params: list) -> dict:
    """Make a JSON-RPC call to SUI node."""
    return http_post(SUI_RPC, {"jsonrpc": "2.0", "id": 1, "method": method, "params": params})


def get_all_coins(wallet: str) -> list:
    """Get all coins from SUI wallet via RPC."""
    result = rpc_call("suix_getAllCoins", [wallet])
    return result.get("result", {}).get("data", [])


def get_coin_metadata(coin_type: str) -> dict:
    """Get coin metadata including decimals from SUI RPC."""
    result = rpc_call("suix_getCoinMetadata", [coin_type])
    return result.get("result") or {}


def get_defillama_prices(coin_types: list) -> dict:
    """
    Get prices and decimals from DeFi Llama.
    Returns dict: {coin_type: {"price": float, "decimals": int, "symbol": str}}
    """
    if not coin_types:
        return {}

    # Build DeFi Llama coin IDs (format: sui:0x...::module::SYMBOL)
    llama_ids = [f"sui:{ct}" for ct in coin_types]
    url = f"{DEFILLAMA_API}/{','.join(llama_ids)}"

    try:
        data = http_get(url)
        coins = data.get("coins", {})

        result = {}
        for coin_type in coin_types:
            llama_key = f"sui:{coin_type}"
            if llama_key in coins:
                coin_data = coins[llama_key]
                result[coin_type] = {
                    "price": coin_data.get("price", 0),
                    "decimals": coin_data.get("decimals", 9),
                    "symbol": coin_data.get("symbol", coin_type.split("::")[-1]),
                }
        return result
    except Exception as e:
        return {}


def main():
    # Get all coins from wallet
    coins = get_all_coins(WALLET)

    # Aggregate balances by coin type
    balances = {}
    for coin in coins:
        coin_type = coin.get("coinType", "")
        balance = int(coin.get("balance", 0))
        if balance > 0:
            balances[coin_type] = balances.get(coin_type, 0) + balance

    if not balances:
        print(json.dumps({"total_usd": 0, "tokens": [], "token_count": 0, "wallet": WALLET[:10] + "..." + WALLET[-6:]}))
        return

    # Get prices and decimals from DeFi Llama (single API call)
    llama_data = get_defillama_prices(list(balances.keys()))

    # For tokens not in DeFi Llama, get metadata from SUI RPC
    for coin_type in balances.keys():
        if coin_type not in llama_data:
            metadata = get_coin_metadata(coin_type)
            llama_data[coin_type] = {
                "price": 0,
                "decimals": metadata.get("decimals", 9),
                "symbol": metadata.get("symbol", coin_type.split("::")[-1]),
                "name": metadata.get("name"),
            }

    # Calculate totals
    total_usd = 0
    tokens = []

    for coin_type, raw_balance in balances.items():
        info = llama_data.get(coin_type, {})
        symbol = info.get("symbol", coin_type.split("::")[-1])
        decimals = info.get("decimals", 9)
        price_usd = info.get("price", 0)

        # Calculate actual balance
        balance = raw_balance / (10**decimals)

        # Calculate value
        value_usd = balance * price_usd
        total_usd += value_usd

        tokens.append(
            {
                "symbol": symbol,
                "balance": round(balance, 6),
                "price_usd": round(price_usd, 8),
                "value_usd": round(value_usd, 2),
            }
        )

    # Sort by value descending
    tokens.sort(key=lambda x: x["value_usd"], reverse=True)

    # Output JSON for Home Assistant
    output = {
        "total_usd": round(total_usd, 2),
        "tokens": tokens,
        "token_count": len(tokens),
        "wallet": WALLET[:10] + "..." + WALLET[-6:],
    }

    print(json.dumps(output))


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        # Return error state for Home Assistant
        print(json.dumps({"total_usd": 0, "error": str(e), "tokens": [], "token_count": 0}))
        sys.exit(1)
