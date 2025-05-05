# -----------------------------------------------------------------------------
# Project: Mindful Eating
# Author: Md Samshad Rahman
# Year: 2025
# License: GNU Affero General Public License v3.0 (See LICENSE file for details)
# Description: This file is part of the Mindful Eating project.
# -----------------------------------------------------------------------------
from pydantic import BaseModel
from typing import List, Optional


class FoodImageUpload(BaseModel):
    base64_file: str  # base64 encoded image string


class FoodUpdatePayload(BaseModel):
    description: Optional[str] = None
    images: Optional[List[FoodImageUpload]] = None
