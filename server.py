from flask import Flask, render_template, request
import os
import proj
import time

UPLOAD_FOLDER = '/uploads'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

imageOperator = proj.Imaging()

@app.route('/findArchtype')
def upload_file():
   return render_template('main.html')
	
@app.route('/archtype', methods = ['GET', 'POST'])
def upload_filese():
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
      if (archIndex <= .21):
         return 'You have a high arch. Your arch index is: ' + str(archIndex)

      elif (archIndex > .21 and archIndex < .26):
         return 'You have a normal arch. Your arch index is: ' + str(archIndex)

      else:
         return 'You have a low arch. Your arch index is: ' + str(archIndex)
if __name__ == '__main__':
   app.run(debug = True)