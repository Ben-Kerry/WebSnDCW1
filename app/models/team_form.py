from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class TeamForm(Base):
    __tablename__ = "team_form_snapshots"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id", ondelete="CASCADE"), nullable=False)
    as_of_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    last_5_wins: Mapped[int] = mapped_column(Integer, default=0)
    last_5_draws: Mapped[int] = mapped_column(Integer, default=0)
    last_5_losses: Mapped[int] = mapped_column(Integer, default=0)
    last_5_goals_for: Mapped[int] = mapped_column(Integer, default=0)
    last_5_goals_against: Mapped[int] = mapped_column(Integer, default=0)
    home_form_rating: Mapped[float] = mapped_column(Float, default=0.0)
    away_form_rating: Mapped[float] = mapped_column(Float, default=0.0)

    team = relationship("Team")