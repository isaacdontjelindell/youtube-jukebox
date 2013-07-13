from flask import Flask
from flask import request
from flask import render_template

from subprocess import call

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def jukebox():
    if request.method == 'POST':
        url = request.form['url']
        url = url + '&amp;vq=hd720'
        print url
        call(["cvlc", url, 'novideo'])
    return render_template('jukebox.html')
    
if __name__ == '__main__':
    app.run(host='0.0.0.0')
