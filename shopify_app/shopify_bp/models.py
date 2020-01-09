from sqlalchemy import Column

from ..extensions import db


class Shop(db.Model):
    __tablename__ = 'shop'

    id = Column(db.Integer, primary_key=True)
    # <shopname>.myshopify.com
    shop = Column(db.String())

    # token is used to issue commands on behalf of a shop
    token = Column(db.String())

    # status of user, currently not used anywhere but maybe one day? ;)
    status = Column(db.SmallInteger, default=1)
