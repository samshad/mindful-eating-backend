# -----------------------------------------------------------------------------
# Project: Mindful Eating
# Author: Md Samshad Rahman
# Year: 2025
# License: GNU Affero General Public License v3.0 (See LICENSE file for details)
# Description: This file is part of the Mindful Eating project.
# -----------------------------------------------------------------------------
from pydantic import BaseModel
from typing import List, Union, Dict


class AnswerItem(BaseModel):
    question_id: int
    answer: Union[str, int, List[str], Dict[str, Union[str, List[str]]]]


class SubmitAnswersRequest(BaseModel):
    answer_list: List[AnswerItem]
