from sqlalchemy import Column, Integer, String, Float, Date

from ..database import DB

class Quotation(DB.Base):
    __tablename__ = "quotation"

    date = Column(Date, primary_key=True, index=True)
    # 代码
    symbol = Column(String, primary_key=True, index=True)
    # 名称
    name = Column(String)
    # 收盘价
    close_price = Column(Float)
    # 涨跌幅
    change = Column(Float)
    # 涨跌额
    change_volume = Column(Float)
    # 成交量
    volume = Column(Float)
    # 成交额
    deal = Column(Float)
    # 振幅
    amplitude = Column(Float)
    # 最高
    high_price = Column(Float)
    # 最低
    low_price = Column(Float)
    # 今开
    open_price = Column(Float)
    # 昨收
    pre_close_price = Column(Float)
    # 量比
    volume_ratio = Column(Float)
    # 换手率
    turnover_rate = Column(Float)
    # 市盈率-动态
    pe_dynamic = Column(Float)
    # 市净率
    pb = Column(Float)
    # 总市值
    market_cap = Column(Float)
    # 流通市值
    float_cap = Column(Float)
