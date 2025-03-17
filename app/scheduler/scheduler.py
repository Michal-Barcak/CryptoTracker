from apscheduler.schedulers.background import BackgroundScheduler
import httpx
import asyncio
from datetime import datetime, timezone
from .. import models
from ..database import get_db
from ..utils import convert_unix_to_utc_datetime
import ssl
import certifi

scheduler = BackgroundScheduler()

async def update_all_cryptocurrencies():
    """ Background function for update all crypto in local db. """
    db = next(get_db())
    try:
        all_cryptos = models.Cryptocurrency.all(db)
        
        if not all_cryptos:
            print("No cryptocurrencies in database to update")
            return
            
        crypto_ids = ",".join([crypto.id for crypto in all_cryptos])
        
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            "ids": crypto_ids,
            "vs_currencies": "usd",
            "include_market_cap": "true",
            "include_24hr_vol": "true",
            "include_24hr_change": "true",
            "include_last_updated_at": "true"
        }
        
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        
        async with httpx.AsyncClient(verify=ssl_context) as client:
            response = await client.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                
                for crypto in all_cryptos:
                    if crypto.id in data:
                        coin_data = data[crypto.id]
                        
                        last_updated_at = coin_data.get("last_updated_at")
                        
                        if last_updated_at is not None:
                            last_updated = convert_unix_to_utc_datetime(last_updated_at)
                        else:
                            last_updated = datetime.now(timezone.utc)
                            print(f"Warning: Missing last_updated_at for {crypto.id}, using current time")
                        
                        update_data = {
                            "price_usd": coin_data["usd"],
                            "market_cap": coin_data.get("usd_market_cap"),
                            "volume_24h": coin_data.get("usd_24h_vol"),
                            "price_change_24h": coin_data.get("usd_24h_change"),
                            "last_updated": last_updated
                        }
                        models.Cryptocurrency.update(db, record_id=crypto.id, **update_data)
                
                print(f"Successfully updated {len(all_cryptos)} cryptocurrencies")
            else:
                print(f"API request failed with status {response.status_code}")
    except Exception as e:
        print(f"Error updating cryptocurrencies: {str(e)}")
    finally:
        db.close()

def run_update_task():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(update_all_cryptocurrencies())
    loop.close()

def init_scheduler():
    scheduler.add_job(run_update_task, 'interval', seconds=30)
    scheduler.start()
