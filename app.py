import urllib2,json
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

weatherAPI = "7243b666b6841ed373ea8cd1289cc06d"

@app.route("/")
def home():
	return render_template("base.html")

@app.route("/info", methods = ["GET", "POST"])
def info():
        if request.form.has_key("city") and request.form["city"] != "":
                city = request.form["city"]
                weatherError = False
                imageError = False

                #Wikipedia Info
                url = "https://en.wikipedia.org/w/api.php?action=query&titles=%s&prop=extracts&exintro=&explaintext=&rvprop=content&format=json"
                url = url%(city.replace(" ", "%20"))
                req = urllib2.urlopen(url)
                result = req.read()
                r = json.loads(result)
                if r.has_key("query"):
                        q = r["query"]
                        if q.has_key("pages"):
                                wiki = q["pages"]
                        else:
                                wikiError = True
                                wiki = []
                else:
                        wikiError = True
                        wiki = []

                
                #Weather data
                url = "http://api.openweathermap.org/data/2.5/weather?q=%s&units=Imperial&appid=%s"
                url = url%(city.replace(" ", "%20"), weatherAPI)
                req = urllib2.urlopen(url)
                result = req.read()
                r = json.loads(result)
                if r.has_key("main"):
                        main = r["main"]
                        weather = []
                        weather.append("Current Temperature:" + str(main["temp"]))
                        weather.append("Min Temperature:" + str(main["temp_min"]))
                        weather.append("Max Temperature:" + str(main["temp_max"]))
                        weather.append("Humidity:" + str(main["humidity"]))
                else:
                        weatherError = True
                        weather = []
                
                #Google Images
                url = "https://ajax.googleapis.com/ajax/services/search/images?v=1.0&q=%s"
                url = url%(city.replace(" ", "%20"))
                req = urllib2.urlopen(url)
                result = req.read()
                r = json.loads(result)
                images = r["responseData"]["results"]
                if len(images) > 0:
                        imageURLs = []
                        for i in range(0, 3):
                                if len(images) > i:
                                        imageURLs.append(images[i]["unescapedUrl"])
                else:
                        imageError = True
                        imageURLs = []

                return render_template("info.html", city = city, wiki=wiki, weatherError = weatherError, imageError = imageError, weather = weather, images = imageURLs)
        else:
                return redirect("/")

if __name__ == "__main__":
   app.debug = True
   app.run(host="0.0.0.0", port=8000)
