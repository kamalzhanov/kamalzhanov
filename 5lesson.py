from bs4 import BeautifulSoup
import requests

count_news = 0
for page in range(1, 11):
    url = f'https://24.kg/page_{page}'
    response = requests.get(url)
    print(response)
    soup = BeautifulSoup(response.text, "lxml")
    
    all_news = soup.find_all('div', class_='title')
    
    for news in all_news:
        count_news += 1
        print(news.text)

    with open('allnews.txt', 'w', encoding='utf-8') as file:
        for news in all_news:
            new_text = " ".join(news.text.split())
            file.write(f"{new_text}\n")
