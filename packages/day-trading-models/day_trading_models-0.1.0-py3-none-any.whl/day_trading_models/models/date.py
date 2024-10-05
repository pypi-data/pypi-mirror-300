from sqlalchemy import Column, Date
from ..database import DB

class OpeningDate(DB.Base):
    __tablename__ = "opening_date"

    date = Column(Date, primary_key=True, index=True)
