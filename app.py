from flask import Flask,jsonify,request,render_template,Response,flash,redirect,url_for

app = Flask(__name__)


@app.route('/')
def home():
	return render_template('index.html')

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html')

if __name__ == "__main__":
	app.run(host="0.0.0.0", debug=True)
	#app.run(host='0.0.0.0', port=80)