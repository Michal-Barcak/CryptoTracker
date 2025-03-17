from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Cryptocurrency(BaseModel):
    id: str
    symbol: str
    name: str
    price_usd: float
    market_cap: Optional[float] = None
    volume_24h: Optional[float] = None
    price_change_24h: Optional[float] = None
    last_updated: Optional[datetime] = None

    class Config:
        orm_mode = True
