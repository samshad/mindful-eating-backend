# -----------------------------------------------------------------------------
# Project: Mindful Eating
# Author: Md Samshad Rahman
# Year: 2025
# License: GNU Affero General Public License v3.0 (See LICENSE file for details)
# Description: This file is part of the Mindful Eating project.
# -----------------------------------------------------------------------------
from pydantic import BaseModel
from typing import List


class BehaviorItem(BaseModel):
    behavior_id: int
    first_priority: bool
    high_priority: bool


class SubmitBehaviorsRequest(BaseModel):
    behavior_list: List[BehaviorItem]
