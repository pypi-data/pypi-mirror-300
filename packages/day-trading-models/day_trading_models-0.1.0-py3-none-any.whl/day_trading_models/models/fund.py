from sqlalchemy import Column, Integer, String, Float, Date

from ..database import DB

class Fund(DB.Base):
    __tablename__ = "fund"

    date = Column(Date, primary_key=True, index=True)
    # 上证-收盘价
    sse_close_price = Column(Float)
    # 上证-涨跌幅
    sse_change = Column(Float)
    # 深证-收盘价
    szse_close_price = Column(Float)
    # 深证-涨跌幅
    szse_change = Column(Float)
    # 主力净流入-净额
    main_in_capital = Column(Float)
    # 主力净流入-净占比
    main_in_capital_ratio = Column(Float)
    # 超大单净流入-净额
    super_big_in_capital = Column(Float)
    # 超大单净流入-净占比
    super_big_in_capital_ratio = Column(Float)
    # 大单净流入-净额
    big_in_capital = Column(Float)
    # 大单净流入-净占比
    big_in_capital_ratio = Column(Float)
    # 中单净流入-净额
    medium_in_capital = Column(Float)
    # 中单净流入-净占比
    medium_in_capital_ratio = Column(Float)
    # 小单净流入-净额
    small_in_capital = Column(Float)
    # 小单净流入-净占比
    small_in_capital_ratio = Column(Float)
    # 两市成交额
    sum_deal = Column(Float)
