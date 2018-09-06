from flask import Flask, render_template, request, jsonify
import pickle
import re

from modelmaker import SpreadModel
sp = SpreadModel()

model = pickle.load(open("data/model.pkl", "rb"))

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('nbabet.html')


@app.route('/solve', methods=['POST'])
def solve():
    user_data = request.json
    home, away, spread = user_data['home'], user_data['away'],\
                    user_data['spread']
    prob = _predict_proba(home, away, spread)
    return jsonify({'Probability Home Team Wins': prob*100})


def _predict_proba(home, away, spread):
    train = sp.matchup_predict_data(home, away, spread)
    prob = model.predict_prob(train)[0] * 100
    return prob


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
