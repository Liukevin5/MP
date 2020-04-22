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

@app.route('/')
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

      gender = request.form['gender']



      if (archIndex <= .21):
         pronation = 'underpronation'
         comment = 'You have a high arch. Your arch index is: ' + str(archIndex)


      elif (archIndex > .21 and archIndex < .26):
         pronation ='neutral'
         comment = 'You have a normal arch. Your arch index is: ' + str(archIndex)

      else:
         pronation = 'overpronation'
         comment = 'You have a low arch. Your arch index is: ' + str(archIndex)
      #brand name img url
      shoelist = []

      with open(os.getcwd() + '/static/shoes/'+ gender+pronation +'.txt') as fp:
         line = fp.readline()
         while line:
            temp = line.strip()
            temp = temp.split('~')
            print(temp[4], gender)
            if temp[4] == gender:
               shoelist.append((temp[0], temp[1], temp[2], temp[3]))
            
            line = fp.readline()

      
      if gender == 'male':
         gender = "Men's"
      else: 
         gender = "Women's"
  
      render = '<html><header><title>'+ gender + ' ' + pronation+' shoes</title><link rel="stylesheet" href="'+ '/static/styles.css"></header><body>'

      table = '<table>'


      td = []
      for shoe in shoelist:
         td.append('<td style="word-wrap: break-word"><a href="' + shoe[3] +'"><div><img src="' + shoe[2] + '"/>' +'<br/>'+ shoe[1]+'</div></a></td>')

      columnCount = 5
      # print(shoelist)
      count = 0

      if pronation == 'neutral':
         render += '<h2>' + gender + ' Neutral Running Shoes</h2></tr>'
      if pronation == 'overpronation':
         render += '<h2>' + gender + ' Overpronation Running Shoes</h2></tr>'
      if pronation == 'underpronation':
         render += '<h2>' + gender + ' Underpronation Running Shoes</h2></tr>'

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


      return render





if __name__ == '__main__':
   app.run(debug = True)