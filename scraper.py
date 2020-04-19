import requests
from bs4 import BeautifulSoup
import os
import urllib.request
import json 
from html.parser import HTMLParser


def scrapeAsics(url):
    result = requests.get(url)
    resultContent = result.text
    # print(result.status_code)
    # print(resultContent)

    soup = BeautifulSoup(resultContent, 'lxml')
    links = soup.find_all('div', {'class': 'pt_product-search-result'})
    x = links[0].find_all('div',  {'class': 'product-tile asics'})

    titles = []
    shoes = []

    for tag in x:

        pretag = tag.find_all('a', class_ = 'thumb-link')
        href = str(pretag[0])
        start = href.index('href="')
        href = href[start + 6:]
        href = href[:href.index('"') + 1]

        newTag = str(pretag[0])


        # newTag = tag.find_all('img', class_ = 'b-lazy js-product-thumb-img')[0]
        # newTag = str(newTag)
        if "data-alt-image='" in newTag:
            start = newTag.index("data-alt-image='")
            newString = newTag[start+16:]
            i = newString.index('}')
            newString = newString[:i+1]

            res = json.loads(newString)

            title = res['title'].strip()

            if '&' in title:
                title = title[:title.index('&')]
                title = title.strip()

            if not(title in titles):
                titles.append(title)
                shoes.append(((title), res['src'], href))

    return shoes

ASICS_OVERPRONATE = "https://www.asics.com/us/en-us/mens-running/c/aa10401000/overpronate/?start=0&sz=96&cb=1587260258090"

ASICS_NEUTRAL = "https://www.asics.com/us/en-us/mens-running/c/aa10401000/neutral/?start=0&sz=96&cb=1587260258090"

ASICS_UNDERPRONATE = "https://www.asics.com/us/en-us/mens-running/c/aa10401000/underpronate/?start=0&sz=96&cb=1587260258090"





