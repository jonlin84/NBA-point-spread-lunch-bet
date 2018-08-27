from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
    
    return render_template('nbabet.html')

@app.route('/submit')
def submit():
    return '''
    <form action="/predict" method='POST'>
        <input type (GET BOTH TEAM COLUMNS AND SPREAD INPUT) ='input_data' />
    '''
    
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080, debug=True)