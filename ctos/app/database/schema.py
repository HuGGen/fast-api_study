from sqlalchemy import(
    Column
  , Integer
  , String
  , Text
  , DateTime
  , func
  , Enum
  , Boolean
)

from sqlalchemy.orm import Session
from app.database.conn import Base, db
import json
from fastapi.encoders import jsonable_encoder

class BaseMixin:
    id = Column(Text, primary_key=True)
    get_dt = Column(DateTime, default=func.now(), onupdate=func.now())

    def __init__(self):
        self._q =None
        self._session = None
        self.served = None

    def all_columns(self):
        return [c.name for c in self.__table__.columns]

    def __hash__(self):
        return hash(self.id)

    @classmethod
    def create(cls, session: Session = None, auto_commit=False, **kwargs):
        obj = cls()
        sess = next(db.session()) if not session else session
        columns =  obj.all_columns()
        for col in kwargs:
            if col in columns:
                setattr(obj, col, kwargs.get(col))
        sess.add(obj)
        sess.flush()
        if auto_commit:
            sess.commit()
        return obj

    @classmethod
    def read(cls, session: Session = None, **kwargs):
        obj = cls()
        columns = obj.all_columns()
        sess = next(db.session()) if not session else session
        query = sess.query(cls)
        for key, val in kwargs.items():
            if key in columns:
                col = getattr(cls, key)
                query = query.filter(col == val)
        result = query.all()
        if not session:
            sess.close()
        return jsonable_encoder(result)

    @classmethod
    def update(cls, session: Session = None, auto_commit=False, **kwargs):
        obj = cls()
        columns = obj.all_columns()
        sess = next(db.session()) if not session else session
        query = sess.query(cls)
        for key, val in kwargs.get("filter").items():
            if key in columns:
                col = getattr(cls, key)
                query = query.filter(col == val)
        for key, val in kwargs.get("update").items():
            if key in columns:
                col = getattr(cls, key)
                query = query.update({key : val})
        sess.flush()
        if auto_commit:
            sess.commit()
        return query

    @classmethod
    def delete(cls, session: Session = None, auto_commit= False, **kwargs):
        obj = cls()
        columns = obj.all_columns()
        sess = next(db.session()) if not session else session
        query = sess.query(cls)
        for key, val in kwargs.items():
            if key in columns:
                col = getattr(cls, key)
                query = query.filter(col == val)
        query = query.delete()

        sess.flush()
        if auto_commit:
            sess.commit()
        return query

class Test(Base, BaseMixin):
    __tablename__ = "test"
    value = Column(Integer, nullable=True)
    err_txt = Column(Text, nullable=True)
    