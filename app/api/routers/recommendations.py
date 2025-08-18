from fastapi import APIRouter, Depends
from app.api.deps import get_recommendation_service, get_current_user
from app.services.recommendation_service import RecommendationService
from app.db.models.user import User

recommendationsRouter = APIRouter()


@recommendationsRouter.get("/subscriptions/recommendations")
def get_recommendations(
    user_id: User = Depends(get_current_user),
    svc: RecommendationService = Depends(get_recommendation_service),
):
    results = svc.generate_suggestion(User.id)
    return {"recommendations": results}
