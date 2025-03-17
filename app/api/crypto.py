from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import models
from ..database import get_db
from datetime import datetime
from ..utils import (
    fetch_cryptocurrency_data, 
    extract_cryptocurrency_data, 
    not_found_exception,
    already_exists_exception
)

router = APIRouter()

@router.get("/cryptocurrencies", summary="Get all cryptocurrencies from database")
def get_cryptocurrencies(db: Session = Depends(get_db)):
    """ Get all cryptocurrencies stored in the local database. """
    return models.Cryptocurrency.all(db, order_by=models.Cryptocurrency.id)

@router.get("/cryptocurrency/{crypto_id}", summary="Get cryptocurrency by ID from database")
def get_cryptocurrency(crypto_id: str, db: Session = Depends(get_db)):
    """ Get specific cryptocurrency from the local database. """
    db_crypto = models.Cryptocurrency.get(db, crypto_id)

    if not db_crypto:
        raise not_found_exception("Cryptocurrency", crypto_id)

    return db_crypto


@router.get("/cryptocurrency/info/{crypto_id}", summary="Get cryptocurrency info from CoinGecko")
async def get_cryptocurrency_info(crypto_id: str, db: Session = Depends(get_db)):
    """ Fetch cryptocurrency information from CoinGecko API. """
    exists_in_db = models.Cryptocurrency.exists(db, crypto_id)

    data = await fetch_cryptocurrency_data(crypto_id)
    crypto_data = extract_cryptocurrency_data(data)
    
    if isinstance(crypto_data["last_updated"], datetime):
        crypto_data["last_updated"] = crypto_data["last_updated"].isoformat()
    
    return {
        **crypto_data,
        "exists_in_db": exists_in_db
    }


@router.post("/cryptocurrency", summary="Save cryptocurrency to database")
async def create_cryptocurrency(crypto_id: str, db: Session = Depends(get_db)):
    """ Save cryptocurrency from CoinGecko to the local database. """
    if models.Cryptocurrency.exists(db, crypto_id):
        raise already_exists_exception("Cryptocurrency", crypto_id)
    
    data = await fetch_cryptocurrency_data(crypto_id)
    crypto_data = extract_cryptocurrency_data(data)
    
    return models.Cryptocurrency.create(db, **crypto_data)


@router.put("/cryptocurrency/{crypto_id}", summary="Update cryptocurrency in database")
async def update_cryptocurrency(crypto_id: str, db: Session = Depends(get_db)):
    """ Update existing cryptocurrency with new data from CoinGecko. """
    if not models.Cryptocurrency.exists(db, crypto_id):
        raise not_found_exception("Cryptocurrency", crypto_id)
    
    data = await fetch_cryptocurrency_data(crypto_id)
    crypto_data = extract_cryptocurrency_data(data)
    
    return models.Cryptocurrency.update(db, record_id=crypto_id, **crypto_data)



@router.delete("/cryptocurrency/{crypto_id}", summary="Delete cryptocurrency from database")
def delete_cryptocurrency(crypto_id: str, db: Session = Depends(get_db)):
    """ Delete cryptocurrency from the local database. """
    db_crypto = models.Cryptocurrency.delete(db, crypto_id)
    if not db_crypto:
        raise not_found_exception("Cryptocurrency", crypto_id)

    return {"message": f"Cryptocurrency {crypto_id} successfully deleted"}
