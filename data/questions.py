import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Questions(SqlAlchemyBase):
    __tablename__ = 'questions'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    que1 = sqlalchemy.Column(sqlalchemy.String, default=True)
    que2 = sqlalchemy.Column(sqlalchemy.String, default=True)
    que3 = sqlalchemy.Column(sqlalchemy.String, default=True)

    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    user = orm.relationship('User')

