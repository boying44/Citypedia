import urllib2,json
from flask import Flask, render_template

app = Flask(__name__)

weatherAPI = 7243b666b6841ed373ea8cd1289cc06d

@app.route("/")
def home():
	# url = """
	# """
	# url = url%(tag)
	# request = urllib2.urlopen(url)
	# result = request.read()
	# r = json.loads(result)
	return render_template("home.html")

if __name__ == "__main__":
   app.debug = True
   app.run(host="0.0.0.0", port=8000)
