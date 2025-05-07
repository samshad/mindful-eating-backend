import pandas as pd


if __name__ == '__main__':
    df = pd.read_csv('Data/persuasive_messages_behavior_big5.csv')

    arr_tips = []

    for index, row in list(df.iterrows()):
        arr = row['Behavior_Big5']
        # Remove the square brackets and split the string by the comma and space
        string_list = arr[1:-1].split(', ')

        req = {
            'Eating Behavior': string_list[0],
            'Dominant Big5': string_list[1]
        }

        arr_tips.append([req, row['Message']])

    tf = pd.DataFrame(arr_tips, columns=['Behavior_Big5', 'Message'])
    tf.to_csv('Data/tips_dataset.csv', index=False, encoding='utf-8-sig')
