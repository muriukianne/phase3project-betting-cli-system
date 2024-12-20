from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table
from sqlalchemy.orm import relationship, declarative_base


Base = declarative_base()

bets = Table(
    "bets",
    Base.metadata,
    Column("id",Integer,primary_key=True),
    Column("match_id",Integer,ForeignKey("matches.id")),
    Column("bettor_id",Integer,ForeignKey("bettors.id"))
)

class Bettor(Base):
    __tablename__ = "bettors"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    wallet = Column(Float, default=100.0) 

    matches = relationship("Match", secondary=bets, back_populates="bettors")
    transactions = relationship("Transaction", back_populates="bettor")

class Match(Base):
    __tablename__="matches"

    id = Column(Integer, primary_key=True)    
    name = Column(String, nullable=False)
    odds_team_a = Column(Float, nullable=False)
    odds_team_b = Column(Float, nullable=False)

    bettors = relationship("Bettor", secondary=bets,  back_populates="matches")
    transactions = relationship("Transaction", back_populates="match")

class Transaction(Base):
    __tablename__="transactions"

    id = Column(Integer, primary_key=True)
    bettor_id = Column(Integer, ForeignKey("bettors.id"))
    match_id = Column(Integer, ForeignKey("matches.id"))
    amount = Column(Float, nullable=False)
    team_bet_on = Column(String, nullable=False)
    status = Column(String, default="pending")

    bettor = relationship("Bettor", back_populates="transactions")
    match = relationship("Match", back_populates="transactions")

