# -----------------------------------------------------------------------------
# Project: Mindful Eating
# Author: Md Samshad Rahman
# Year: 2025
# License: GNU Affero General Public License v3.0 (See LICENSE file for details)
# Description: This file is part of the Mindful Eating project.
# -----------------------------------------------------------------------------
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from app.models import Base


class UserBehavior(Base):
    __tablename__ = "user_behaviors"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    behavior_id = Column(String)
    behavior_title = Column(String)
    first_priority = Column(Boolean, default=False)
    high_priority = Column(Boolean, default=False)
