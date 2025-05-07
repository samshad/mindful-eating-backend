import pandas as pd


def main():
    df = pd.read_csv('Data/big5_essays.csv')

    arr = []

    for index, row in list(df.iterrows()):
        print(row['extraversion'], row['agreeableness'], row['conscientiousness'], row['neuroticism'], row['openness'])

        scores = {
            'extraversion': row['extraversion'],
            'agreeableness': row['agreeableness'],
            'conscientiousness': row['conscientiousness'],
            'neuroticism': row['neuroticism'],
            'openness': row['openness']
        }
        max_trait = max(scores, key=scores.get)
        max_score = scores[max_trait]

        print(scores)
        print(f'Highest trait: {max_trait}, Value: {max_score}')

        text = row['text'].strip()
        text = ' '.join(text.split())

        arr.append([text,
                    row['extraversion'],
                    row['agreeableness'],
                    row['conscientiousness'],
                    row['neuroticism'],
                    row['openness'],
                    max_trait
                    ])

    df = pd.DataFrame(arr, columns=['text', 'extraversion', 'agreeableness', 'conscientiousness', 'neuroticism', 'openness', 'dominant'])
    df.to_csv('Data/big5_essays_dominant.csv', index=False, encoding='utf-8')


if __name__ == '__main__':
    main()