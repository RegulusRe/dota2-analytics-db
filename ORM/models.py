from sqlalchemy import Column, Integer, BigInteger, String, Date, ForeignKey, Boolean, DECIMAL
from sqlalchemy.orm import relationship
from database import Base

class Tournaments(Base):
    __tablename__ = "Tournaments"

    tournament_id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    start_date = Column(Date)
    end_date = Column(Date)
    winner = Column(String(255))

class Teams(Base):
    __tablename__ = "Teams"

    team_id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)

class Players(Base):
    __tablename__ = "Players"

    player_id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    nickname = Column(String(255))
    position = Column(String(100))
    team_id = Column(BigInteger, ForeignKey("Teams.team_id"))
    available = Column(Boolean, default=True)
    team = relationship("Teams")

class Heroes(Base):
    __tablename__ = "Heroes"

    hero_id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)
    role = Column(String(100))
    ultimate = Column(String(255))

class Series(Base):
    __tablename__ = "Series"

    series_id = Column(BigInteger, primary_key=True, index=True)
    tournament_id = Column(BigInteger, ForeignKey("Tournaments.tournament_id"))
    team1_id = Column(BigInteger, ForeignKey("Teams.team_id"))
    team2_id = Column(BigInteger, ForeignKey("Teams.team_id"))
    winner_id = Column(BigInteger, ForeignKey("Teams.team_id"))
    start_date = Column(Date)
    end_date = Column(Date)

class Matches(Base):
    __tablename__ = "Matches"

    match_id = Column(BigInteger, primary_key=True, index=True)
    series_id = Column(BigInteger, ForeignKey("Series.series_id"))
    tournament_id = Column(BigInteger, ForeignKey("Tournaments.tournament_id"))
    team_radiant = Column(BigInteger, ForeignKey("Teams.team_id"))
    team_dire = Column(BigInteger, ForeignKey("Teams.team_id"))
    winner_id = Column(BigInteger, ForeignKey("Teams.team_id"))

class Statistics(Base):
    __tablename__ = "Statistics"

    stat_id = Column(BigInteger, primary_key=True, index=True)
    player_id = Column(BigInteger, ForeignKey("Players.player_id"))
    match_id = Column(BigInteger, ForeignKey("Matches.match_id"))
    hero_id = Column(BigInteger, ForeignKey("Heroes.hero_id"))
    kills = Column(Integer, default=0)
    deaths = Column(Integer, default=0)
    assists = Column(Integer, default=0)
    damage = Column(Integer, default=0)
    roshan_kills = Column(Integer, default=0)
    towers_kills = Column(Integer, default=0)

class Prizes(Base):
    __tablename__ = "Prizes"

    prize_id = Column(BigInteger, primary_key=True, index=True)
    tournament_id = Column(BigInteger, ForeignKey("Tournaments.tournament_id"))
    team_id = Column(BigInteger, ForeignKey("Teams.team_id"))
    place = Column(Integer)
    amount = Column(DECIMAL(15, 2))