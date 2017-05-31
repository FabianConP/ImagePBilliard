from flask import Flask,jsonify,request
from main import Game

app = Flask(__name__)

# Create route for get suggestion from image
@app.route("/", methods = ["POST"])
def get_table():
    # Get image in base64 coding
    img_str = request.json['img_str']
    #print(img_str)
    # Create game from image
    game = Game(img_str)
    # Return for each ball a suggestion
    return jsonify({'img_str': game.get_angles()})


if __name__ == '__main__':
    app.run(debug=True, host= '192.168.1.15')

'''
game = Game('')
'''