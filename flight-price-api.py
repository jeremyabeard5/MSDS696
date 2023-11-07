# flight-price-api.py
import requests
import time
import json
from json import JSONDecodeError


headers = {
	"X-RapidAPI-Key": "347c541513msh80c201a41e39ddep1dd960jsnf10b2afec703",
	"X-RapidAPI-Host": "sky-scrapper.p.rapidapi.com"
}

#################################

#print()
#print("try 1: checking server")

#url = "https://sky-scrapper.p.rapidapi.com/api/v1/checkServer"

#response = requests.get(url, headers=headers)
#try:
#   response_json = response.json()
#   print(json.dumps(response_json, indent=4))
#except JSONDecodeError:
#   print('Response could not be serialized')

##################################
# have program sleep for 5 seconds
#time.sleep(2)

#print()
#print("try 2: getting config") # this section only needs to run once, and then the config.json file can be used for future requests

#url = "https://sky-scrapper.p.rapidapi.com/api/v1/getConfig"

#response = requests.get(url, headers=headers)
#try:
#    response_json = response.json()
#    with open('config.json', 'w') as outfile:
#        json.dump(response_json, outfile, indent=4)
#    #print(json.dumps(response_json, indent=4))
#except JSONDecodeError:
#    print('Response could not be serialized')

##################################

#print()
#print("try 3: searching airports")
#time.sleep(2)   
    
#url = "https://sky-scrapper.p.rapidapi.com/api/v1/flights/searchAirport"

#querystring = {"query":"new"}

#response = requests.get(url, headers=headers, params=querystring)

#try:
#    response_json = response.json()
#    with open('airports.json', 'w') as outfile:
#        json.dump(response_json, outfile, indent=4)
#    #print(json.dumps(response_json, indent=4))
#except JSONDecodeError:
#    print('Response could not be serialized')


############################################

print()
print("try 4: getting nearby airports")
time.sleep(2)

url = "https://sky-scrapper.p.rapidapi.com/api/v1/flights/getNearByAirports"

querystring = {"lat":"39.7365633","lng":"-104.8236107"}

headers = {
	"X-RapidAPI-Key": "347c541513msh80c201a41e39ddep1dd960jsnf10b2afec703",
	"X-RapidAPI-Host": "sky-scrapper.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())

############################################

#print()
#print("try 4: searching for flights")
#time.sleep(2)

#url = "https://sky-scrapper.p.rapidapi.com/api/v1/flights/searchFlights"

#querystring = {"originSkyId":"LOND","destinationSkyId":"NYCA","originEntityId":"27544008","destinationEntityId":"27537542","date":"2024-02-20","adults":"1","currency":"USD","market":"en-US","countryCode":"US"}

#response = requests.get(url, headers=headers)
#try:
#   response_json = response.json()
#   print(json.dumps(response_json, indent=4))
#except JSONDecodeError:
#   print('Response could not be serialized')

##################################

#print()
#print("try 5: price calendar")
#time.sleep(2)

#url = "https://sky-scrapper.p.rapidapi.com/api/v1/flights/getPriceCalendar"

#querystring = {"originSkyId":"BOM","destinationSkyId":"JFK","fromDate":"2024-02-20"}

#response = requests.get(url, headers=headers)
#try:
#   response_json = response.json()
#   print(json.dumps(response_json, indent=4))
#except JSONDecodeError:
#   print('Response could not be serialized')

###################################

#url = "https://booking-com15.p.rapidapi.com/api/v1/flights/searchFlights"

#querystring = {"fromId":"DEN.AIRPORT","toId":"CVG.AIRPORT","departDate":"2023-12-18","returnDate":"2023-12-29","pageNo":"1","adults":"1","currency_code":"USD"}

#headers = {
#	"X-RapidAPI-Key": "347c541513msh80c201a41e39ddep1dd960jsnf10b2afec703",
#	"X-RapidAPI-Host": "booking-com15.p.rapidapi.com"
#}

#response = requests.get(url, headers=headers, params=querystring)

#try:
#    response_json = response.json()
#    print(json.dumps(response_json, indent=4))
#except JSONDecodeError:
#    print('Response could not be serialized')
    
####################################
#https://rapidapi.com/ntd119/api/booking-com13
url = "https://booking-com13.p.rapidapi.com/flights/one-way"

year = 2024
month = 9
day = 19
datecode = str(year) + '-' + str(month) + '-' + str(day)
departure_city = 'Denver, USA, Colorado'
arrival_city = 'Cincinnati, USA, Ohio'
querystring = {"location_from":departure_city,"location_to":arrival_city,"departure_date":datecode,"page":"1","country_flag":"us","number_of_stops":"NonstopFlights"}
#querystring = {"location_from":"Denver, USA, Colorado","location_to":"Cincinnati, USA, Ohio","departure_date":datecode,"page":"1","country_flag":"us","number_of_stops":"NonstopFlights"}
#querystring = {"location_from":"Denver, USA, Colorado","location_to":"Cincinnati, USA, Ohio","departure_date":"2023-12-19","page":"1","country_flag":"us","number_of_stops":"NonstopFlights"}

headers = {
	"X-RapidAPI-Key": "347c541513msh80c201a41e39ddep1dd960jsnf10b2afec703",
	"X-RapidAPI-Host": "booking-com13.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

#print(response.json())
filen = 'flights_' + datecode + '.json'
try:
    response_json = response.json()
    with open(filen, 'w') as outfile:
        json.dump(response_json, outfile, indent=4)
    #print(json.dumps(response_json, indent=4))
except JSONDecodeError:
    print('Response could not be serialized')
    
    
# Let's plan some...

# Assumptions:
#   - one adult
#   - one-way flight
#   - no checked bags

# User inputs:
#   - departure airport
#   - arrival airport
#   - departure date

# Database features:
#   - departure airport
#   - arrival airport
#   - departure date
#   - price
#   - airline
#   - flight duration
#   - departure time
#   - arrival time
#   - number of connections

# For each Booking.com13 output (shown example in flights.json), we want to keep:
# __typename: "Trip" > bounds > segments > arrivedAt, departuredAt, duration, flightNumber, destination>cityCode,cityName, marketingCarrier>code,name, operatingCarrier>code,name, origin>cityCode,cityName
# __typename: "Trip" > travelerPrices > price > price>currency>code > value
#   
#       
    
# I want to build a database/dataframe that has the features above for all flights from DEN-CVG from 2023-11-18 to 2024-09-19
# I want to test the following flights:
#    DEN-CVG
#    CVG-DEN

#    DEN-ORD
#    ORD-DEN

#    DEN-LAX
#    LAX-DEN

#    DEN-ATL
#    ATL-DEN

#    DEN-DFW
#    DFW-DEN

#    DEN-JFK
#    JFK-DEN

#    DEN-SFO
#    SFO-DEN

#    DEN-SEA
#    SEA-DEN

#    DEN-LAS
#    LAS-DEN

#    DEN-PHX
#    PHX-DEN

#    DEN-CLT
#    CLT-DEN

#    DEN-MCO
#    MCO-DEN

#    DEN-EWR
#    EWR-DEN

#    DEN-MSP
#    MSP-DEN

#    DEN-MIA
#    MIA-DEN

#    This should be 30 flight searches every day for 10 months~~300 days, so about 9000 flight searches. 
#    Each will return about 10 flights, so 90000 flights.
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    