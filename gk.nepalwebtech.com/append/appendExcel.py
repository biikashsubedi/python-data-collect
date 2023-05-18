import pandas as pd

# Read the first CSV file
df1 = pd.read_csv('output.csv')

# Read the second CSV file
df2 = pd.read_csv('cleanCorrectAnswers.csv')

# Merge the two dataframes based on the common columns
merged_df = pd.merge(df1, df2, on='Question')

# Rename the "Correct_y" column to "Correct"
merged_df.rename(columns={'Correct_y': 'Correct'}, inplace=True)

# Drop the unnecessary columns
merged_df.drop(columns=['Correct_x'], inplace=True)

# Save the merged dataframe to a new CSV file
merged_df.to_csv('finalQuestionsList.csv', index=False)
