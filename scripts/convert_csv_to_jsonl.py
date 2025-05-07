import ast
import csv
import json
import pandas as pd
from prompt_eating_behavior import (generate_big5_personality_prompt,
                                    generate_eating_behavior_classify_prompt,
                                    generate_tips_prompt)


def tips_csv_to_jsonl(csv_file, jsonl_file):
    """
    Read a CSV with columns:
      - Behavior_Big5
      - Message
    Write a JSONL, where each line is:
    {
      "messages": [
        {"from": "system", "value": "..."},
        {"from": "human", "value": "..."},
        {"from": "gpt",   "value": {...}}
      ]
    }
    """

    system_message = generate_tips_prompt()

    with open(csv_file, "r", encoding="utf-8-sig") as fin, open(jsonl_file, "w", encoding="utf-8-sig") as fout:
        reader = csv.DictReader(fin)

        for row in reader:
            # Build the conversations array
            #behaviors = row["Behavior_Big5"][0]
            #big5 = row["Behavior_Big5"][1]
            #tips = row["Message"]

            #print(behaviors, big5, tips)

            text = row['Behavior_Big5']

            conversations = [
                {
                    "from": "system",
                    "value": system_message
                },
                {
                    "from": "human",
                    "value": text
                },
                {
                    "from": "gpt",
                    "value": row['Message']
                }
            ]

            # One JSON object per line
            record = {
                "conversations": conversations
            }
            # print(json.dumps(record))

            fout.write(json.dumps(record, ensure_ascii=False) + "\n")


def big5_csv_to_jsonl(csv_file, jsonl_file):
    """
    Read a CSV with columns:
      - human
      - extraversion
      - agreeableness
      - conscientiousness
      - neuroticism
      - openness
    Write a JSONL, where each line is:
    {
      "messages": [
        {"from": "system", "value": "..."},
        {"from": "human", "value": "..."},
        {"from": "gpt",   "value": {...}}
      ]
    }
    """

    system_message = generate_big5_personality_prompt()

    with open(csv_file, "r", encoding="utf-8") as fin, open(jsonl_file, "w", encoding="utf-8") as fout:
        reader = csv.DictReader(fin)

        for row in reader:
            # Build the conversations array
            text = row['text'].strip()
            text = ' '.join(text.split())

            conversations = [
                {
                    "from": "system",
                    "value": system_message
                },
                {
                    "from": "human",
                    "value": text
                },
                {
                    "from": "gpt",
                    "value": str({
                        "extraversion": float(row["extraversion"]),
                        "agreeableness": float(row["agreeableness"]),
                        "conscientiousness": float(row["conscientiousness"]),
                        "neuroticism": float(row["neuroticism"]),
                        "openness": float(row["openness"])
                    })
                }
            ]

            # One JSON object per line
            record = {
                "conversations": conversations
            }

            print(json.dumps(record))

            #fout.write(json.dumps(record, ensure_ascii=False) + "\n")


def behavior_persona_csv_to_jsonl(csv_file, jsonl_file):
    """
    Task:
    - Read the text provided after 'Input Text:'.
    - Identify up to three (3) behavior classes from the list that best characterize the text.
    - If no relevant class is found, return an empty list: [].

    Output Format:
    - Return your final classification strictly as a JSON-like list
      (e.g., ["Mindful Eating", "Snacking Habits"]) or [].
    - Do not include additional commentary or explanation.
    """

    system_message = generate_eating_behavior_classify_prompt()

    with open(csv_file, "r", encoding="utf-8-sig") as fin, open(jsonl_file, "w", encoding="utf-8") as fout:
        reader = csv.DictReader(fin)

        for row in reader:
            # Build the conversations array
            text = row['Persona'].strip()
            text = ' '.join(text.split())

            conversations = [
                {
                    "from": "system",
                    "value": system_message
                },
                {
                    "from": "human",
                    "value": text
                },
                {
                    "from": "gpt",
                    "value": str(row["Behavior"])
                }
            ]

            # One JSON object per line
            record = {
                "conversations": conversations
            }

            fout.write(json.dumps(record, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    # Convert the Big Five CSV to JSONL
    # input_csv = "Data/big5_essays.csv"
    # output_jsonl = "Data/big5_finetuning_data.jsonl"
    # big5_csv_to_jsonl(input_csv, output_jsonl)
    # print(f"Done! Wrote JSONL to {output_jsonl}")

    # Convert the Behavior Persona CSV to JSONL
    input_csv = "Data/tips_dataset.csv"
    output_jsonl = "Data/tips_finetune.jsonl"
    tips_csv_to_jsonl(input_csv, output_jsonl)
    print(f"Done! Wrote JSONL to {output_jsonl}")
