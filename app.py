from flask import Flask, render_template, jsonify
import random

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# list of cat images
images = [
"https://bitbucket.org/mirantis-training/public/raw/master/gifs/cats/Cat-Combing-Itself.gif",
"https://bitbucket.org/mirantis-training/public/raw/master/gifs/cats/Cat-Hug.gif",
"https://bitbucket.org/mirantis-training/public/raw/master/gifs/cats/Cat-Playing-Basketball.gif",
"https://bitbucket.org/mirantis-training/public/raw/master/gifs/cats/Cat-Playing-Ping-Pong.gif",
"https://bitbucket.org/mirantis-training/public/raw/master/gifs/cats/Cat-Using-Chopsticks.gif",
"https://bitbucket.org/mirantis-training/public/raw/master/gifs/cats/Cat-Using-Computer.gif",
"https://bitbucket.org/mirantis-training/public/raw/master/gifs/cats/Cat-Wearing-Glasses.gif",
"https://bitbucket.org/mirantis-training/public/raw/master/gifs/cats/Cat-With-Beer.jpg",
"https://bitbucket.org/mirantis-training/public/raw/master/gifs/cats/Cat-With-Teddy-Bear.gif",
"https://bitbucket.org/mirantis-training/public/raw/master/gifs/cats/Cats-Sitting-Like-Human.gif",
"https://bitbucket.org/mirantis-training/public/raw/master/gifs/cats/Cats-Using-iPad.gif",
"https://bitbucket.org/mirantis-training/public/raw/master/gifs/cats/Cats-Wearing-Party-Hats.gif"
]

@app.route('/')
def index():
    url = random.choice(images)
    return render_template('index.html', url=url)

@app.route('/api')
def api():
    url = random.choice(images)
    return jsonify({"cat": url})

if __name__ == "__main__":
    app.run(host="0.0.0.0")
