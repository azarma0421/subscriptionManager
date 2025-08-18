from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.db.base import Base


class Subscription(Base):
    __tablename__ = "subscriptions"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    service = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    usage_count = Column(Integer, default=0)
    monthly_cost = Column(Integer, default=0)
    last_used_at = Column(DateTime, nullable=True)
    owner = relationship("User", back_populates="subscriptions")
