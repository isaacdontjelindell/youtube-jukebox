from flask import Flask
from flask import request
from flask import render_template

from subprocess import call

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def jukebox():
    if request.method == 'POST':
        url = request.form['url']
        print url + "&amp;vq=small"
        call(["vlc", " --intf telnet", '''--lua-config "telnet={host='0.0.0.0:4212'}"''', "--novideo", url])
    return render_template('jukebox.html')
    
if __name__ == '__main__':
    app.run(host='0.0.0.0')
