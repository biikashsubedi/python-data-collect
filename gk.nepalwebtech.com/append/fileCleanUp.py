import pandas as pd

# Read the merged CSV file
merged_df = pd.read_csv('correctAnswers.csv')

# Replace NBSP with a regular space in the "Correct" column
merged_df['Question'] = merged_df['Question'].str.replace('\xa0', '').str.replace(r'\?\s*', '?', regex=True).str.replace(r'\।\s*', '।', regex=True)

# Save the updated dataframe to a new CSV file
merged_df.to_csv('cleanCorrectAnswers.csv', index=False)