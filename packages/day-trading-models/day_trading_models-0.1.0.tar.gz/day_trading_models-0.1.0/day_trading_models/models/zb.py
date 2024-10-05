from sqlalchemy import Column, Integer, String, Float, Date, Time

from ..database import DB

class Zb(DB.Base):
    __tablename__ = "zb"

    date = Column(Date, primary_key=True, index=True)
    # 代码
    symbol = Column(String, primary_key=True, index=True)
    # 名称
    name = Column(String)
    # 涨跌幅
    change = Column(Float)
    # 最新价
    newest_price = Column(Float)
    # 涨停价
    zt_price = Column(Float)
    # 成交额
    volume = Column(Integer)
    # 流通市值
    float_cap = Column(Float)
    # 市值
    market_cap = Column(Float)
    # 换手率
    turnover_rate = Column(Float)
    # 涨速
    speed = Column(Float)
    # 首次封板时间
    first_zt_time = Column(Time)
    # 最后封板时间
    zhaban_times = Column(Integer)
    # 涨停统计 n/m 表示m天中n天涨停
    zt_stat = Column(String)
    # 振幅
    amplitude = Column(Float)
    # 所属行业
    industry = Column(String)
