from sqlalchemy import Column, Integer, String, Float, Date

from ..database import DB

class Lhb(DB.Base):
    __tablename__ = "lhb"

    date = Column(Date, primary_key=True, index=True)
    # 代码
    symbol = Column(String, primary_key=True, index=True)
    # 上榜原因
    reason = Column(String, primary_key=True, index=True)
    # 名称
    name = Column(String)
    # 解读
    comment = Column(String)
    # 收盘价
    close_price = Column(Float)
    # 涨跌幅
    change = Column(Float)
    # 龙虎榜净买额
    lhb_net_buy = Column(Float)
    # 龙虎榜买入额
    lhb_buy = Column(Float)
    # 龙虎榜卖出额
    lhb_sell = Column(Float)
    # 龙虎榜成交额
    lhb_deal = Column(Float)
    # 市场总成交额
    market_deal = Column(Float)
    # 净买额占总成交比
    lhb_buy_over_market_deal = Column(Float)
    # 成交额占总成交比
    lhb_deal_over_market_deal = Column(Float)
    # 换手率
    turnover_rate = Column(Float)
    # 流通市值
    float_cap = Column(Float)
