import pandas as pd


def normalize_rank(df):
    arr = []

    for i, r in df.iterrows():
        if r['rank'] > 2:
            arr.append([r['input'], r['output'], r['rank'], 1])
        else:
            arr.append([r['input'], r['output'], r['rank'], 0])

    tf = pd.DataFrame(arr, columns=['input', 'output', 'rank', 'acceptance'])
    tf.to_csv('Data/model_accuracy/tips-testcases - ranked.csv', index=False)


def main():
    df_mine = pd.read_csv("Data/model_accuracy/tips2-testcases - mine.csv")
    df_gpt = pd.read_csv("Data/model_accuracy/tips2-testcases - GPTo3.csv")
    df_sonnet = pd.read_csv("Data/model_accuracy/tips2-testcases - Sonnet3.7.csv")

    # Normalize the ranks
    normalize_rank(df_mine)


if __name__ == "__main__":
    main()
