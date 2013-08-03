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

@app.route('/player/<videoid>', methods=['GET'])
def player(videoid):
    return render_template('player.html', video_id=videoid)

def enqueue(videoid):
    driver.get("http://localhost:5000/player/"+videoid)
    pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
    #app.run(host='0.0.0.0', debug=True)
