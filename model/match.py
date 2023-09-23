from model.base import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func


class Match(Base):
    __tablename__ = 'match'
    id = Column("pk_match", Integer, primary_key=True, autoincrement=True)
    deck_id = Column(String, nullable=False)
    player_id = Column(Integer,  ForeignKey("player.pk_player"),
                       nullable=False)
    date = Column(DateTime(timezone=True), server_default=func.now())
    game_over = Column(Boolean, default=False)
    bet_1 = Column(Integer, default=0)
    bet_5 = Column(Integer, default=0)
    bet_25 = Column(Integer, default=0)
    bet_50 = Column(Integer, default=0)
    bet_100 = Column(Integer, default=0)
    pay_1 = Column(Integer, default=0)
    pay_5 = Column(Integer, default=0)
    pay_25 = Column(Integer, default=0)
    pay_50 = Column(Integer, default=0)
    pay_100 = Column(Integer, default=0)
