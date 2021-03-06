# rain_notifier.py
#
# This is a project that uses the Grove LED attached to an umbrella to remind 
# people to take their umbrella if it's raining or going to rain that day.
#
# You will need to modify the first few lines to make this project work for you.
# Fee free to modify the rest of the program to make it behave the way you want it to.
#
# Enter your zip code (or Postal Code) on the following line
# (leave the name 'zip' as is, even if you have a postal code. )
zip = 'YOUR_ZIP_CODE'

# once you have gotten an API Key from Wunderground (see tutorial), pleave provide it here
# Wunderground API Key
api_key = 'YOUR_WUNDERGROUND_API_KEY'

# if you wish to use two LEDs, provide the port number of the second LED
# The second LED is the one that will show there's no rain in the weather prediction
# With two LEDs, one will always be on. 
# if you do not want a second LED, set this to -1
clearled = 8

# in case of rain, do you want the LED to blink in order to catch your attention more?
# set to True for blinking, set to False for a steady warning
BLINK = True

############################################################################
# no modifications are required after this
# however the next few lines can be tweaked easily
############################################################################

# this is the delay between each polling of Wunderground. It's set to poll once every 5 minutes
# you may prefer a faster polling.
# the Wunderground free account does set a limit 

DELAY = 5*60 # in seconds

# Pin for the rain LED on the umbrella
rainled = 7

############################################################################
# nothing needs to be modified after this
# if you are familiar with Python, feel free to change anything to improve this
# we welcome additions and suggestions
############################################################################

import urllib2
import json
from grovepi import *
import time

def clear_led(status):
    """ change clear sky LED status """
    if clearled > -1:
        digitalWrite(clearled,status)

def assign_rain(status, blink):
    """ controls the LEDs status

    Arguments:
    status: True if it will be raining
            False if there's no rain in the forecast
    blink:  True if the rain led should blink when on
            False if the rain led does not need blinking
    no return value
    """
    if status == True: # there will be rain
        clear_led(0) # Turn off the CLEAR LED on the umbrella
        
        # Light the RAIN LED on the umbrella
        # check if it needs to be blinking
        if blink == True:
            led_blink() # no sleep required here
        else:
            digitalWrite(rainled,1)
            time.sleep(DELAY)

    else: # no rain in forecast
        # turn off the RAIN LED on the umbrella
        digitalWrite(rainled,0)
        # Turn on the CLEAR LED on the umbrella
        clear_led(1)
        time.sleep(DELAY)

def led_blink():
    """ forces the rain LED to blink

    rain LED will blink at a rate of 0.2 secs on, and 0.2 secs off
    it will blink for a duration set by DELAY
    no additional sleep() is required as it's incorporated in the blinking
    """
    count = 0.0
    blinkrate = 0.2
    while count < float(DELAY):
        digitalWrite(rainled,1)
        time.sleep(blinkrate)   
        digitalWrite(rainled,0)
        time.sleep(blinkrate)   
        count += (2*blinkrate)


#########################################################################

    
# Zip code of location
url='http://api.wunderground.com/api/'+api_key+'/geolookup/conditions/q/'+zip+'.json'

pinMode(rainled,"OUTPUT")
if clearled > -1:
    pinMode(clearled,"OUTPUT")

try:
    while True:
        f = urllib2.urlopen(url)
        json_string = f.read()
        f.close()
        parsed_json = json.loads(json_string)
        location = parsed_json['location']['city']
        precip_today_in = parsed_json['current_observation']['precip_today_in']

        print "Current precipitation in %s is: %s" % (location, precip_today_in)

        if float(precip_today_in) > 0 :
            print "Rain today, take the umbrella"
            assign_rain(True, BLINK)

        else:
            print "No Rain today"
            assign_rain(False, BLINK)



except KeyboardInterrupt:
    clear_led(0)
    digitalWrite(rainled,0)
