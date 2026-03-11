from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Team(Base):
    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    country: Mapped[str] = mapped_column(String(100), nullable=False)
    coach: Mapped[str | None] = mapped_column(String(100), nullable=True)
    founded_year: Mapped[int | None] = mapped_column(Integer, nullable=True)
    uefa_coefficient: Mapped[float] = mapped_column(Float, default=0.0)

    players = relationship("Player", back_populates="team", cascade="all, delete-orphan")
    home_matches = relationship("Match", foreign_keys="Match.home_team_id", back_populates="home_team")
    away_matches = relationship("Match", foreign_keys="Match.away_team_id", back_populates="away_team")
    probabilities = relationship("Probability", back_populates="team", cascade="all, delete-orphan")