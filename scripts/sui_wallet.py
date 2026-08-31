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
# JSON-RPC on public fullnodes is deprecated (https://docs.sui.io/develop/accessing-data/json-rpc-migration) - use GraphQL RPC instead.
SUI_GRAPHQL = "https://graphql.mainnet.sui.io/graphql"
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


BALANCES_QUERY = """
query ($wallet: SuiAddress!, $after: String) {
  address(address: $wallet) {
    balances(first: 50, after: $after) {
      pageInfo { hasNextPage endCursor }
      nodes { coinType { repr } totalBalance }
    }
  }
}
"""

COIN_METADATA_QUERY = """
query ($coinType: String!) {
  coinMetadata(coinType: $coinType) { decimals symbol name }
}
"""


def graphql_call(query: str, variables: dict) -> dict:
    """Make a GraphQL call to SUI node."""
    result = http_post(SUI_GRAPHQL, {"query": query, "variables": variables})
    if "errors" in result:
        raise RuntimeError(result["errors"][0].get("message", "GraphQL error"))
    return result.get("data") or {}


def get_all_coins(wallet: str) -> list:
    """Get all coin balances from SUI wallet via GraphQL (paginated, 50/page)."""
    coins = []
    after = None
    while True:
        data = graphql_call(BALANCES_QUERY, {"wallet": wallet, "after": after})
        balances = (data.get("address") or {}).get("balances") or {}
        for node in balances.get("nodes", []):
            coins.append(
                {
                    "coinType": (node.get("coinType") or {}).get("repr", ""),
                    "balance": node.get("totalBalance", 0),
                }
            )
        page_info = balances.get("pageInfo") or {}
        if not page_info.get("hasNextPage"):
            break
        after = page_info.get("endCursor")
    return coins


def get_coin_metadata(coin_type: str) -> dict:
    """Get coin metadata including decimals from SUI GraphQL RPC."""
    data = graphql_call(COIN_METADATA_QUERY, {"coinType": coin_type})
    return data.get("coinMetadata") or {}


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
    if len(sys.argv) < 2:
        raise RuntimeError("wallet address not provided as argv[1]")
    wallet = sys.argv[1]

    # Get all coins from wallet
    coins = get_all_coins(wallet)

    # Aggregate balances by coin type
    balances = {}
    for coin in coins:
        coin_type = coin.get("coinType", "")
        balance = int(coin.get("balance", 0))
        if balance > 0:
            balances[coin_type] = balances.get(coin_type, 0) + balance

    if not balances:
        print(json.dumps({"total_usd": 0, "tokens": [], "token_count": 0, "wallet": wallet[:10] + "..." + wallet[-6:]}))
        return

    # Get prices and decimals from DeFi Llama (single API call)
    llama_data = get_defillama_prices(list(balances.keys()))

    # For tokens not in DeFi Llama, get metadata from SUI GraphQL RPC
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
        "wallet": wallet[:10] + "..." + wallet[-6:],
    }

    print(json.dumps(output))


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        # Return error state for Home Assistant
        print(json.dumps({"total_usd": 0, "error": str(e), "tokens": [], "token_count": 0}))
        sys.exit(1)
