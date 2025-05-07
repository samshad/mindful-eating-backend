import pandas as pd
import json
import os


def main():
    df = pd.read_csv('Data/essays.csv')

    arr = []

    for index, row in list(df.iterrows()):
        file = row['#AUTHID'] + '.json'

        with open('Data/big5/' + file, 'r') as f:
            big5_data = json.load(f)

        print(big5_data['extraversion'],
              big5_data['agreeableness'],
              big5_data['conscientiousness'],
              big5_data['neuroticism'],
              big5_data['openness'],
              '\n',
              row['cEXT'],
              row['cAGR'],
              row['cCON'],
              row['cNEU'],
              row['cOPN'])

        arr.append(
            [
                row['#AUTHID'],
                row['text'],
                big5_data['extraversion'],
                big5_data['agreeableness'],
                big5_data['conscientiousness'],
                big5_data['neuroticism'],
                big5_data['openness'],
                row['cEXT'],
                row['cAGR'],
                row['cCON'],
                row['cNEU'],
                row['cOPN']
                ]
            )

    tf = pd.DataFrame(arr, columns=[
        '#AUTHID',
        'text',
        'extraversion',
        'agreeableness',
        'conscientiousness',
        'neuroticism',
        'openness',
        'cEXT',
        'cAGR',
        'cCON',
        'cNEU',
        'cOPN'
    ])
    tf.to_csv('Data/big5_essays.csv', encoding='utf-8', index=False)


if __name__ == '__main__':
    main()
