import pandas as pd

df = pd.read_csv('Data/eating_behaviors.csv')

behavior_class = list(df['Behavior'].unique())

big5_personality_trait = [
    'Extraversion',
    'Agreeableness',
    'Conscientiousness',
    'Neuroticism',
    'Openness'
]

arr = []

# print all permutations a and b of length 2
for i in range(len(behavior_class)):
    for j in range(len(big5_personality_trait)):
        behavior_big5 = [behavior_class[i], big5_personality_trait[j]]
        print(behavior_big5)

        prompt = f"""Imagine you are a dietitian, crafting personalized, persuasive messages to guide individual toward mindful eating.
You have been provided with eating behavior and one big5 personality trait of the individual.

**Eating Behavior to Address:**

{behavior_class[i]}

**Big5 Personality Trait:**

{big5_personality_trait[j]}

**Task:**
Write at least 30 persuasive messages (acting as a dietitian) that serve as gentle reminders and actionable guidelines for mindful eating.  These messages should:
- **Be specifically tailored to the given big5_personality_trait and the Eating Behavior.**
- **Promote mindful eating practices**
- **Adopt a supportive, empathetic, and knowledgeable dietitian's tone.** Be encouraging and avoid being judgmental.
- **Provide practical and actionable advice.** Think of these as short, impactful tips individual can easily incorporate into their daily life.
- **Build upon individual's existing awareness and positive changes**

**Desired Tone:**  Empathetic, supportive, encouraging, knowledgeable, and action-oriented dietitian.

Generate a CSV file containing at least 30 personalized, persuasive messages. The CSV should have two columns:

Behavior_Big5 - A combined label for the eating behavior and Big5 personality trait as a list (e.g., ['Mindful vs. Distracted Eating, Extraversion']).
Message - The persuasive message.
The CSV should follow this structure:

Behavior_Big5	Message
...	...

Output the final result in CSV format."""

        print(prompt)
        arr.append([behavior_big5, prompt])

tf = pd.DataFrame(arr, columns=['Behavior_Big5', 'Prompt'])
tf.to_csv('Data/prompt_behavior_big5.csv', index=False)

