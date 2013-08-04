from flask import Flask
from flask import request
from flask import render_template
from selenium import webdriver
from Queue import Queue
import urlparse


# start the Flask listener
app = Flask(__name__)

# open the browser
driver = webdriver.Firefox()

# play queue - contains video ids to be played
queue = Queue()

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
    queue.put(video_id)

    #if not 'player' in driver.current_url:
    #    driver.get("http://localhost:5000/player")

@app.route('/pause', methods=['POST'])
def pause():
    driver.execute_script("player.pauseVideo()")
    return ""

@app.route('/play', methods=['POST'])
def play():
    driver.execute_script("player.playVideo()")
    return ""

## Generate the server-side player page ##
@app.route('/player/<videoid>', methods=['GET'])
def player(videoid):
    return render_template('player.html', video_id=videoid)

@app.route('/player', methods=['GET'])
def player():
    return render_template('player.html', video_id=None)

@app.route('/getnextvideo', methods=['POST'])
def getnextvideo():
    vid = queue.get()
    queue.task_done()
    return vid

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
    #app.run(host='0.0.0.0', debug=True)

