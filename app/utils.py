import httpx
from fastapi import HTTPException
from datetime import datetime, timezone

COINGECKO_API_URL = "https://api.coingecko.com/api/v3"

async def fetch_cryptocurrency_data(crypto_id: str):
    """Fetch data from CoinGecko."""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{COINGECKO_API_URL}/coins/{crypto_id}")
        if response.status_code == 429:
            raise HTTPException(status_code=429, detail="You have exceeded the request limit. Please wait a moment and try again.")
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch cryptocurrency data")
        
        return response.json()


def extract_cryptocurrency_data(data: dict):
    """Extract relevant data from CoinGecko."""

    try:
        return {
            "id": data["id"],
            "symbol": data["symbol"],
            "name": data["name"],
            "price_usd": data["market_data"]["current_price"]["usd"],
            "market_cap": data["market_data"]["market_cap"]["usd"],
            "volume_24h": data["market_data"]["total_volume"]["usd"],
            "price_change_24h": data["market_data"]["price_change_percentage_24h"],
            "last_updated": convert_iso_to_utc_datetime(data["last_updated"])
        }
    except KeyError as e:
        raise HTTPException(status_code=422, detail=f"Missing required field in API response: {e}")

def convert_iso_to_utc_datetime(iso_string):
    """Convert ISO string format to UTC datetime object."""
    if iso_string.endswith('Z'):
        iso_string = iso_string.replace('Z', '+00:00')
    return datetime.fromisoformat(iso_string)

def convert_unix_to_utc_datetime(timestamp):
    """Convert UNIX timestamp to UTC datetime object."""
    return datetime.fromtimestamp(timestamp, tz=timezone.utc)

def not_found_exception(entity: str, entity_id: str):
    """Return standard 404 exception - crypto not found."""
    return HTTPException(status_code=404, detail=f"{entity} {entity_id} not found")

def already_exists_exception(entity: str, entity_id: str):
    """Return standard 400 exception - crypto is exists in db."""
    return HTTPException(status_code=400, detail=f"{entity} {entity_id} already exists")
