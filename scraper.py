import requests
from bs4 import BeautifulSoup
import os
import urllib.request
import json
import mimetypes
import cv2
from html.parser import HTMLParser

def scrapeAdidas (url, pronation, gender):
    shoes = []
    titles = []

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
    result = requests.get(url, headers = headers)

    resultContent = result.text
    soup = BeautifulSoup(resultContent, 'lxml')
    divs = soup.find_all('div', {'class': 'gl-product-card__media'})   


    count = 0
    titles = []
    for div in divs:
        x = div.find_all('a', {'class': 'gl-product-card__media-link'})[0]
        y = div.find_all('img')[0]

        href = 'https://www.adidas.com' + x['href']
        img = y['src']
        title = y['alt']
        if title in titles:
            continue
        titles.append(title)
        id = 'adidas' + pronation + str(count) + gender
        response = requests.get(img)
        content_type = response.headers['content-type']
        extension = mimetypes.guess_extension(content_type)
        urllib.request.urlretrieve(img, os.getcwd()+'/static/shoes/'+id+extension)
        im = cv2.imread(os.getcwd()+'/static/shoes/'+id+extension)
        resizedIm = cv2.resize(im, (128,128)) 
        cv2.imwrite(os.getcwd()+'/static/shoes/'+id+extension,resizedIm)
        shoes.append((title, id, href, extension,'Adidas', gender))
        count += 1
    return shoes
def scrapeAsics(url, sType, gender):
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
                id = 'asic' + sType + str(cnt) + gender
                cnt += 1
                urllib.request.urlretrieve(res['src'], os.getcwd()+'/static/shoes/'+id+extension)
                im = cv2.imread(os.getcwd()+'/static/shoes/'+id+extension)
                resizedIm = cv2.resize(im, (128,128)) 
                cv2.imwrite(os.getcwd()+'/static/shoes/'+id+extension,resizedIm)
                shoes.append(((title), id, href, extension,'Asics', gender))
                #nameOfShoe, brandPronationCount, linkToStore, extensionOfImage
    return shoes

def scrapeBrooks(url, pronation, gender):
    shoes = []
    titles = []

   
    result = requests.get(url)

    resultContent = result.text
    soup = BeautifulSoup(resultContent, 'lxml')
    divs = soup.find_all('div', {'class': 'product__card--wrapper'})   

    count = 0
    titles = []

    for div in divs:
        x = div.find_all('a', {'class': 'card__slider'})[0]
        y = div.find_all('img')[0]

        href =  x['href']
        img = y['data-src']
        title = y['alt']
        if title in titles:
            continue
        titles.append(title)
        id = 'brooks' + pronation + str(count) + gender
        response = requests.get(img)
        content_type = response.headers['content-type']
        extension = mimetypes.guess_extension(content_type)
        urllib.request.urlretrieve(img, os.getcwd()+'/static/shoes/'+id+extension)
        im = cv2.imread(os.getcwd()+'/static/shoes/'+id+extension)
        resizedIm = cv2.resize(im, (128,128)) 
        cv2.imwrite(os.getcwd()+'/static/shoes/'+id+extension,resizedIm)
        shoes.append((title, id, href, extension,'Brooks', gender))
        count += 1
    return shoes

def scrapeNike (url, pronation, gender):
    shoes = []
    titles = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
    result = requests.get(url, headers = headers)
    resultContent = result.text
    soup = BeautifulSoup(resultContent, 'lxml')

    divs = soup.find_all('div',{'class':'product-card__body'})
    # print(divs[0])

    count = 0
    for div in divs: 
        x = div.find_all('a')[0]
        href = x['href']

        title = x.find_all(text=True, recursive=False)[0]
        if title in titles:
            continue
        titles.append(title)
        # print(href)
        imgSoup = BeautifulSoup(requests.get(href).text, 'lxml')
        img = imgSoup.find_all('a', {'class': 'colorway-anchor'})
        # print(img)
        img = imgSoup.find_all('source')[0]['srcset']
        # print(div)
        id = 'nike' + pronation + str(count) + gender
        response = requests.get(img)
        content_type = response.headers['content-type']
        extension = mimetypes.guess_extension(content_type)
        urllib.request.urlretrieve(img, os.getcwd()+'/static/shoes/'+id+extension)
        im = cv2.imread(os.getcwd()+'/static/shoes/'+id+extension)
        # print(os.getcwd()+'/static/shoes/'+id+extension)
        resizedIm = cv2.resize(im, (128,128)) 
        cv2.imwrite(os.getcwd()+'/static/shoes/'+id+extension,resizedIm)
        shoes.append((title, id, href, extension,'Nike', gender))
        count += 1





    # f = open("sample.html", "w")
    # f.write(str(soup))
    # f.close()
    return shoes


