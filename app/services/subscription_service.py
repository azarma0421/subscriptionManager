from typing import List
from app.repositories.subscription_repository import SubscriptionRepository
from app.schemas.subscription import SubscriptionCreate
from app.db.models.subscription import Subscription
from app.db.models.user import User

class SubscriptionService:
    def __init__(self, subs: SubscriptionRepository) -> None:
        self.subs = subs

    def create_for_user(self, current_user: User, data: SubscriptionCreate) -> Subscription:
        return self.subs.create(name=data.name, service=data.service, user_id=current_user.id)

    def list_for_user(self, current_user: User) -> List[Subscription]:
        return self.subs.list_by_user_id(user_id=current_user.id)

    def list_by_user_id(self, user_id: int) -> List[Subscription]:
        return self.subs.list_by_user_id(user_id=user_id)