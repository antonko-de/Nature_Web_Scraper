import re
import string

import requests
from bs4 import BeautifulSoup

import os
# all the modules needed for this stage #
number_of_pages = int(input())
artic_type = input()
# receive user input for the number of pages and article type #
for page in range(1, number_of_pages + 1):
    # a loop for checking all the pages required #
    current_page = str(page)
    url = f'https://www.nature.com/nature/articles?sort=PubDate&year=2020&page={current_page}'
    r = requests.get(url)
    os.mkdir(f'Page_{current_page}')
    os.chdir(f'Page_{current_page}')
    # dir creation for the current page #

    if r.status_code == 200:
        soup = BeautifulSoup(r.content, 'html.parser')
        article = soup.find_all('article')
        # check for connection and get all the page content #

        for x in article:
            # loop through the page content searching for the article type #
            article_type = x.find('span', attrs={'data-test': 'article.type'})
            _string = x.find(string=re.compile(artic_type))
            # use the re.compile for smalles resource use later #

            if _string == artic_type:
                # format the name #
                link = x.find('a', attrs={'data-track-action': 'view article'}).text.strip()
                name = link.translate(str.maketrans(" ", "_", string.punctuation)) + ".txt"


                article_url = f"https://www.nature.com{x.a.get('href')}"
                # get the body#
                r2 = requests.get(article_url)
                soup2 = BeautifulSoup(r2.content, 'html.parser')
                text = soup2.find('div', {'class': 'c-article-body'}).text.strip()


                file = open(name, 'wb')
                file.write(text.encode('utf-8'))
                file.close()

    os.chdir('/home/anton/PycharmProjects/Web Scraper/Web Scraper/task/')