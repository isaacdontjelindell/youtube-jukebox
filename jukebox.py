from flask import Flask
from flask import request
from flask import render_template

from subprocess import call
from subprocess import Popen
from Queue import Queue

import sys
import telnetlib
import time

# start VLC with the telnet control interface enabled
vlc_pid = Popen(['vlc', '--extraintf', 'telnet'])
time.sleep(1)

# make a connection to the telnet interface
tn = telnetlib.Telnet('localhost', 4212)
tn.read_until("Password:")
tn.write('jukebox\n')
time.sleep(.5)

playing = False

# start the Flask listener
app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def jukebox():
    if request.method == 'POST':
        url = request.form['url']
        url = url + "&amp;vq=small"
        enqueue(url)
    return render_template('jukebox.html')

def enqueue(url):
    tn.write('enqueue ' + url.encode('ascii') + '\n')
    if not playing:
        time.sleep(0.5)
        tn.write('play\n')
        playing = True
    #time.sleep(1)
    #tn.write("vtrack -1\n") # disable video

if __name__ == '__main__':
    app.run(host='0.0.0.0')
