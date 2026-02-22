import json
from pathlib import Path
from typing import List, Dict, Any
from models import Feedback


class FeedbackManager:
    def __init__(self, data_dir: str = ".early-reach"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.feedback_file = self.data_dir / "feedback.json"
    
    def add_feedback(self, feedback: Feedback):
        all_feedback = self.get_all_feedback()
        all_feedback.append(feedback)
        with open(self.feedback_file, "w") as f:
            json.dump([fb.model_dump(mode="json") for fb in all_feedback], f, indent=2, default=str)
    
    def get_all_feedback(self) -> List[Feedback]:
        if not self.feedback_file.exists():
            return []
        with open(self.feedback_file, "r") as f:
            data = json.load(f)
            return [Feedback(**item) for item in data]
    
    def generate_report(self) -> Dict[str, Any]:
        all_feedback = self.get_all_feedback()
        
        if not all_feedback:
            return {
                "total": 0,
                "avg_rating": 0,
                "by_platform": {},
                "recent": []
            }
        
        ratings = [fb.rating for fb in all_feedback if fb.rating]
        avg_rating = sum(ratings) / len(ratings) if ratings else 0
        
        by_platform = {}
        for fb in all_feedback:
            if fb.platform:
                platform_name = fb.platform.value
                by_platform[platform_name] = by_platform.get(platform_name, 0) + 1
        
        recent = sorted(all_feedback, key=lambda x: x.created_at, reverse=True)
        
        return {
            "total": len(all_feedback),
            "avg_rating": avg_rating,
            "by_platform": by_platform,
            "recent": recent
        }
