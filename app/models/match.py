from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Match(Base):
    __tablename__ = "matches"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    home_team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"), nullable=False)
    away_team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"), nullable=False)
    round_name: Mapped[str] = mapped_column(String(50), nullable=False)
    leg_number: Mapped[int | None] = mapped_column(Integer, nullable=True)
    bracket_slot: Mapped[str | None] = mapped_column(String(50), nullable=True)
    match_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    venue: Mapped[str] = mapped_column(String(120), nullable=False)
    is_neutral_venue: Mapped[bool] = mapped_column(Boolean, default=False)
    home_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    away_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    status: Mapped[str] = mapped_column(String(30), default="scheduled")
    winner_team_id: Mapped[int | None] = mapped_column(ForeignKey("teams.id"), nullable=True)

    home_team = relationship("Team", foreign_keys=[home_team_id], back_populates="home_matches")
    away_team = relationship("Team", foreign_keys=[away_team_id], back_populates="away_matches")
    winner_team = relationship("Team", foreign_keys=[winner_team_id])
    predictions = relationship("MatchPrediction", back_populates="match", cascade="all, delete-orphan")