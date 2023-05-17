import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

url = "https://gk.nepalwebtech.com/"
response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')
question_divs = soup.find_all('div', class_='block')

data = []
for div in question_divs:
    question = div.find('div', class_='quest').text.strip().split(":", 1)[1].strip()
    answer_options = [option.text.strip() for option in div.find_all('li')]
    data.append([question, *answer_options])
    continue

new_df = pd.DataFrame(data, columns=['Question', 'Answer1', 'Answer2', 'Answer3', 'Answer4'])

try:
    existing_df = pd.read_csv('output.csv')
except FileNotFoundError:
    existing_df = pd.DataFrame()

if 'Question' in existing_df.columns:
    duplicate_questions = new_df[new_df['Question'].isin(existing_df['Question'])]
    new_df = new_df[~new_df['Question'].isin(duplicate_questions['Question'])]

if not new_df.empty:
    updated_df = pd.concat([existing_df, new_df], ignore_index=True)
    updated_df.to_csv('output.csv', index=False)
    print('Exported...')
else:
    print('No new questions to export.')

# proceed for answers
question_answer_list = soup.select('#ticker01 li')

data = []
for item in question_answer_list:
    question = item.text.strip().split(") ", 1)[1].split(" ANS:")[0]
    answer = re.search(r'ANS: (.+)', item.text.strip()).group(1)
    data.append([question, answer])
    continue

new_df = pd.DataFrame(data, columns=['Question', 'Correct'])

try:
    existing_df = pd.read_csv('correctAnswers.csv')
except FileNotFoundError:
    existing_df = pd.DataFrame()

if 'Question' in existing_df.columns:
    duplicate_questions = new_df[new_df['Question'].isin(existing_df['Question'])]
    new_df = new_df[~new_df['Question'].isin(duplicate_questions['Question'])]

if not new_df.empty:
    updated_df = pd.concat([existing_df, new_df], ignore_index=True)
    updated_df.to_csv('correctAnswers.csv', index=False)
    print('correct answer updated...')
else:
    print('No new questions to export.')
