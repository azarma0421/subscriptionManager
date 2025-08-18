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

    def delete_by_user_id_and_subscription_id(
        self, user_id: int, subscription_id: int
    ) -> dict | None:
        sub = (
            self.db.query(Subscription)
            .filter(Subscription.user_id == user_id, Subscription.id == subscription_id)
            .first()
        )
        if not sub:
            return {"result": "Subscription not found or does not belong to user"}

        self.db.delete(sub)
        self.db.commit()
        return {"result": f"Subscription id:{subscription_id}, deleted "}
