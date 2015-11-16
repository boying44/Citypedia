import urllib2,json
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route("/")
def base():
	return render_template("base.html") 

@app.route("/explore", methods = ["GET", "POST"])
def explore():
        if request.form.has_key("city") and request.form["city"] != "":
                city = request.form["city"].title()
                wikiError = False
                weatherError = False
                imageError = False

                #Wikipedia Info
                url = "https://en.wikipedia.org/w/api.php?action=query&titles=%s&prop=extracts&exintro=&explaintext=&rvprop=content&format=json"
                url = url%(city.replace(" ", "%20"))
                req = urllib2.urlopen(url)
                result = req.read()
                r = json.loads(result)["query"]["pages"]
                wiki = []
                for i in r:
                        if r[i].has_key("extract") and r[i]["extract"] != "":
                                wiki.append(r[i]["extract"])
                        else:
                                wikiError = True
                                wiki = []
                
                #Weather data
                url = "http://api.openweathermap.org/data/2.5/weather?q=%s&units=Imperial&appid=7243b666b6841ed373ea8cd1289cc06d"
                url = url%(city.replace(" ", "%20"))
                req = urllib2.urlopen(url)
                result = req.read()
                r = json.loads(result)
                if r.has_key("main"):
                        main = r["main"]
                        weather = []
                        weather.append("Current Temperature: " + str(main["temp"]) + " Farenheit")
                        weather.append("Humidity: " + str(main["humidity"]))
                        weather.append("Weather: " + r["weather"][0]["main"])
                        weather.append("Cloudiness: " + str(r["clouds"]["all"]))
                        weather.append("Wind Speed: " + str(r["wind"]["speed"]))
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

                return render_template("explore.html", city = city, wikiError = wikiError, weatherError = weatherError, imageError = imageError, wiki = wiki, weather = weather, images = imageURLs)
        else:
                return redirect("/")

@app.route("/about")
def about():
        return render_template("about.html")

if __name__ == "__main__":
   app.debug = True
   app.run(host="0.0.0.0", port=8000)
