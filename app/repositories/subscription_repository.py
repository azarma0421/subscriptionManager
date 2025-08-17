from typing import List
from sqlalchemy.orm import Session
from app.db.models.subscription import Subscription

class SubscriptionRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, name: str, service: str, user_id: int) -> Subscription:
        sub = Subscription(name=name, service=service, user_id=user_id)
        self.db.add(sub)
        self.db.commit()
        self.db.refresh(sub)
        return sub

    def list_by_user_id(self, user_id: int) -> List[Subscription]:
        return self.db.query(Subscription).filter(Subscription.user_id == user_id).all()