from flask import Flask
from flask import request
from flask import render_template
from selenium import webdriver
from threading import Lock
import urlparse
import json


# start the Flask listener
app = Flask(__name__)

# open the browser
driver = webdriver.Firefox()

# play queue - contains video ids to be played
playlist = []
lock = Lock()  # to allow concurrent usage


@app.route('/', methods=['POST', 'GET'])
def jukebox():
    if request.method == 'POST':
        url = request.form['url']
        enqueue(url)

    return render_template('jukebox.html')

def enqueue(url):
    # parse the url to get the video id
    # http://www.youtube.com/watch?v=39RrLTNyGTM
    url_data = urlparse.urlparse(url)
    query = urlparse.parse_qs(url_data.query)
    video_id = query["v"][0]
    with lock:
        playlist.append(video_id)

    if not 'player' in driver.current_url:
        driver.get("http://localhost:5000/player")

@app.route('/pause', methods=['POST'])
def pause():
    driver.execute_script("player.pauseVideo()")
    return ""

@app.route('/play', methods=['POST'])
def play():
    driver.execute_script("player.playVideo()")
    return ""

## Generate the server-side player page ##
@app.route('/player', methods=['GET'])
def player():
    return render_template('player.html')

## Return a video id if the playlist isn't empty,
## otherwise return empty string
@app.route('/getnextvideo', methods=['POST'])
def getnextvideo():
    with lock:
        if len(playlist) == 0:
            return ''
        else:
            vid = playlist.pop(0)
            print 'sending video %s' % vid
            return vid

@app.route('/getplaylist', methods=['POST'])
def getplaylist():
    with lock:
        return json.dumps(playlist)


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
    #app.run(host='0.0.0.0', debug=True)

