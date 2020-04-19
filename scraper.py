import requests
from bs4 import BeautifulSoup
import os
import urllib.request
import json
import mimetypes
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
    cnt = 0
    for tag in x:

        pretag = tag.find_all('a', class_ = 'thumb-link')
        href = str(pretag[0])
        start = href.index('href="')
        href = href[start + 6:]
        href = href[:href.index('"') ]

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
                response = requests.get(res['src'])
                content_type = response.headers['content-type']
                extension = mimetypes.guess_extension(content_type)
                id = 'asic' + str(cnt)
                cnt += 1
                urllib.request.urlretrieve(res['src'], os.getcwd()+'/shoes/'+id+extension)
                shoes.append(((title), id, href, extension))


    return shoes

def scrapeAll(pronation):
    ASICS_OVERPRONATE = "https://www.asics.com/us/en-us/mens-running/c/aa10401000/overpronate/?start=0&sz=96&cb=1587260258090"

    ASICS_NEUTRAL = "https://www.asics.com/us/en-us/mens-running/c/aa10401000/neutral/?start=0&sz=96&cb=1587260258090"

    ASICS_UNDERPRONATE = "https://www.asics.com/us/en-us/mens-running/c/aa10401000/underpronate/?start=0&sz=96&cb=1587260258090"
    

    shoes = []
    if (pronation == 'neutral pronation'):
        shoes += scrapeAsics(ASICS_NEUTRAL)
    elif (pronation == 'underpronation'):
        shoes += scrapeAsics(ASICS_UNDERPRONATE)
    elif (pronation == 'overpronation'):
        shoes += scrapeAsics(ASICS_OVERPRONATE)

    return shoes

            




