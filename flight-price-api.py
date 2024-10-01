# flight-price-api.py
################################################
# This python script is designed to pull flight data from the Booking.com13 API
# Once pulled via raw JSON, the data is parsed and put into an sqlite database
# The database can be added to over time and can be used to model flight prices

# Thanks!
# Jeremy Beard
################################################

import timeit
start_time = timeit.default_timer()
import requests
import time
from datetime import datetime, timedelta
import json
from json import JSONDecodeError
import sqlite3
from itertools import combinations
import pandas as pd
import sys

class Logger(object):
   def __init__(self):
       self.terminal = sys.stdout
       self.log = open("console.log", "a")

   def write(self, message):
       self.terminal.write(message)
       self.log.write(message) 

   def flush(self):
       # this flush method is needed for python 3 compatibility.
       # this handles the flush command by both writing and flushing the file.
       self.terminal.flush()
       self.log.flush()

headers = {
	"X-RapidAPI-Key": os.getenv('RAPIDAPI_KEY'),
	"X-RapidAPI-Host": os.getenv('RAPIDAPI_HOST')
}

####################################

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
#   - url
    
# I want to build a database/dataframe that has the features above for all flights from DEN-CVG from 2023-11-18 to 2024-09-19
# I want to test the following flights to/from Denver:
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
    
def get_flights(origin_location, destination_location, date):
    # This function is designed to take a pair of locations and a date, and return the JSON data from the Booking.com13 API
    print(f'Getting flights from {origin_location} to {destination_location} on {date}, TIME: {timeit.default_timer() - start_time}')
    # instantiate flights variable with empty string
    flights = ''
       
    url = "https://booking-com13.p.rapidapi.com/flights/one-way"

    year = 2024
    month = 9
    day = 19
    datecode = date
    origin_city = origin_location #'Denver, USA, Colorado'
    destination_city = destination_location #'Cincinnati, USA, Ohio'
    querystring = {"location_from":origin_city,"location_to":destination_city,"departure_date":datecode,"page":"1","country_flag":"us","number_of_stops":"NonstopFlights"}
    #querystring = {"location_from":"Denver, USA, Colorado","location_to":"Cincinnati, USA, Ohio","departure_date":datecode,"page":"1","country_flag":"us","number_of_stops":"NonstopFlights"}
    #querystring = {"location_from":"Denver, USA, Colorado","location_to":"Cincinnati, USA, Ohio","departure_date":"2023-12-19","page":"1","country_flag":"us","number_of_stops":"NonstopFlights"}

    headers = {
        "X-RapidAPI-Key": os.getenv('RAPIDAPI_KEY'),
        "X-RapidAPI-Host": os.getenv('RAPIDAPI_HOST')
    }

    response = requests.get(url, headers=headers, params=querystring)

    #print(response.json())
    filen = 'flights_' + datecode + '.json'
    try:
        response_json = response.json()
        #with open(filen, 'w') as outfile:
        #    json.dump(response_json, outfile, indent=4)
        flights = json.dumps(response_json, indent=4)
    except JSONDecodeError:
        print('Response could not be serialized')
    
    print(f'Got flights from {origin_location} to {destination_location} on {date}')
    return json.loads(flights)

