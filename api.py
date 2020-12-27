from flask import Flask, request, render_template,jsonify
import bookrec

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/recommend', methods=['GET','POST'])
def do_something():
   
    input_feature = request.form['myBook']
    return render_template('home.html', output = bookrec.combine(input_feature))

if __name__ == '__main__':
    app.run(debug=True)




