from flask import Flask,jsonify,request
from main import Game
'''
app = Flask(__name__)


@app.route("/", methods = ["POST"])
def get_table():
    img_str = request.json['img_str']
    #print(img_str)
    game = Game(img_str)
    return jsonify({'img_str': game.get_angles()})


if __name__ == '__main__':
    app.run(debug=True)
'''

game = Game('')