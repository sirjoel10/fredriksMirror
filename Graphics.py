import tkinter
import time
import locale
import requests
import json
import traceback

from PIL import Image
from PIL import ImageTk

# Text size
xlarge_text = 94
large_text = 50
medium_text = 28
small_text = 18

size = (100,100)

# Language set to swedish
locale.setlocale(locale.LC_TIME, "sv_SE")

# Weather inputs
weather_api_token = '564101d85f0c6c9e575f27590b44c094'
weather_lang = 'sv'
weather_unit = 'si'
latitude = '55.70584'
longitude = '13.19321'

# Icon look up !!! Astängd !!!
icon_lookup = {
    'clear-day':"assets/Sun.png",
    'wind':"assets/Wind.png",
    'cloudy':"assets/Cloud.png",
    'partly-cloudy-day':"assets/PartlySunny.png",
    'rain':"assets/Rain.png",
    'snow':"assets/Snow.png",
    'snow-thin':"assets/Snow.png",
    'fog':"assets/Haze.png",
    'clear-night':"assets/Moon.png",
    'partly-cloudy-night':"assets/PartlyMoon.png",
    'thunderstorm':"assets/Storm.png",
    'hail':"assets/Hail.png"
}


class clock(tkinter.Frame):

    def __init__(self,parent):
        tkinter.Frame.__init__(self, parent, bg='black')

        # Klockan funkar
        self.time1 = ''
        self.timeLbl = tkinter.Label(self, font=('Helvetica', xlarge_text, 'bold'), bg ='black', fg ='white')
        self.timeLbl.pack(side='top', anchor='e')

        # Dag
        self.day1 = ''
        self.dayLbl = tkinter.Label(self, font=('Helvetica', large_text, 'bold'), bg ='black', fg ='white')
        self.dayLbl.pack(side='top', anchor='e')

        # Datum
        self.date1 = ''
        self.dateLbl = tkinter.Label(self, font=('Helvetica', medium_text, 'bold'), bg ='black', fg ='white')
        self.dateLbl.pack(side='top', anchor='e')

        # Tick funktion
        self.tick()

    def tick(self):

        time2 = time.strftime('%H:%M')
        day2 = time.strftime('%A')
        date2 = time.strftime('%b %d, %y')

        if time2 != self.time1:
            self.time1 = time2
            self.timeLbl.config(text=time2)

        if day2 != self.day1:
            self.day1 = day2
            self.dayLbl.config(text=day2)

        if date2 != self.date1:
            self.date1 = date2
            self.dateLbl.config(text=date2)

        self.timeLbl.after(200, self.tick)


class weather(tkinter.Frame):

    def __init__(self, parent):

        tkinter.Frame.__init__(self, parent, bg='black')

        self.temperature = ''
        self.forecast = ''
        self.location = ''
        self.currently = ''
        self.icon = ''

        # Degree symbol
        self.degreeFrm = tkinter.Frame(self, bg="black")
        self.degreeFrm.pack(side='top', anchor='w')

        # Temperature
        self.temperatureLbl = tkinter.Label(self.degreeFrm, font=('Helvetica', xlarge_text), fg="white", bg="black")
        self.temperatureLbl.pack(side='left', anchor='n')

        # Display icon
        self.iconLbl = tkinter.Label(self.degreeFrm, bg="black")
        self.iconLbl.pack(side='left', anchor='n', padx=20)

        # Current weather
        self.currentlyLbl = tkinter.Label(self, font=('Helvetica', medium_text), fg="white", bg="black")
        self.currentlyLbl.pack(side='top', anchor='w')

        # Forecast
        self.forecastLbl = tkinter.Label(self, font=('Helvetica', small_text), fg="white", bg="black")
        self.forecastLbl.pack(side='top', anchor='w')

        # Location
        self.locationLbl = tkinter.Label(self, font=('Helvetica', small_text), fg="white", bg="black")
        self.locationLbl.pack(side='top', anchor='w')

        self.get_weather()

    def get_ip(self):
        try:
            ip_url = "http://jsonip.com/"
            req = requests.get(ip_url)
            ip_json = json.loads(req.text)
            return ip_json['ip']
        except Exception as e:
            traceback.print_exc()
            return "Error: %s. Cannot get ip." % e

    def get_weather(self):

        try:

            if latitude is None and longitude is None:
                # get location
                location_req_url = "http://freegeoip.net/json/%s" % self.get_ip()
                r = requests.get(location_req_url)
                location_obj = json.loads(r.text)

                lat = location_obj['latitude']
                lon = location_obj['longitude']

                location2 = "%s, %s" % (location_obj['city'], location_obj['region_code'])

                # get weather
                weather_req_url = "https://api.darksky.net/forecast/%s/%s,%s?lang=%s&units=%s" % (
                weather_api_token, lat, lon, weather_lang, weather_unit)

            else:
                location2 = ""
                # get weather
                weather_req_url = "https://api.darksky.net/forecast/%s/%s,%s?lang=%s&units=%s" % (weather_api_token, latitude, longitude, weather_lang, weather_unit)

            r = requests.get(weather_req_url)
            weather_obj = json.loads(r.text)

            degree_sign = u'\N{DEGREE SIGN}'
            temperature2 = "%s%s" % (str(int(weather_obj['currently']['temperature'])), degree_sign)
            currently2 = weather_obj['currently']['summary']
            forecast2 = weather_obj["hourly"]["summary"]


            icon_id = weather_obj['currently']['icon']
            icon2 = None

            if icon_id in icon_lookup:
                icon2 = icon_lookup[icon_id]

            if icon2 is not None:

                if self.icon != icon2:
                    self.icon = icon2
                    image = Image.open(icon2)
                    image.thumbnail(size, Image.ANTIALIAS)

                    '''
                    image = Image.resize((100, 100), Image.ANTIALIAS)
                    image = Image.convert('RGB')
                    '''
                    photo = ImageTk.PhotoImage(image)

                    self.iconLbl.config(image=photo)
                    self.iconLbl.image = photo
            else:
                # remove image
                self.iconLbl.config(image='')


            if self.currently != currently2:
                self.currently = currently2
                self.currentlyLbl.config(text=currently2)

            if self.forecast != forecast2:
                self.forecast = forecast2
                self.forecastLbl.config(text=forecast2)

            if self.temperature != temperature2:
                self.temperature = temperature2
                self.temperatureLbl.config(text=temperature2)

            if self.location != location2:

                if location2 == ", ":
                    self.location = "Cannot Pinpoint Location"
                    self.locationLbl.config(text="Cannot Pinpoint Location")
                else:
                    self.location = location2
                    self.locationLbl.config(text=location2)

        except Exception as e:
            traceback.print_exc()
            print ('Error: %s. Cannot get weather.') % e


        self.after(600000, self.get_weather)


class fullscreen:

    def __init__(self):

        # Skapar fönsteret
        self.window = tkinter.Tk()
        self.window.config(background='black')
        self.window.geometry('700x500')

        self.topframe = tkinter.Frame(self.window, background='black')
        self.bottomframe = tkinter.Frame(self.window, background='black')

        self.topframe.pack(side = 'top', fill = 'both', expand = 'YES')
        self.bottomframe.pack(side = 'bottom', fill='both', expand = 'YES')

        # Inför klockan till fönstret
        self.clock = clock(self.topframe)
        self.clock.pack(side='right', anchor='n', padx='100', pady = '60')

        # Inför vädret till fönstret
        self.weather = weather(self.topframe)
        self.weather.pack(side='left', anchor='n',padx='100', pady='60')


w = fullscreen()
w.window.mainloop()

