from sqlalchemy import Column, Integer, String, Float, Date

from ..database import DB

class LhbPlayer(DB.Base):
    __tablename__ = "lhb_player"

    # 机构名称可能有重复，比如 机构专用，所以添加自增ID
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, index=True)
    # 买入 或 卖出
    type = Column(String, index=True)
    # 代码
    symbol = Column(String, index=True)
    # 交易营业部名称
    player = Column(String, index=True)
    # 买入金额
    buy_volume = Column(Integer)
    # 买入金额-占总成交比例
    buy_ratio = Column(Float)
    # 卖出金额
    sell_volume = Column(Integer)
    # 卖出金额-占总成交比例
    sell_ratio = Column(Float)
    # 净额
    net_volume = Column(Integer)
    # 类型
    reason = Column(String)
