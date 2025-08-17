from typing import List
from fastapi import APIRouter, Depends
from app.schemas.subscription import SubscriptionCreate, SubscriptionOut
from app.services.subscription_service import SubscriptionService
from app.api.deps import get_subscription_service, get_current_user
from app.db.models.user import User

subRouter = APIRouter()


@subRouter.post("", response_model=SubscriptionOut)
def create_subscription(
    data: SubscriptionCreate,
    current_user: User = Depends(get_current_user),
    svc: SubscriptionService = Depends(get_subscription_service),
):
    return svc.create_for_user(current_user, data)


@subRouter.get("", response_model=List[SubscriptionOut])
def list_subscriptions(
    current_user: User = Depends(get_current_user),
    svc: SubscriptionService = Depends(get_subscription_service),
):
    return svc.list_for_user(current_user)
