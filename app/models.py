from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Float, DateTime


Base = declarative_base()

class FetchMixin:
    @classmethod
    def filter(cls, db, **kwargs):
        return db.query(cls).filter_by(**kwargs)
    
    @classmethod
    def get(cls, db, id):
        return db.query(cls).filter(cls.id == id).first()
    
    @classmethod
    def all(cls, db, order_by=None):
        query = db.query(cls)
        if order_by:
            query = query.order_by(order_by)
        return query.all()

    @classmethod
    def exists(cls, db, id):
        from sqlalchemy.sql import exists
        return db.query(exists().where(cls.id == id)).scalar()


class ModifyMixin(FetchMixin):
    @classmethod
    def create(cls, db, **kwargs):
        obj = cls(**kwargs)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj
    
    @classmethod
    def update(cls, db, record_id, **kwargs):
        obj = cls.get(db, record_id)
        if obj:
            for key, value in kwargs.items():
                setattr(obj, key, value)
            db.commit()
            db.refresh(obj)
        return obj
    
    @classmethod
    def delete(cls, db, id):
        obj = cls.get(db, id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj

class Cryptocurrency(ModifyMixin, Base):
    """Model representing cryptocurrency and its current market information."""
    __tablename__ = "cryptocurrencies"
    
    id = Column(String, primary_key=True)
    symbol = Column(String, nullable=False)
    name = Column(String, nullable=False)
    price_usd = Column(Float, nullable=False)
    market_cap = Column(Float)
    volume_24h = Column(Float)
    price_change_24h = Column(Float)
    last_updated = Column(DateTime(timezone=True), nullable=False)


