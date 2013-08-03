from flask import Flask
from flask import request
from flask import render_template
from selenium import webdriver
import Queue

# start the Flask listener
app = Flask(__name__)
queue = Queue.Queue()
driver = webdriver.Firefox()

@app.route('/', methods=['POST', 'GET'])
def jukebox():
    if request.method == 'POST':
        videoid = request.form['url']
        enqueue(videoid)

    return render_template('jukebox.html')

def enqueue(videoid):
    driver.get("player/"+videoid)
    pass

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



if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
    #app.run(host='0.0.0.0', debug=True)
