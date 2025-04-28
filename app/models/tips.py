from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from datetime import datetime
from app.models import Base


class UserTips(Base):
    __tablename__ = "user_tips"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    tips_text = Column(String)
    created_at = Column(DateTime, default=datetime.now())
