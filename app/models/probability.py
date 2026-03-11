from sqlalchemy import Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Probability(Base):
    __tablename__ = "probabilities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id", ondelete="CASCADE"), nullable=False)
    win_probability: Mapped[float] = mapped_column(Float, nullable=False)
    source_confidence: Mapped[float] = mapped_column(Float, default=0.5)

    team = relationship("Team", back_populates="probabilities")