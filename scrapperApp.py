import json
import time

import pandas as pd
import requests
from bs4 import BeautifulSoup

base_url = 'https://www.sciencebee.com.bd/qna'


def get_question_list(url_l, page_counter):
    data = []
    request_data = requests.get(url=url_l)
    counter = 0
    soup = BeautifulSoup(request_data.text, 'html.parser')
    time.sleep(10)
    questions_list = soup.find_all('div', {'class': 'qa-q-list-item'})
    for q in questions_list[1:]:
        try:

            question_tag_raw = q.find_all('li', {'class': 'qa-q-item-tag-item'})
            question_link = base_url + q.find('div', {'class': 'qa-q-item-title'}).a['href'].replace('.', '')
            number_of_answer = q.find('span', {'class': 'qa-a-count-data'}).text

            print(f"Page-{page_counter}: {q.find('div', {'class': 'qa-q-item-title'}).text.strip()} Number of Answer:{number_of_answer}")
            if number_of_answer != '0':
                request_data_answer = requests.get(question_link)

                soup_answer = BeautifulSoup(request_data_answer.text, 'html.parser')
                time.sleep(5)
                answer = soup_answer.find_all('div', {'class': 'qa-a-item-content qa-post-content'})
                print(len(answer))
                for x in answer:
                    temp = {
                        'id': f'p-{page_counter}-a-{counter}',
                        'question': q.find('div', {'class': 'qa-q-item-title'}).text.strip(),
                        'question_category': q.find('a', {'class': 'qa-category-link'}).text.strip(),
                        'number_of_answer': q.find('span', {'class': 'qa-a-count-data'}).text,
                        'number_of_vote': q.find('span', {'class': 'qa-netvote-count-data'}).text,
                        'number_of_view': q.find('span', {'class': 'qa-view-count-data'}).text,
                        'answer_link': question_link,
                        'question_tag': [x.text for x in question_tag_raw],
                        'answer': x.get_text(strip=True),
                    }
                    # temp1['id'] = f'p-{page_counter}-a-{counter}'
                    # temp1['answer'] = x.get_text(strip=True)
                    # print(temp1['answer'])
                    data.append(temp)
                    counter += 1
            else:
                temp = {
                    'id': f'p-{page_counter}-a-{None}',
                    'question': q.find('div', {'class': 'qa-q-item-title'}).text.strip(),
                    'question_category': q.find('a', {'class': 'qa-category-link'}).text.strip(),
                    'number_of_answer': q.find('span', {'class': 'qa-a-count-data'}).text,
                    'number_of_vote': q.find('span', {'class': 'qa-netvote-count-data'}).text,
                    'number_of_view': q.find('span', {'class': 'qa-view-count-data'}).text,
                    'answer_link': question_link,
                    'question_tag': [x.text for x in question_tag_raw],
                    'answer': None,
                }
                data.append(temp)
        except:
            continue
    df = pd.DataFrame(data)
    df.to_csv(f'./extracted/page_{page_counter}.csv', index=False)
    page_counter += 1
    try:
        pagination_has_next = soup.find('a', {'class': 'qa-page-next'})['href'].replace('.', '')
        url_p = base_url + pagination_has_next
        print('Next Page Url: ', url_p)
        get_question_list(url_l=url_p, page_counter=page_counter)
    except:
        exit()


if __name__ == '__main__':
    url = 'https://www.sciencebee.com.bd/qna/questions'
    get_question_list(url_l=url, page_counter=1)
