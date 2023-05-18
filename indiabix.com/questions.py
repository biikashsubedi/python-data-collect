import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

pageList = ['00500']
firstUrl = 'https://www.indiabix.com/general-knowledge/basic-general-knowledge/'
mainUrl = firstUrl + pageList[0] + str(1)
response = requests.get(mainUrl)
soup = BeautifulSoup(response.text, 'html.parser')

divs = soup.find('div', class_='scrolly-250 scrolly-bg1').find_all('li')
divs.remove(divs[0])
params = [param.find('a')['href'].replace(firstUrl, '')[:-1] for param in divs]
pageSlugs = pageList + params

for slug in pageSlugs:
    for i in range(20):
        if i == 9:
            slug = slug[:-1]

        url = 'https://www.indiabix.com/general-knowledge/basic-general-knowledge/' + slug + str(i + 1)

        print(url)

        response = requests.get(url)
        if response.status_code == 404:
            print('Page does not exists..')
            continue

        soup = BeautifulSoup(response.text, 'html.parser')
        question_divs = soup.find_all('div', class_='bix-div-container')

        data = []
        for div in question_divs:
            question = div.find('div', class_='bix-td-qtxt').text.strip()
            answerLists = [answer.text.strip() for answer in div.find_all('div', class_='bix-td-option-val')]
            correctAnswerValue = div.find('input', class_='jq-hdnakq')['value']
            answer_key_mapping = {
                'A': 0,
                'B': 1,
                'C': 2,
                'D': 3,
            }
            correctAnswerKey = answer_key_mapping.get(correctAnswerValue, 0)
            correctAnswer = answerLists[correctAnswerKey]

            data.append([question, *answerLists, correctAnswer])
            continue

        new_df = pd.DataFrame(data, columns=['Question', 'Answer1', 'Answer2', 'Answer3', 'Answer4', 'Correct'])

        try:
            existing_df = pd.read_csv('questions.csv')
        except FileNotFoundError:
            existing_df = pd.DataFrame()

        if 'Question' in existing_df.columns:
            duplicate_questions = new_df[new_df['Question'].isin(existing_df['Question'])]
            new_df = new_df[~new_df['Question'].isin(duplicate_questions['Question'])]

        if not new_df.empty:
            updated_df = pd.concat([existing_df, new_df], ignore_index=True)
            updated_df.to_csv('questions.csv', index=False)
            print('Exported...')
        else:
            print('No new questions to export.')
