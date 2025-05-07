import pandas as pd
import http.client
import json
import os

from time import sleep
from random import choice


def check_file_exists(filename):
    return os.path.exists("Data/big5/" + filename)


def get_big5_symanto(text_data):
    conn = http.client.HTTPSConnection("big-five-personality-insights.p.rapidapi.com")

    payload = json.dumps([
        {
            "id": "1",
            "language": "en",
            "text": text_data
        }
    ])

    headers = {
        'x-rapidapi-key': "",
        'x-rapidapi-host': "big-five-personality-insights.p.rapidapi.com",
        'Content-Type': "application/json"
    }

    conn.request("POST", "/api/big5", payload, headers)

    res = conn.getresponse()
    data = res.read()

    return data.decode("utf-8")


def write_to_json(data, filename):
    with open("Data/big5/" + filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print("Data written to " + filename)


def main():
    df = pd.read_csv("Data/essays.csv")

    # print(len(df['#AUTHID'].unique()))
    sleep_timers = [5, 10, 15, 20, 25]
    cnt = 1

    for index, row in list(df.iterrows()):
        print(row['#AUTHID'])
        print("Count: ", cnt)
        cnt += 1

        filename = row['#AUTHID'] + ".json"

        if check_file_exists(filename):
            print("File exists! Skipping...")
            continue

        big5_symanto = get_big5_symanto(row['text'])

        print(big5_symanto)

        big5_symanto = json.loads(big5_symanto)[0]
        print(big5_symanto)

        write_to_json(big5_symanto, filename)

        lets_sleep = choice(sleep_timers)
        print(f"Sleeping for {lets_sleep} seconds!")
        sleep(lets_sleep)


if __name__ == "__main__":
    main()