def scrapeSaucony(url, pronation, gender ):
    shoes = []
    titles = []
    result = requests.get(url)
    resultContent = result.text
    soup = BeautifulSoup(resultContent, 'lxml')

    divs = soup.find_all('div', {'class': 'product-image'})
    count = 0
    
    for div in divs:
        x = div.find_all('a', {'class':'thumb-link'})[0]
        y = div.find_all('img')
        y = y[len(y) - 1]
        title = x['title']
        if (title in titles):
            continue
        titles.append(title)
        href = x['href']
        id = 'saucony' + pronation + str(count) + gender
        count += 1

        response = requests.get(y['src'])
        content_type = response.headers['content-type']
        extension = mimetypes.guess_extension(content_type)
        urllib.request.urlretrieve(y['src'], os.getcwd()+'/static/shoes/'+id+extension)
        im = cv2.imread(os.getcwd()+'/static/shoes/'+id+extension)
        resizedIm = cv2.resize(im, (128,128)) 
        cv2.imwrite(os.getcwd()+'/static/shoes/'+id+extension,resizedIm)
        shoes.append((title, id,href, extension,'Saucony', gender))



    # print(shoes)
    return shoes

def scrapeAll(pronation, gender):
    ADIDAS_OVERPRONATE_MALE = 'https://www.adidas.com/us/men-running-overpronation-shoes'
    ADIDAS_NEUTRAL_MALE = 'https://www.adidas.com/us/men-running-neutral-shoes'
    ADIDAS_UNDERPRONATE_MALE ='https://www.adidas.com/us/men-running-supination-shoes' 

    ASICS_OVERPRONATE_MALE = "https://www.asics.com/us/en-us/mens-running/c/aa10401000/overpronate/?start=0&sz=96&cb=1587260258090"  
    ASICS_NEUTRAL_MALE = "https://www.asics.com/us/en-us/mens-running/c/aa10401000/neutral/?start=0&sz=96&cb=1587260258090"
    ASICS_UNDERPRONATE_MALE = "https://www.asics.com/us/en-us/mens-running/c/aa10401000/underpronate/?start=0&sz=96&cb=1587260258090"

    BROOKS_OVERPRONATE_MALE = 'https://www.brooksrunning.com/en_us/mens-road-running-shoes/?prefn0=arch&prefv0=flat'
    BROOKS_NEUTRAL_MALE = 'https://www.brooksrunning.com/en_us/mens-road-running-shoes/?prefn1=arch&prefv1=medium&sz=97'
    BROOKS_UNDERPRONATE_MALE = 'https://www.brooksrunning.com/en_us/mens-road-running-shoes/?prefn1=arch&prefv1=high&sz=88'
    
    NIKE_OVERPRONATE_MALE = 'https://www.nike.com/w/mens-running-cross-training-shoes-2lnrvz37v7jznik1zy7ok'
    NIKE_NEUTRAL_MALE = 'https://www.nike.com/w/mens-running-neutral-shoes-1a1ppz37v7jznik1zy7ok'
    NIKE_UNDERPRONATE_MALE = 'https://www.nike.com/w/mens-cushioning-running-neutral-shoes-1a1ppz37v7jz3ivq7znik1zy7ok'

    SAUCONY_OVERPRONATE_1_MALE = "https://www.saucony.com/en/featured-shop-all-mens/?prefn1=isOnSale&prefv1=false&prefn2=pronation&prefv2=maximum"
    SAUCONY_OVERPRONATE_2_MALE = "https://www.saucony.com/en/featured-shop-all-mens/?prefn1=isOnSale&prefv1=false&prefn2=pronation&prefv2=moderate"
    SAUCONY_NEUTRAL_MALE = "https://www.saucony.com/en/featured-shop-all-mens/?prefn1=isOnSale&prefv1=false&prefn2=pronation&prefv2=neutral"
    SAUCONY_UNDERPRONATE_MALE = "https://www.saucony.com/en/featured-shop-all-mens/#prefn1=isOnSale&prefv1=false&prefn2=pronation&prefv2=supination"

    ADIDAS_OVERPRONATE_FEMALE = 'https://www.adidas.com/us/women-running-overpronation-shoes'
    ADIDAS_NEUTRAL_FEMALE = 'https://www.adidas.com/us/women-running-neutral-shoes'
    ADIDAS_UNDERPRONATE_FEMALE = 'https://www.adidas.com/us/women-running-supination-shoes'

    ASICS_OVERPRONATE_FEMALE =   "https://www.asics.com/us/en-us/women/c/aa20000000/overpronate/"
    ASICS_NEUTRAL_FEMALE = "https://www.asics.com/us/en-us/women/c/aa20000000/neutral/"
    ASICS_UNDERPRONATE_FEMALE = "https://www.asics.com/us/en-us/women/c/aa20000000/underpronate/"

    BROOKS_OVERPRONATE_FEMALE = 'https://www.brooksrunning.com/en_us/womens-road-running-shoes/?prefn0=arch&prefv0=flat'
    BROOKS_NEUTRAL_FEMALE = 'https://www.brooksrunning.com/en_us/womens-road-running-shoes/?prefn0=arch&prefv0=medium'
    BROOKS_UNDERPRONATE_FEMALE = 'https://www.brooksrunning.com/en_us/womens-road-running-shoes/?prefn0=arch&prefv0=high'
    
    NIKE_OVERPRONATE_FEMALE = 'https://www.nike.com/w/womens-running-cross-training-shoes-2lnrvz37v7jz5e1x6zy7ok'
    NIKE_NEUTRAL_FEMALE = 'https://www.nike.com/w/womens-running-neutral-shoes-1a1ppz37v7jz5e1x6zy7ok'
    NIKE_UNDERPRONATE_FEMALE = 'https://www.nike.com/w/womens-cushioning-running-neutral-shoes-1a1ppz37v7jz3ivq7z5e1x6zy7ok'
    
    SAUCONY_OVERPRONATE_1_FEMALE = "https://www.saucony.com/en/womens-running/#prefn1=isOnSale&prefv1=false&prefn2=pronation&prefv2=maximum"
    SAUCONY_OVERPRONATE_2_FEMALE = "https://www.saucony.com/en/womens-running/#prefn1=isOnSale&prefv1=false&prefn2=pronation&prefv2=moderate"
    SAUCONY_NEUTRAL_FEMALE = "https://www.saucony.com/en/womens-running/#prefn1=isOnSale&prefv1=false&prefn2=pronation&prefv2=neutral"
    SAUCONY_UNDERPRONATE_FEMALE = "https://www.saucony.com/en/womens-running/#prefn1=isOnSale&prefv1=false&prefn2=pronation&prefv2=supination&start=0&sz=12"

    shoes = []
    if (pronation == 'neutral'):
        if gender == 'male':
            shoes += scrapeAdidas(ADIDAS_NEUTRAL_MALE, pronation, 'male')
            shoes += scrapeAsics(ASICS_NEUTRAL_MALE, pronation, 'male')
            shoes += scrapeBrooks(BROOKS_NEUTRAL_MALE, pronation, 'male')
            shoes += scrapeNike(NIKE_NEUTRAL_MALE, pronation, 'male')
            shoes += scrapeSaucony(SAUCONY_NEUTRAL_MALE, pronation, 'male')
        else:
            shoes += scrapeAdidas(ADIDAS_NEUTRAL_FEMALE, pronation, 'female')
            shoes += scrapeAsics(ASICS_NEUTRAL_FEMALE, pronation, 'female')
            shoes += scrapeBrooks(BROOKS_NEUTRAL_FEMALE, pronation, 'female')
            shoes += scrapeNike(NIKE_NEUTRAL_FEMALE, pronation, 'female')
            shoes += scrapeSaucony(SAUCONY_NEUTRAL_FEMALE, pronation, 'female')
    elif (pronation == 'underpronation'):
        if gender == 'male':
            shoes += scrapeAdidas(ADIDAS_UNDERPRONATE_MALE, pronation, 'male')
            shoes += scrapeAsics(ASICS_UNDERPRONATE_MALE, pronation, 'male')
            shoes += scrapeBrooks(BROOKS_UNDERPRONATE_MALE, pronation, 'male')
            shoes += scrapeNike(NIKE_UNDERPRONATE_MALE, pronation, 'male')
            shoes += scrapeSaucony(SAUCONY_UNDERPRONATE_MALE, pronation, 'male')
        else:
            shoes += scrapeAdidas(ADIDAS_UNDERPRONATE_FEMALE, pronation,'female')
            shoes += scrapeAsics(ASICS_UNDERPRONATE_FEMALE, pronation, 'female')
            shoes += scrapeBrooks(BROOKS_UNDERPRONATE_FEMALE, pronation, 'female')
            shoes += scrapeNike(NIKE_UNDERPRONATE_FEMALE, pronation, 'female')
            shoes += scrapeSaucony(SAUCONY_UNDERPRONATE_FEMALE, pronation, 'female')
    elif (pronation == 'overpronation'):
        if gender == 'male':
            shoes += scrapeAdidas(ADIDAS_OVERPRONATE_MALE,pronation, 'male')
            shoes += scrapeAsics(ASICS_OVERPRONATE_MALE, pronation, 'male')
            shoes += scrapeBrooks(BROOKS_OVERPRONATE_MALE, pronation, 'male')
            shoes += scrapeNike(NIKE_OVERPRONATE_MALE, pronation, 'male')
            shoes += scrapeSaucony(SAUCONY_OVERPRONATE_1_MALE, pronation, 'male')
            shoes += scrapeSaucony(SAUCONY_OVERPRONATE_2_MALE, pronation, 'male')
        else:
            shoes += scrapeAdidas(ADIDAS_OVERPRONATE_FEMALE, pronation, 'female')
            shoes += scrapeAsics(ASICS_OVERPRONATE_FEMALE, pronation, 'female')
            shoes += scrapeBrooks(BROOKS_OVERPRONATE_FEMALE, pronation, 'female')
            shoes += scrapeNike(NIKE_OVERPRONATE_FEMALE, pronation, 'female')
            shoes += scrapeSaucony(SAUCONY_OVERPRONATE_1_FEMALE, pronation, 'female')
            shoes += scrapeSaucony(SAUCONY_OVERPRONATE_2_FEMALE, pronation, 'female')


    return shoes
scrapeNike('https://www.nike.com/w/mens-running-neutral-shoes-1a1ppz37v7jznik1zy7ok', 'neutral', 'male')
# scrapeNike('https://www.nike.com/w/mens-running-neutral-shoes-1a1ppz37v7jznik1zy7ok', 'neutral', 'male')
# print (scrapeAdidas('https://www.adidas.com/us/men-running-neutral-shoes', 'neutral', 'male'))

# # scrapeSaucony('https://www.saucony.com/en/featured-shop-all-mens/?prefn1=isOnSale&prefv1=false&prefn2=pronation&prefv2=neutral', 'neutral', 'male')
            
# scrapeBrooks('https://www.brooksrunning.com/en_us/mens-road-running-shoes/?prefn0=arch&prefv0=flat', 'overpronate', 'male')



