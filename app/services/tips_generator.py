import re
import os
import logging
from datetime import datetime, date
from sqlalchemy.exc import SQLAlchemyError
from app.models import UserBehavior, BigFiveTraits, FoodUpdate, UserGoal, UserTips
from app.services.ollama_service import generate_result

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

MOCK = os.getenv("MOCK", "false").lower() in ("true", "True")


def generate_tips_prompt(input_text=""):
    """
    Generate a prompt for providing tips based on the given input text.

    Args:
        input_text (str): The input text for which to generate tips.

    Returns:
        str: A formatted prompt text for generating tips based on the input.
    """

    prompt_text = f"""
Role:
You are an AI assistant designed to provide personalized tips and messages related to eating behavior, taking into account the individual's dominant Big Five personality trait.
Think about you have expertise in Personality Psychologist and Dietitian with 10+ years of experience in personality analysis and eating behavior.
The input will be provided as a dictionary with two keys: "Eating Behavior" and "Dominant Big5".
The output should be a single sentence or a short paragraph upto 5 sentences, encouraging message tailored to both the eating behavior and the personality trait.

Here are some examples of how to connect eating behavior and personality traits in a message:

For example:
Input will be like: A dictionary with two keys: "Eating Behavior" and "Dominant Big5"
Output should be: "some tips according to the eating behavior and personality trait"

Task: Generate concise, actionable tips related to the user's eating behavior goals, tailored to their provided personality trait and eating behaviors.

Constraints:
    - Respond only with the tips.
    - Do not include any explanations, commentary, or introductions.
    - Ensure the tips are relevant to the user's specific eating behaviors and the provided Big Five trait.
    - Maintain a professional and helpful tone.
    - Use clear and simple language.
    - Limit the response to a maximum of 5 sentences and it should be a single paragraph.
    - Avoid jargon or overly technical terms.
    - Ensure the tips are practical and easy to implement.
    - Focus on positive reinforcement and encouragement.

Input Text:
{input_text}
"""

    return prompt_text


def format_user_data_text(big_five_dominated_trait, user_goal):
    """
    Format user data into a prompt-friendly text.

    Args:
        user_goal (list): user today's goal.
        big_five_dominated_trait (str): Dominated Big Five trait.

    Returns:
        str: Concatenated formatted string.
    """
    input_text = {
        "eating behaviors": user_goal,
        "Dominated big5": big_five_dominated_trait
        if big_five_dominated_trait
        else "N/A",
    }
    str_input_text = str(input_text)
    return str_input_text


def store_tips(user_id, tips_text, db):
    """
    Store or update the user's daily tip in the database.

    This function checks if a tip for the given user already exists for the current day.
    If a tip exists, it updates the existing tip with the new tips_text. If no tip exists for
    the current day, it creates a new tip entry for the user.

    Args:
        user_id (User): The user id for whom the tip is to be stored or updated.
        tips_text (str): The tip text to be stored in the database.
        db (Session): The SQLAlchemy database session used for querying and committing changes.

    Returns:
        None
    """
    today = date.today()
    existing_tip = (
        db.query(UserTips)
        .filter(
            UserTips.user_id == user_id,
            UserTips.created_at >= datetime.combine(today, datetime.min.time()),
            UserTips.created_at <= datetime.combine(today, datetime.max.time()),
        )
        .first()
    )

    if existing_tip:
        existing_tip.tips_text = tips_text
        db.commit()
        logger.info(f"Tip updated for user {user_id} on {today}.")
    else:
        # new_tip = UserTips(user_id=user_id, tips_text=tips_text)
        new_tip = UserTips(
            user_id=user_id,
            tips_text=tips_text,
            created_at=datetime.now()
        )
        db.add(new_tip)
        db.commit()
        logger.info(f"New tip stored for user {user_id} on {today}.")


def clean_text(text, preserve_paragraphs=False):
    """
    Clean text by removing unnecessary characters and normalizing whitespace.

    Args:
        text (str): Input text to be cleaned
        preserve_paragraphs (bool): If True, preserves paragraph breaks (double newlines)
                                   If False, converts all whitespace to single spaces

    Returns:
        str: Cleaned text
    """
    if not text:
        return text

    # Replace common Unicode whitespace characters with standard spaces
    text = re.sub(
        r"[\u200b\u200c\u200d\u202a-\u202e]", "", text
    )  # Remove zero-width and directional chars
    text = re.sub(
        r"[\xa0\u1680\u180e\u2000-\u200f\u2028-\u202f\u205f\u3000\ufeff]", " ", text
    )

    # Standardize line endings
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    if preserve_paragraphs:
        # Preserve paragraph breaks (double newlines) while cleaning other whitespace
        text = re.sub(
            r"[^\S\n]+", " ", text
        )  # Replace non-newline whitespace with single space
        text = re.sub(r"\n{3,}", "\n\n", text)  # Limit consecutive newlines to 2
    else:
        # Replace all whitespace (including newlines) with single spaces
        text = re.sub(r"\s+", " ", text)

    # Remove any remaining special characters (keeping alphanumeric, basic punctuation and spaces)
    text = re.sub(r"[^a-zA-Z0-9,.!?;:\"'\-–—\s]", "", text)

    # Strip leading/trailing whitespace
    text = text.strip()

    return text


def generate_user_tips(user_id, db):
    """
    Generate personalized tips for a user and store them in the database.
    Handles all exceptions gracefully and ensures the app does not crash.

    Args:
        user_id (User): SQLAlchemy user model instance id.
        db (Session): SQLAlchemy database session.
    """
    try:
        # Get Big Five trait
        try:
            big_five = (
                db.query(BigFiveTraits).filter(BigFiveTraits.user_id == user_id).first()
            )
            big_five_dominated_trait = big_five.max_value if big_five else None
        except Exception as e:
            big_five_dominated_trait = None
            logger.warning(f"Failed to fetch Big Five traits for user {user_id}: {e}")

        # Collect user goals
        try:
            today = date.today()
            goal = (
                db.query(UserGoal)
                .filter(
                    UserGoal.user_id == user_id,
                    UserGoal.created_at >= datetime.combine(today, datetime.min.time()),
                    UserGoal.created_at <= datetime.combine(today, datetime.max.time()),
                )
                .first()
            )
            user_goals = goal.goal_text if goal else ""
        except Exception as e:
            user_goals = ""
            logger.warning(f"Failed to fetch user goals for user {user_id}: {e}")

        # Format and generate prompt
        formatted_text = format_user_data_text(big_five_dominated_trait, user_goals)
        tips_generator_prompt = generate_tips_prompt(formatted_text)

        ollama_result = None
        # Generate tips from model
        try:
            if MOCK:
                ollama_result = (
                    "Eat more whole foods and drink plenty of water today! Dummy"
                )
            else:
                tips_generator_model = os.getenv("TIPS_GENERATOR_MODEL")
                ollama_result = generate_result(
                    tips_generator_prompt, tips_generator_model
                )
        except Exception as e:
            logger.error(f"Failed to generate tips from Ollama model: {e}")

        # Save tips to database
        if ollama_result:
            try:
                ollama_result = clean_text(ollama_result)
                store_tips(user_id, ollama_result, db)
                logger.info(
                    f"User tips generated and saved successfully for user {user_id}."
                )
            except SQLAlchemyError as db_err:
                db.rollback()
                logger.error(f"Failed to save user tips for user {user_id}: {db_err}")

    except Exception as e:
        logger.error(f"Unexpected error in generate_user_tips for user {user_id}: {e}")
