from sqlalchemy import Column, Integer, String, Float, Date, Time

from ..database import DB

class Dt(DB.Base):
    __tablename__ = "dt"

    date = Column(Date, primary_key=True, index=True)
    # 代码
    symbol = Column(String, primary_key=True, index=True)
    # 名称
    name = Column(String)
    # 涨跌幅
    change = Column(Float)
    # 最新价
    newest_price = Column(Float)
    # 成交额
    volume = Column(Integer)
    # 流通市值
    float_cap = Column(Float)
    # 市值
    market_cap = Column(Float)
    # 换手率
    turnover_rate = Column(Float)
    # 动态市盈率
    pe_dynamic = Column(Float)
    # 换手率
    turnover_rate = Column(Float)
    # 封单资金
    fengdan_zijin = Column(Integer)
    # 最后封板时间
    final_dt_time = Column(Time)
    # 板上成交额
    banshang_chengjiaoe = Column(Integer)
    # 连续跌停
    lianxu_dt = Column(Integer)
    # 开板次数
    kaiban_times = Column(Integer)
    # 所属行业
    industry = Column(String)
