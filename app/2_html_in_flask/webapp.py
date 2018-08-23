from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    html = """
    <html lang="en">
    <head>
    <meta charset="utf-8">

    <title>NBA Spread Bet Preditor</title>
    <meta name="description" content="NBA Spread Bet Preditor">
    <meta name="author" content="Jonathan Lin">

    </head>

    <body>

        <h1>Which team should I bet on??</h1>
        <p>This app will give you the odds for each team with respect to the spread!</p>
        <p>Please select teams from the dropdown!</p>

    </body>
    </html>
    """
    return html

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)