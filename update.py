import scraper
import math
import os

def update(pronation, gender):
    shoelist = scraper.scrapeAll(pronation, gender)
    f = open(os.getcwd() + '/static/shoes/'+gender+ pronation +'.txt', "w")
    s = ''
    for shoe in shoelist:
        #  brand   name   image       url
        s += shoe[4] + '~' + shoe[0] + '~' + '/static/shoes/'+ shoe[1] + shoe[3]+ '~' + shoe[2] + '~' + gender + '\n'
    f.write(s)
    f.close()

def updateAll():
    update('neutral', 'male')
    update('underpronation', 'male')
    update('overpronation', 'male')
    update('neutral', 'female')
    update('underpronation', 'female')
    update('overpronation', 'female')
updateAll()