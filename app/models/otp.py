# -----------------------------------------------------------------------------
# Project: Mindful Eating
# Author: Md Samshad Rahman
# Year: 2025
# License: GNU Affero General Public License v3.0 (See LICENSE file for details)
# Description: This file is part of the Mindful Eating project.
# -----------------------------------------------------------------------------
from sqlalchemy import Column, String, DateTime, Integer
from app.models import Base


class OTP(Base):
    __tablename__ = "otp"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False)
    otp_code = Column(String, nullable=False)
    expires_at = Column(DateTime, nullable=False)
