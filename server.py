from flask import Flask, render_template, request, json
import os
import proj
import time
import scraper
import math

UPLOAD_FOLDER = '/uploads'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

imageOperator = proj.Imaging()



@app.route('/findArchtype')
def upload_file():
   return render_template('main.html')
	
@app.route('/archtype', methods = ['GET', 'POST'])
def archtype():
   if request.method == 'POST':
      f = request.files['file']
      millis = int(round(time.time() * 1000))
      newPath = os.getcwd() + '/uploads/' + str(millis) + f.filename
      f.save(newPath)
      archIndex = imageOperator.getIndex(newPath)
      os.remove(newPath)
      # # High arch (AI≤0.21)
      # Normal arch (AI between 0.21 and 0.26) and
      # Low arch (AI≥0.26)
      pronation = ''
      comment = ''

      if (archIndex <= .21):
         pronation = 'underpronation'
         comment = 'You have a high arch. Your arch index is: ' + str(archIndex)

      elif (archIndex > .21 and archIndex < .26):
         pronation ='neutral pronation'
         comment = 'You have a normal arch. Your arch index is: ' + str(archIndex)

      else:
         pronation = 'overpronation'
         comment = 'You have a low arch. Your arch index is: ' + str(archIndex)

      render = '<html><header><title>'+ pronation +'</title></header> <body>'
      render += '<h1>' + comment + '</h1>'

      table = '<table>'
      shoelist = scraper.scrapeAll(pronation)

      td = []
      for shoe in shoelist:
         td.append('<td><a href="' + shoe[2] +'"><img src="' +os.getcwd()+'/shoes/'+ shoe[1] + shoe[3] + '"/></a>' +'<br/>'+ shoe[0]+'</td>')

      columnCount = 5
      print(shoelist)
      count = 0
      for i in range(math.ceil(len(td)/columnCount)):
         table += '<tr>'
         for j in range(5):
            if(count < len(td)):
               table += td[count]
               count += 1

         table += '</tr>'
         


      table += '</table>'

      render += table


      render += '</body></html>'
      print(render)
      return render
if __name__ == '__main__':
   app.run(debug = True)