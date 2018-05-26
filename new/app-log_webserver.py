from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import time, datetime
import io
import math
import Adafruit_DHT
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import hisab as hisab
import database as DB
import openweather as openweather
import wunderground as wunderground
import input_data as IN

from flask import Flask, render_template, send_file, make_response, request
app = Flask(__name__)

import sqlite3
conn=sqlite3.connect('/kufarm.db')
curs=conn.cursor()

sampleFreq = 1*60 # time in seconds ==> Sample each 1 min
requestStatus = False;

#initialize global variables
global numSamples
numSamples = DB.maxRowsTable()
if (numSamples > 101):
	numSamples = 100

global freqSamples
freqSamples = DB.freqSample()

global rangeTime
rangeTime = 100	

# main route 
@app.route("/")
def index():
	time, temp, hum, soil, rain = DB.getLastData()
	templateData = {
	  'time'		: time,
	  'temp'		: temp,
	  'hum'			: hum,
	  'soil'		: soil,
	  'rain'		: rain,
	  'freq'		: freqSamples,
	  'rangeTime'	: rangeTime
	  #'numSamples'	: numSamples
	}
	return render_template('index_copy3.html', **templateData)


@app.route('/', methods=['POST'])
def my_form_post():
	global numSamples 
	global freqSamples
	global rangeTime
	rangeTime = int (request.form['rangeTime'])
	if (rangeTime < freqSamples):
		rangeTime = freqSamples + 1
	numSamples = rangeTime//freqSamples
	numMaxSamples = DB.maxRowsTable()
	if (numSamples > numMaxSamples):
		numSamples = (numMaxSamples-1)
	time, temp, hum, soil, rain = DB.getLastData()
	
	templateData = {
	  'time'		: time,
	  'temp'		: temp,
	  'hum'			: hum,
	  'soil'		: soil,
	  'rain'		: rain,
	  'freq'		: freqSamples,
	  'rangeTime'	: rangeTime
	  #'numSamples'	: numSamples
	}
	return render_template('index_copy3.html', **templateData)
	
#plot temp	
@app.route('/plot/temp')
def plot_temp():
	times, temps, hums, soils, rains = DB.getHistData(numSamples)
	ys = temps
	fig = Figure()
	axis = fig.add_subplot(1, 1, 1)
	axis.set_title("Temperature [C]")
	axis.set_xlabel("Samples")
	axis.grid(True)
	xs = range(numSamples)
	axis.plot(xs, ys)
	canvas = FigureCanvas(fig)
	output = io.BytesIO()
	canvas.print_png(output)
	response = make_response(output.getvalue())
	response.mimetype = 'image/png'
	return response

#plot hum
@app.route('/plot/hum')
def plot_hum():
	times, temps, hums, soils, rains = DB.getHistData(numSamples)
	ys = hums
	fig = Figure()
	axis = fig.add_subplot(1, 1, 1)
	axis.set_title("Humidity [%]")
	axis.set_xlabel("Samples")
	axis.grid(True)
	xs = range(numSamples)
	axis.plot(xs, ys)
	canvas = FigureCanvas(fig)
	output = io.BytesIO()
	canvas.print_png(output)
	response = make_response(output.getvalue())
	response.mimetype = 'image/png'
	return response

#plot soil
@app.route('/plot/soil')
def plot_soil():
	times, temps, hums, soils, rains = DB.getHistData(numSamples)
	ys = soils
	fig = Figure()
	axis = fig.add_subplot(1, 1, 1)
	axis.set_title("Soil Condition")
	axis.set_xlabel("Samples")
	axis.grid(True)
	xs = range(numSamples)
	axis.plot(xs, ys)
	canvas = FigureCanvas(fig)
	output = io.BytesIO()
	canvas.print_png(output)
	response = make_response(output.getvalue())
	response.mimetype = 'image/png'
	return response

#plot rain
@app.route('/plot/rain')
def plot_rain():
	times, temps, hums, soils, rains = DB.getHistData(numSamples)
	ys = rains
	fig = Figure()
	axis = fig.add_subplot(1, 1, 1)
	axis.set_title("Rain Intensity")
	axis.set_xlabel("Samples")
	axis.grid(True)
	xs = range(numSamples)
	axis.plot(xs, ys)
	canvas = FigureCanvas(fig)
	output = io.BytesIO()
	canvas.print_png(output)
	response = make_response(output.getvalue())
	response.mimetype = 'image/png'
	return response

if __name__ == "__main__":
	# ------------ Execute program 
	app.run(host='0.0.0.0', port=8080, debug=False)

