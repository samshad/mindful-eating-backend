import ast
from random import sample

import pandas as pd


def generate_eating_behavior_classify_prompt(csv_file_path="Data/eating_behaviors.csv", input_text=""):
    """
    Generate a prompt for analyzing eating behaviors based on available behavior classes.

    Args:
        csv_file_path (str): Path to the CSV file containing eating behavior classes
        input_text (str): The input text to be analyzed for eating behaviors

    Returns:
        str: Formatted prompt text for analysis
    """
    # Load classes from CSV using pandas
    df = pd.read_csv(csv_file_path, header=None)  # If your CSV has no header, use header=None
    # Assume each row in the CSV has a single eating behavior class in column 0:
    behavior_classes = df[0].tolist()[1:]

    # Build the prompt by listing the classes
    classes_list_str = ""
    for i, cls in enumerate(behavior_classes, start=1):
        classes_list_str += f"{i}. {cls}\n"

    prompt_text = f"""
You are an expert in analyzing eating behaviors. I have {len(behavior_classes)} possible behavior classes:

{classes_list_str}
Task:
Carefully read the text provided after 'Input Text:'.
Identify only the most relevant behavior classes that accurately characterize the text.
Select between one (1) and three (3) behaviors based on clear relevance:
- If only one class clearly matches, select only one.
- If two classes match well, select exactly two.
- Select three classes only if all three are distinctly and equally relevant.
If no behavior clearly matches, return an empty list: [].

Output Format:
- Return your final classification strictly as a JSON-like list 
  (e.g., ["Mindful Eating", "Snacking Habits"]) or [].
- Do not include additional commentary or explanation.

Input Text:
{input_text}
"""

    return prompt_text


def generate_big5_personality_prompt(input_text=""):
    """
    Generate a prompt for Big Five personality analysis from the given input text.

    Args:
        input_text (str): The input text from which to predict Big Five traits.

    Returns:
        str: A formatted prompt text for Big Five personality analysis.
    """

    prompt_text = f"""
You are an expert Personality Psychologist with over 10 years of experience in personality analysis.
You specialize in predicting the Big Five personality traits (Extraversion, Agreeableness, Conscientiousness,
Neuroticism, and Openness).

Task:
1. Read the text provided after 'Input Text:'.
2. Return a JSON object containing the Big Five trait scores.
   Each score should be a floating-point number between 0 and 1, for example:
   {{
     "extraversion": 0.66251994264596,
     "agreeableness": 0.33902498131954684,
     "conscientiousness": 0.33057333844942144,
     "neuroticism": 0.6707797322131793,
     "openness": 0.6744249449683947
   }}
3. Do not provide any explanation or commentary; only return the JSON.

Input Text:
{input_text}
"""

    return prompt_text


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


if __name__ == "__main__":
    # This allows the script to be run directly for testing
    # prompt = generate_eating_behavior_classify_prompt()
    prompt = generate_tips_prompt()
    print(prompt + "Testing text...")