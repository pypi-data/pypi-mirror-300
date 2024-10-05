from sqlalchemy import Column, Integer, String, Float, Date, Time

from ..database import DB

class Subnew(DB.Base):
    __tablename__ = "subnew"

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
    # 开板几日：次新股当前交易日距离个股第一次中断连续一字涨停板的那个交易日，所经历的交易日的天数
    days_kaiban = Column(Integer)
    # 开板日期: 新股第一次中断连续一字涨停板的那个交易日的日期
    date_kaiban = Column(Date)
    # 上市日期
    date_listed = Column(Date)
    # 涨停统计 n/m 表示m天中n天涨停
    zt_stat = Column(String)
    # 是否新高
    is_highest = Column(Integer)
    # 所属行业
    industry = Column(String)
