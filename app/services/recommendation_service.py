from app.repositories.subscription_repository import SubscriptionRepository
from app.db.models.subscription import Subscription
from datetime import datetime


class RecommendationService:
    def __init__(self, subs: SubscriptionRepository) -> None:
        self.subs = subs

    def calculate_efficiency(self, sub: Subscription) -> int:

        cost_per_use = sub.monthly_cost / max(sub.usage_count, 1)
        if sub.last_used_at:
            days_since_last_use = (datetime.now() - sub.last_used_at).days
        else:
            days_since_last_use = 0

        score = 0

        # 成本效率（越低越好）
        if cost_per_use <= 5:
            score += 2
        elif cost_per_use <= 10:
            score += 1

        # 使用頻率
        if sub.usage_count >= 8:
            score += 2
        elif sub.usage_count >= 4:
            score += 1

        # 最近使用時間
        if days_since_last_use <= 7:
            score += 2
        elif days_since_last_use <= 14:
            score += 1

        return self.score_to_suggestion(score)

    def generate_suggestion(self, current_id: str):
        subs = self.subs.list_by_user_id(current_id)
        results = []

        for sub in subs:
            suggestion = self.calculate_efficiency(sub)

            results.append(
                {
                    "name": sub.name,
                    "cost": sub.monthly_cost,
                    "usage_count": sub.usage_count,
                    "suggestion": suggestion,
                }
            )
        return results

    def score_to_suggestion(self, score: int) -> str:
        if score <= 2:
            return "考慮取消"
        elif score <= 4:
            return "使用頻率偏低，可再觀察"
        else:
            return "繼續保留"
