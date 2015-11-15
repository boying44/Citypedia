import urllib2,json
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

weatherAPI = "7243b666b6841ed373ea8cd1289cc06d"

@app.route("/")
def home():
	return render_template("home.html")

@app.route("/info", methods = ["GET", "POST"])
def info():
        if request.form.has_key("city") and request.form["city"] != "":
                city = request.form["city"]

                #Weather data
                url = "http://api.openweathermap.org/data/2.5/weather?q=%s&units=Imperial&appid=%s"
                url = url%(city.replace(" ", "%20"), weatherAPI)
                req = urllib2.urlopen(url)
                result = req.read()
                r = json.loads(result)
                main = r["main"]
                weather = []
                weather.append("Current Temperature:" + str(main["temp"]))
                weather.append("Min Temperature:" + str(main["temp_min"]))
                weather.append("Max Temperature:" + str(main["temp_max"]))
                weather.append("Humidity:" + str(main["humidity"]))
                
                return render_template("info.html", city = city, weather = weather)
        else:
                return redirect("/")

if __name__ == "__main__":
   app.debug = True
   app.run(host="0.0.0.0", port=8000)
