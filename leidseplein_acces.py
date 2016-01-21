# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 15:33:41 2016

@author: Saxoriko

Analizing what people are tweeting when they go out(at night) in Amsterdam near het Leidseplein.
Because of the 100 tweets limit the result contains only 3 tweets.


"""


from twython import Twython, TwythonError
import json
import datetime 
import re

##codes to access twitter API. 
APP_KEY = 
APP_SECRET = 
OAUTH_TOKEN = 
OAUTH_TOKEN_SECRET = 

##initiating Twython object 
twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)


# write to file
output_file = 'result.csv' 
target = open(output_file, 'w')

# Defining leidseplein of Amsterdam with a range of 1 kilometer.
latitude = 52.362223	
longitude = 4.883747
max_range = 1 

geocode = "%f,%f,%dkm" % (latitude, longitude, max_range)


search_results = twitter.search(geocode=geocode, count=100)

total = 0
locations = 0
night = 0

for tweet in search_results["statuses"]: 
    total += 1
    # check if it has coordinates      
    if tweet['coordinates'] != None:
        locations += 1        
        coords = str(tweet['coordinates'])
        # using regex to get the coordinates out of the textstring
        expression = "\[(.*?)\]"
        regex = re.search(expression, coords)
        coordstring = regex.group(1)        
        #print coordstring
        
        date = str(tweet['created_at'])        
        # using regex to get the hour out of the date of the tweet        
        expression2 = "([0-9]{2})(?::[0-9]{2}:[0-9]{2})"
        regex2 = re.search(expression2, date)
        hour = int(regex2.group(1))
        
        # what was tweeted between 0 and 5am ?
        if hour < 5:
            night += 1            
            #print tweet['created_at']
            text = tweet['text']
            string = "%s, %s" % (coordstring, text)
            target.write(string)
            target.write('\n') #produce a tab delimited file
                
        
# some statistics        
print "total: %s" % total    
print "total locations: %s" % locations
print "total at night: %s" % night

target.close()


