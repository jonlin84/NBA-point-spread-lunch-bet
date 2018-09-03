from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
    
    return render_template('nbabet.html')

@app.route('/solve', methods=['POST'])
def solve():
    user_data = request.json
    home_team, away_team, spread = user_data['team1'], user_data['team2'], user_data['spread']
    cover = _predict_proba(home_team, away_team, spread)
    return jsonify({'Chance Home Team Covers!': cover)  

    
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080, debug=True)