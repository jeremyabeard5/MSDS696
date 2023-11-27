# flight-price-model.py

################################################
# This python script is designed to take the flight data from
# the sqlite3 database or .csv created in flight-price-api.py and create a model to predict the price
# of flights for any given day, airline and route.

# Thanks!
# Jeremy Beard
################################################

import timeit
start_time = timeit.default_timer()

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import os

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics

dpi = 300
data_dir = "data"
flights_dir = "flight-price-api"
file_path = os.path.join(data_dir, flights_dir)

def GetValues(str):
    print(f"Value counts for {str} column:")
    print(df[str].value_counts())
    print()
    

# start main function
if __name__ == "__main__":
    print("Starting flight-price-model.py")
    print()
    
    # read in data from database
    current_time = timeit.default_timer()
    print(f"Reading in data from database...")
    conn = sqlite3.connect(os.path.join(data_dir, flights_dir, "flights.db"))
    print(f"Time to connect to database: {timeit.default_timer() - current_time} seconds")
    print()
    
    # create dataframe from database
    current_time = timeit.default_timer()
    print(f"Creating dataframe from database...")
    df = pd.read_sql_query("SELECT * FROM flights", conn)
    print(f"Time to create dataframe from database: {timeit.default_timer() - current_time} seconds")
    
    # Create day_of_week column from datetime
    df['deptDateTime'] = pd.to_datetime(df['deptDateTime'])
    df['arrvDateTime'] = pd.to_datetime(df['arrvDateTime'])
    df['deptDayOfWeek'] = df['deptDateTime'].dt.day_of_week
    df['arrvDayOfWeek'] = df['arrvDateTime'].dt.day_of_week
    df['deptDate'] = df['deptDateTime'].dt.date
    df['arrvDate'] = df['arrvDateTime'].dt.date
    
    
    print()
    print("OG Dataframe info:")
    print(df.info())
    print()
    
    # We should have NO null values
    
    # Get value counts for marktName and marktCode columns
    GetValues('marktName')
    GetValues('marktCode')
    GetValues('optName')
    GetValues('optCode')
    GetValues('orgName')
    GetValues('orgCode')
    GetValues('destName')
    GetValues('destCode')
    GetValues('currency')
       
    # I saw that the only difference between MARKETING airline and OPERATING airline resided with American Airlines
    # So I will drop the optName and optCode columns
    # Drop unnecessary columns. We don't care about the codes, about the operating name
    df = df.drop(columns=['destCode', 'orgCode', 'optCode', 'marktCode', 'optName'])
    # If the currency value counts length is 1 (only USD), then drop the column
    if len(df['currency'].value_counts()) == 1:
        print()
        print("Only USD observed in currency column. Dropping column.")
        df = df.drop(columns=['currency'])
        print()
    
    print()
    print("NEW Dataframe info:")
    print(df.info())
    print()
    
    print("Dataframe head:")
    print(df.head())
    print()
    
    print("Dataframe tail:")
    print(df.tail())
    print()
    
    print("Dataframe describe:")
    print(df.describe())
    print()
    
    print("Dataframe shape:")
    print(df.shape)
    print()
    
    print("Dataframe columns:")
    print(df.columns)
    print()
    
    print("Few Columns of Interest: ")
    print(df.loc[:, ['orgName', 'destName', 'deptDateTime', 'price']])
    print()
    
    print("Creating first plot: Price vs. Date")
    fig0, ax0 = plt.subplots(figsize=(6,6))
    df.plot.scatter(x='deptDateTime', y='price', c='DarkBlue', ax=ax0)
    ax0.set(xlabel='datetime', ylabel='price', title='price by datetime')
    #df.plot.scatter(x='deptDateTime', y='price', c='DarkBlue')
    plt.tight_layout()
    plot0_filename = 'output/01_price-by-date_scatter.png'
    fig0.savefig(plot0_filename, dpi=dpi)
    
    
    # Now we enter the meat
    # I want to:
    # Explore the data
    # Plots I want to create
    #   - Price vs. Date
    #   - Price vs. Date, by airline
    #   - Price vs. Date, by route
    #   - Average Price vs. Day of Week
    #   - Average Price vs. Day of Week, by airline
    #   - Average Price vs. Day of Week, by route
    #   - Average Price vs. Month
    #   - Average Price vs. Month, by airline
    
    
    # Generate Linear Regression Model
    #df = 
    
    
    
    
    
    
    # ANALYSIS
    
    
    
    
    
    
    
    
    
    # close connection to database
    conn.commit()
    conn.close()
    
    # end program
    print(f"DONE! Time to run flight-price-model.py: {timeit.default_timer() - start_time} seconds")