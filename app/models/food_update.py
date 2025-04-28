from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models import Base


class FoodUpdate(Base):
    __tablename__ = "food_updates"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.now())

    user = relationship("User", back_populates="food_updates")
    images = relationship(
        "FoodImage", back_populates="food_update", cascade="all, delete-orphan"
    )


class FoodImage(Base):
    __tablename__ = "food_images"

    id = Column(Integer, primary_key=True, index=True)
    food_update_id = Column(Integer, ForeignKey("food_updates.id"), nullable=False)
    image_path = Column(String, nullable=False)  # Store the image file path

    food_update = relationship("FoodUpdate", back_populates="images")
