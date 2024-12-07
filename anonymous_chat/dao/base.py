from fastapi import Depends
from sqlalchemy import insert, select

from database import get_db
from sqlalchemy.orm import Session


class BaseDAO:
    model = None

    @classmethod
    async def find_by_id(cls, model_id: int, db: Session = Depends(get_db)):
        query = select(cls.model).filter_by(id=model_id)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def find_one_or_none(cls, db: Session = Depends(get_db), **filter_by):
        query = select(cls.model).filter_by(**filter_by)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def add(cls, db: Session = Depends(get_db), **data):
        query = insert(cls.model).values(**data)
        await db.execute(query)
        await db.commit()
