import time
import forecastio
import database_sqlite as DB
soil = 300
wu_desc = 'Sunny'
watering = 'watering'
not_watering = 'no need water'

api_key = "77eb864c8ec94685a5834e714c840e03"
lat = DB.getLatitude()
lng = DB.getLongitude()

forecast = forecastio.load_forecast(api_key, lat, lng)

def decision():
    last_soil = int(DB.getlast_soil)
    treshold = 300
    if last_soil < treshold :
        watering
    else:
        not_watering

t0 = time.time()
print ("========================")
print ("time now		: " +time.strftime("%I %M %p",time.localtime(t0)))
print ("current soil		: "+ str(DB.getlast_soil))
print ("current weather		: "+ str(forecast.currently()))
print ("last rain		: "+ str(DB.getlast_rain()))
print ("command			: "+ decision())

t1 = t0 + 60*60
by_hour = forecast.hourly()
print ("========================")
print ("prediciton 1 hour ahead")
print ("time +1 		: " +time.strftime("%I %M %p",time.localtime(t1)))
print ("prediciton soil		: "+ str(soil))
print ("forecast weather	: %s " % (by_hour.summary))
print ("last rain		: "+ str(DB.getlast_rain()))
print ("command			: "+ decision())

t2 = t1 + 60*60
print ("========================")
print ("prediciton 2 hour ahead")
print ("time +2 		: " +time.strftime("%I %M %p",time.localtime(t2)))
print ("prediciton soil		: "+ str(soil))
print ("forecast weather	: %s " % (by_hour.summary))
print ("last rain		: "+ str(DB.getlast_rain()))
print ("command			: "+ decision())