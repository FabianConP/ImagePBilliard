from flask import Flask,jsonify,request
from main import Game

app = Flask(__name__)


# Create route for get suggestion from image
@app.route("/", methods = ["POST"])
def get_table():
    # Get image in base64 coding
    img_str = request.form.get("img_str")
    #print(img_str)
    # Create game from image
    game = Game(img_str)
    pos = game.get_balls_position()
    angles = game.get_angles()
    response = []
    for i in range(len(pos)):
        ball = pos[i]
        angle = angles[i]
        response.append({"x": ball[0], "y" : ball[1], "angle" : angle})
    print(response)
    return jsonify({"result":response})


if __name__ == '__main__':
    app.run(debug=True, host= '192.168.1.15')

'''
game = Game('')
'''