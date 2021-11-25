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
    def cls_attr(cls, col_name=None):
        return getattr(cls, col_name) if col_name else cls

    @classmethod
    def filter(cls, session: Session = None, **kwargs):
        cond = []
        for key, val in kwargs.items():
            key = key.split("__")
            if len(key) > 2:
                raise Exception("No 2 more dunders")
            col = getattr(cls, key[0])
            if len(key) == 1: cond.append((col == val))
            elif len(key) == 2 and key[1] == 'gt': cond.append((col > val))
            elif len(key) == 2 and key[1] == 'gte': cond.append((col >= val))
            elif len(key) == 2 and key[1] == 'lt': cond.append((col < val))
            elif len(key) == 2 and key[1] == 'lte': cond.append((col <= val))
            elif len(key) == 2 and key[1] == 'in': cond.append((col.in_(val)))
        obj = cls()
        if session:
            obj._session = session
            obj.served = True
        else:
            obj._session = next(db.session())
            obj.served = False
        query = obj._session.query(cls)
        query = query.filter(*cond)
        obj._q = query
        return obj

    @classmethod
    def create(cls, session: Session = None, auto_commit=False, **kwargs):
        obj = cls()
        sess = next(db.session()) if not session else session
        columns = obj.all_columns()
        for col in kwargs:
            if col in columns:
                setattr(obj, col, kwargs.get(col))
        sess.add(obj)
        sess.flush()
        if auto_commit:
            sess.commit()
        if not session:
            sess.close()
        return obj

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
        if not session:
            sess.close()
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
        if not session:
            sess.close()
        return query

    def get_one(self):
        result = self._q.first()
        self.close()
        return result

    def get_all(self):
        result = self._q.all()
        self.close()
        return result

    def close(self):
        if not self.served:
            self._session.close()
        else:
            self._session.flush()

    def order_by(self, *args: str):
        for a in args:
            if a.startswith("-"):
                col_name = a[1:]
                is_asc = False
            else:
                col_name = a
                is_asc = True
            col = self.cls_attr(col_name)
            self._q = self._q.order_by(col.asc() if is_asc else col.desc())
        return self


class Test(Base, BaseMixin):
    __tablename__ = "test"
    value = Column(Integer, nullable=True)
    err_txt = Column(Text, nullable=True)
    