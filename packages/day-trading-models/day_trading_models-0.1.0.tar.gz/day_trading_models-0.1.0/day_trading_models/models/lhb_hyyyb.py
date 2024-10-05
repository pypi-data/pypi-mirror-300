from sqlalchemy import Column, Integer, String, Float, Date

from ..database import DB

# 活跃营业部
class LhbHyyyb(DB.Base):
    __tablename__ = "lhb_hyyyb"

    # 机构名称可能有重复，比如 机构专用，所以添加自增ID
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, index=True)
    # 营业部名称
    player = Column(String, index=True)
    # 买入个股数
    buy_num = Column(Integer)
    # 卖出个股数
    sell_num = Column(Integer)
    # 买入总金额
    buy_volume = Column(Float)
    # 卖出总金额
    sell_volume = Column(Integer)
    # 总买卖净额
    net_volume = Column(Float)
    # 买入股票
    bought_stocks = Column(String)
