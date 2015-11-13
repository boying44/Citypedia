import urllib2,json
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

weatherAPI = "7243b666b6841ed373ea8cd1289cc06d"

@app.route("/")
def home(city=""):
	url = """
http://api.openweathermap.org/data/2.5/weather?q=%s&units=Imperial&appid=%s
	"""
	url = url%(city, weatherAPI)
	request = urllib2.urlopen(url)
	result = request.read()
	r = json.loads(result)

	main = r["main"]
	info = []
	info.append("Current Temperature:" + str(main["temp"]))
	info.append("Min Temperature:" + str(main["temp_min"]))
	info.append("Max Temperature:" + str(main["temp_max"]))
	info.append("Humidity:" + str(main["humidity"]))
	return render_template("home.html", weather = info)

@app.route("/info", methods = ["GET", "POST"])
def info():
        if request.form.has_key("city") and request.form["city"] != "":
                city = request.form["city"]
                return render_template("info.html", city = city)
        else:
                return redirect("/")

if __name__ == "__main__":
   app.debug = True
   app.run(host="0.0.0.0", port=8000)