def process_flights(flights, cu, d8):
    # this function takes the raw JSON data from the Booking.com13 API and parses it into a sqlite database
    # It checks for duplicates before adding to the database
    # It also checks for direct flights vs. indirect flights
    print(f'Processing flights for {d8}')
    tmp_flights_added = 0

    if 'data' in flights and flights['data'] is not None and 'flights' in flights['data']:
        print(f"Flights exist")
    else:
        print(f"NO FLIGHTS FOR {d8}")
        return

    for result in flights['data']['flights']:
        print()
        segLen = len(result['bounds'][0]['segments'])
        if segLen > 1:
            print(f"INDIRECT: more than one segment, found {segLen}")
            totalDuration = 0
            for seg in result['bounds'][0]['segments']:
                id = seg['segmentId']
                # take seg['duration'], cast to int, divide by 1000, add to totalDuration
                totalDuration += round(seg['duration'] / 1000 / 60)
                if id == '00' or id == '01' or id == '02' or id == '03' or id == '04':
                    print(f"segment: {seg['origin']['cityCode']} to {seg['destination']['cityCode']}")
                else:
                    print(f"layover found with duration {round(seg['duration']/1000/60)} minutes")
            #   - destination airport
            destCode = result['bounds'][0]['segments'][-1]['destination']['cityCode']
            destName = result['bounds'][0]['segments'][-1]['destination']['cityName']
            #   - origin airport
            orgCode = result['bounds'][0]['segments'][0]['origin']['cityCode']
            orgName = result['bounds'][0]['segments'][0]['origin']['cityName']
            #   - departure date and time
            deptDateTime = result['bounds'][0]['segments'][0]['departuredAt']
            #   - arrival date and time
            arrvDateTime = result['bounds'][0]['segments'][-1]['arrivedAt']
            #   - price
            price = round(result['travelerPrices'][0]['price']['price']['value']/100, 2)
            #   - currency
            currency = result['travelerPrices'][0]['price']['price']['currency']['code']
            #   - airline
            marktName = result['bounds'][0]['segments'][0]['marketingCarrier']['name']
            marktCode = result['bounds'][0]['segments'][0]['marketingCarrier']['code']
            optName = result['bounds'][0]['segments'][0]['operatingCarrier']['name']
            optCode = result['bounds'][0]['segments'][0]['operatingCarrier']['code']
            #   - flight number
            flightNum = result['bounds'][0]['segments'][0]['flightNumber']
            #   - flight duration
            duration = totalDuration #result['bounds'][0]['segments'][0]['duration']
            #   - number of connections
            numConex = len(result['bounds'][0]['segments'])
            #   - url
            url = result['shareableUrl']
            
            print(f'INDIRECT FLIGHT: {orgCode} to {destCode} on {deptDateTime} for {price} {currency} on {marktName} flight {flightNum} ({duration} minutes)')
            print(url)
        else: # direct flight
            #   - destination airport
            destCode = result['bounds'][0]['segments'][0]['destination']['cityCode']
            destName = result['bounds'][0]['segments'][0]['destination']['cityName']
            #   - origin airport
            orgCode = result['bounds'][0]['segments'][0]['origin']['cityCode']
            orgName = result['bounds'][0]['segments'][0]['origin']['cityName']
            #   - departure date and time
            deptDateTime = result['bounds'][0]['segments'][0]['departuredAt']
            #   - arrival date and time
            arrvDateTime = result['bounds'][0]['segments'][0]['arrivedAt']
            #   - price
            price = round(result['travelerPrices'][0]['price']['price']['value']/100, 2)
            #   - currency
            currency = result['travelerPrices'][0]['price']['price']['currency']['code']
            #   - airline
            marktName = result['bounds'][0]['segments'][0]['marketingCarrier']['name']
            marktCode = result['bounds'][0]['segments'][0]['marketingCarrier']['code']
            optName = result['bounds'][0]['segments'][0]['operatingCarrier']['name']
            optCode = result['bounds'][0]['segments'][0]['operatingCarrier']['code']
            #   - flight number
            flightNum = result['bounds'][0]['segments'][0]['flightNumber']
            #   - flight duration
            duration = round(result['bounds'][0]['segments'][0]['duration'] / 1000 / 60)
            #   - number of connections
            numConex = len(result['bounds'][0]['segments'])
            #   - url
            url = result['shareableUrl']
            
            print(f'DIRECT FLIGHT: {orgCode} to {destCode} on {deptDateTime} for {price} {currency} on {marktName} flight {flightNum} ({duration} minutes)')
            print(url)
        # Now we have all the data we want for this flight, let's put it into the sqlite database
        # First we'll check for duplicates
        cu.execute("SELECT * FROM flights WHERE destCode=? AND destName=? AND orgCode=? AND orgName=? AND deptDateTime=? AND arrvDateTime=? AND currency=? AND marktName=? AND marktCode=? AND optName=? AND optCode=? AND flightNum=? AND duration=? AND numConex=? AND url=?", 
                   (destCode, destName, orgCode, orgName, deptDateTime, arrvDateTime, currency, marktName, marktCode, optName, optCode, flightNum, duration, numConex, url))
        result = cu.fetchone()
        if result is not None: # is duplicate
            print("Duplicate entry found, will skip")
        else: # is not duplicate, let's enter into database
            print("No duplicate entry found")
            cu.execute("INSERT INTO flights VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", 
                    (destCode, destName, orgCode, orgName, deptDateTime, arrvDateTime, 
                    price, currency, marktName, marktCode, optName, optCode, flightNum, 
                    duration, numConex, url))
            tmp_flights_added += 1
            
    print(f'Done processing flights for {d8}, ADDED {tmp_flights_added} FLIGHTS')
    return tmp_flights_added
    
def find_pairs(location_list):
    # this function takes a list of locations and returns all possible pairs, including B-A and A-B
    pairs = []
    locations_reversed = location_list[::-1]
    pairs = list(combinations(location_list, 2))
    reversed_pairs = list(combinations(locations_reversed, 2))
    pairs.extend(reversed_pairs)
    return pairs

def prune_pairs(location_pairs, prune_string):
    # this function takes a list of location pairs and removes any pairs that don't list DEN as either origin/destination
    pruned_pairs = []
    for pair in location_pairs:
        if prune_string in pair:
            pruned_pairs.append(pair)     
    return pruned_pairs   
    
