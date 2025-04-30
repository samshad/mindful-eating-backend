import os
import logging
from datetime import datetime, date
from fastapi import HTTPException, BackgroundTasks
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from app.models.tips import UserTips
from app.schemas.tips import CreateUserTipsRequest
from app.services.tips_generator import generate_user_tips

load_dotenv()

# Logger setup
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def create_or_update_user_tips(payload: CreateUserTipsRequest, db: Session, user):
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        today = date.today()
        existing_tip = (
            db.query(UserTips)
            .filter(
                UserTips.user_id == user.id,
                UserTips.created_at >= datetime.combine(today, datetime.min.time()),
                UserTips.created_at <= datetime.combine(today, datetime.max.time()),
            )
            .first()
        )

        if existing_tip:
            existing_tip.tips_text = payload.tips_text
            db.commit()
            message = "User tips updated successfully"
        else:
            # new_tip = UserTips(user_id=user.id, tips_text=payload.tips_text)
            new_tip = UserTips(
                user_id=user.id,
                tips_text=payload.tips_text,
                created_at=datetime.now()
            )
            db.add(new_tip)
            db.commit()
            message = "User tips created successfully"

        return {"message": message}

    except Exception as e:
        logger.error(f"User tips submission failed: {e}")
        raise HTTPException(status_code=500, detail="Technical issue")


def get_user_tips_today(background_tasks: BackgroundTasks, db: Session, user):
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        today = date.today()
        user_tip = (
            db.query(UserTips)
            .filter(
                UserTips.user_id == user.id,
                UserTips.created_at >= datetime.combine(today, datetime.min.time()),
                UserTips.created_at <= datetime.combine(today, datetime.max.time()),
            )
            .first()
        )

        if user_tip:
            return {
                "message": "User tips retrieved successfully",
                "data": {"tips_text": user_tip.tips_text},
            }
        else:
            background_tasks.add_task(generate_user_tips, user.id, db)

            generic_tip = os.getenv("GENERIC_TIPS_TEXT")
            return {
                "message": "No tips submitted today. Showing generic tip.",
                "data": {"tips_text": generic_tip},
            }

    except Exception as e:
        logger.error(f"User tips retrieval failed: {e}")
        raise HTTPException(status_code=500, detail="Technical issue")
