import requests
from bs4 import BeautifulSoup

url = 'https://www.sciencebee.com.bd/qna/32945/%E0%A6%9C%E0%A7%87%E0%A6%A8%E0%A7%8B%E0%A6%AC%E0%A6%9F-%E0%A6%A7%E0%A6%B0%E0%A6%A8%E0%A7%87%E0%A6%B0'
#
request_data = requests.get(url=url)
# print(request_data.text)
# with open('textanswer1.txt', 'r',  encoding="utf-8") as file:
#     request_data = file.read()

soup = BeautifulSoup(request_data.text, 'html.parser')

answer = soup.find_all('div', {'class': 'qa-a-item-content qa-post-content'})
print(answer[0].get_text(strip=True))