# start main python function
if __name__ == "__main__":
    sys.stdout = Logger()
    print("Hello World!")
    print("I'm Mr. Meeseeks, look at me!")
    print(f'Program started at {datetime.now()}')
    print(f'TIME: {timeit.default_timer() - start_time}')
    
    # I will start small, DEN-CVG, 2023-12-19
    # using https://rapidapi.com/ntd119/api/booking-com13
    
    # Lets start by creating the empty database
    conn = sqlite3.connect('flights.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS flights
              (destCode text, destName text, orgCode text, orgName text, deptDateTime text, 
              arrvDateTime text, price real, currency text, marktName text, marktCode text, 
              optName text, optCode text, flightNum text, duration real, numConex integer, url text)
              ''')
    
    # Now let's set the locations we want to search
    #locations = ['Denver, USA, Colorado', 'Cincinnati, USA, Ohio', 'Chicago, USA, Illinois', 
    #             'Los Angeles, USA, California', 'Atlanta, USA, Georgia', 'Dallas, USA, Texas', 
    #             'New York, USA, New York', 'San Francisco, USA, California', 
    #             'Seattle, USA, Washington', 'Las Vegas, USA, Nevada', 'Phoenix, USA, Arizona', 
    #             'Charlotte, USA, North Carolina', 'Orlando, USA, Florida', 
    #             'Newark, USA, New Jersey', 'Minneapolis, USA, Minnesota', 'Miami, USA, Florida']
    locations = ['Denver, USA, Colorado', 'Cincinnati, USA, Ohio', 'Chicago, USA, Illinois',
                 'Los Angeles, USA, California', 'New York, USA, New York', 'San Francisco, USA, California', 
                 'Las Vegas, USA, Nevada', 'Orlando, USA, Florida', 'Buffalo, USA, New York', 'Miami, USA, Florida']                 
    location_pairs = find_pairs(locations)
    denver_pairs = prune_pairs(location_pairs, 'Denver, USA, Colorado')
    len_pairs = len(denver_pairs)
    i_done = 1
    pct_done = 0
    flights_added = 0
    # we'll use the datetime package to iterate through the dates
    start_date = datetime.strptime('2023-11-20', '%Y-%m-%d')
    end_date = datetime.strptime('2024-10-10', '%Y-%m-%d')
    total_days = (end_date - start_date).days+1
    total_queries = total_days * len_pairs
    total_flights = total_queries * 10
    
    
    for pair in denver_pairs: # iterate through all locations/routes
        location_a = pair[0]
        location_b = pair[1]
        pair_time = timeit.default_timer()
        print(f'Getting flights from {location_a} to {location_b}, TIME: {timeit.default_timer() - start_time}')
        
        current_date = start_date
        
        while current_date <= end_date: # iterate through all dates
            days_elapsed = (current_date - start_date).days
            #temp = get_flights('Denver, USA, Colorado', 'Cincinnati, USA, Ohio', 2023-12-19)
            temp = get_flights(location_a, location_b, current_date.strftime('%Y-%m-%d'))
            # temp is 10 flights worth of JSON data! 
            # But we still have to parse everything     
            # and put it into a sqlite database
            
            # Now we'll extract the data
            #process_flights(temp, c, '2023-12-19')
            process_flights(temp, c, current_date.strftime('%Y-%m-%d'))
            current_date += timedelta(days=1)
            
            # Now we'll print out the progress
            pct_done = round(i_done / total_queries * 100, 2)
            time_elapsed = timeit.default_timer() - start_time
            remain = round((100-pct_done)*time_elapsed/pct_done/60, 2)
            print(f'Progress: {i_done} of {total_queries} queries completed ({pct_done}%), TIME: {time_elapsed}, ESTIMATED TIME REMAINING: {remain} minutes ({remain*60} seconds)')
            i_done += 1
    
        print()
        print(f'It took {timeit.default_timer() - pair_time} seconds to get flights from {location_a} to {location_b} for all dates')
        # Now we'll print out the progress
        pct_done = round(i_done / total_queries * 100, 2)
        time_elapsed = timeit.default_timer() - start_time
        remain = round((100-pct_done)*time_elapsed/pct_done/60, 2)
        print(f'Progress: {i_done} of {total_queries} queries completed ({pct_done}%), TIME: {time_elapsed}, ESTIMATED TIME REMAINING: {remain} minutes ({remain*60} seconds)')
        print()
        
    # DONE! FINALLY!
    print('Outputting final database...')
    df = pd.read_sql_query('SELECT * FROM flights', conn)
    
    df.to_csv('flights.csv', index=False)
    
    
    conn.commit()
    conn.close()
    
    print()
    print(f"Done with the world! Program took {timeit.default_timer() - start_time} seconds to run")
    
    
    
    
    # Thanks!
    # Jeremy Beard
    # MSDS 696
    
    
    
    