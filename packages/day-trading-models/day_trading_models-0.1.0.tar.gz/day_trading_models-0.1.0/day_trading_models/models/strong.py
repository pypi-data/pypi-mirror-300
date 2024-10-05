from sqlalchemy import Column, Integer, String, Float, Date, Time

from ..database import DB

class Strong(DB.Base):
    __tablename__ = "strong"

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
    # 是否新高
    is_highest = Column(Integer)
    # 量比
    volume_ratio = Column(Float)
    # 涨停统计 n/m 表示m天中n天涨停
    zt_stat = Column(String)
    # 入选理由
    reason = Column(String)
    # 所属行业
    industry = Column(String)
