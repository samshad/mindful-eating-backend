# -----------------------------------------------------------------------------
# Project: Mindful Eating
# Author: Md Samshad Rahman
# Year: 2025
# License: GNU Affero General Public License v3.0 (See LICENSE file for details)
# Description: This file is part of the Mindful Eating project.
# -----------------------------------------------------------------------------
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from datetime import datetime
from app.models import Base
from app.utils.get_current_time import get_current_time


class UserGoal(Base):
    __tablename__ = "user_goals"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    goal_text = Column(String)
    created_at = Column(DateTime, default=get_current_time())
