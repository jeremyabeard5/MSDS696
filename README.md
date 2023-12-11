# MSDS696

![Sample Image](output/06-tableau-dashboard.png)

# MSDS696: Final Capstone

**Machine Learning in the Clouds**

by

Jeremy Beard

# Table of Contents

[Youtube Presentation](#youtube)

[Main Ideas](#mainideas)

[Problem Statement](#problemstatement)

[Introduction](#intro)

[Methods](#methods)

[EDA](#eda)

[Results](#results)

[Conclusions](#conclusions)

[Future Work](#future)

[References](#references)


<a name="youtube"/>

# Youtube Presentation 

https://youtu.be/sUgiseRjJC0

<a name="mainideas"/>

# Main Ideas

This project is centered around an effort to scrape real-time flights and utilize it for a price prediction model. An Application Programming Interface (API) was utilized (see references below) in order to obtain ~45,000 real flights, primarily from United, American, and Frontier Airlines. 

Following the web-scraping of this project, I created a wide array of Machine Learning (ML) models to compare and be able to reliably predict (within $22) what price a flight will be. 

Many more details will be shared, so let's continue    :) 

<a name="problemstatement"/>

# Problem Statement

The main problem we were seeking to solve is:

"How can we reliably predict trends with flight prices in order to leverage the best days, times, and airlines on which to travel?" 

Another angle of my problem statement is:

"How can we reliably predict trends and prices for air travel based on common real-life
inputs to leverage the same ML tactics corporations are utilizing, but on consumer-side?"

<a name="intro"/>

# Introduction

Obviously there are websites which exist today that serve to find consumers the cheapest flights for a specific time period and destination, but these websites are often slow and filled with advertisements and depend on an internet connection. I had a need for creating Denver-based flight prediction models for myself and others that could go beyond what is already offered. The model shown in this repository, while being built upon a dataset which relies on an internet connection, can act independently of an internet connection and is without advertisements.  

The tool built seeks to serve as an initial check into which days and which airlines should be noted as typically the cheaper options for a specific route and specific day. Using this tool, the user can view trends in flight prices and can input a specific route to view what the predicted price will be on that day. 

The challenge is to implement a web-scraping solution that extracts relevant data, including departure details, flight duration, layovers, class types, and current/historical pricing information, from a relevant online source (or sources). Following that, the goal is to create an ACCURATE machine learning model. 

The solution I created will empower stakeholders with valuable insights for informed decision-making in the airline industry!

<a name="methods"/>

# Methods

This project involves five (5) main efforts for predicting these flight prices. The overall process though is pretty simple and is as follows:

* Figure out a way to scrape real flights from the internet to create a large database with which to create a model.

* Perform exploratory data analytics on the flight database, ensuring data is clean prepared for model analytics.

* Create Tableau dashboards to see at-a-glance which days, weeks, months, and airlines are cheapest for flying.

* Take data from the flight database and do comparative analysis on different ML models in order to create the most accurate model for predicting flight prices.

* Choose the most accurate model and validate the accuracy!

Within the machine learning aspect of the project, there were really two (2) main focuses: comparative analytics among ML models, as well as time-based analysis and determining the best way to handle time-series data. 

I was new to handling time-series data and didn't know which method would be the best and most accurate in handling this data within a machine learning context. I chose 3-5 formats for the datetimes in the dataset, including ordinal datetimes as well as utilizing the time.mktime() package to create floating-point datetime fields. 

Once we scrape all the flights we need and perform the comparative analysis, we will have a machine learning model that is Denver-focused and can help to quickly assist the user in selecting a flight which is satisfactory to them! 

### Which Models?

To be able to compare a large amount of machine learning models across numerous variations of datetime formats, I utilized the pycaret package which can perform analysis on many machine learning models within a single context or command. This helps to simplify the process greatly, especially when I have many different date formats I wanted to compare as well. 

<a name="eda"/>

# EDA

During the Exploratory Data Analysis (EDA) section of the project, I created many charts, some of which were new to me. Calendar plots using the calplot and july packages in Python were useful in visualizing the entire year's worth of data at a glance. I'll include these charts below.

The reader can also see average price by hour, average price by day of week, average price by month, and more. 

![Calplot](output/07-calendar-01.png)

Spring Break is going to be an expensive time of year, looks like! Sundays are consistently expensive.

![Price by Datetiime](output/00-price-by-datetime-scatter.png)

Generic scatterplot of the data. That one Thanksgiving Denver-New York flight is waaaaay up there!

![Avg Price by Day of Year](output/03-avg-price-by-doy.png)

You can see that there is a big gap in the data from late October to early November. This is because I began scraping when it was early November 2023, so I didn't have access to some of the November data. As well, the October 2024 data started to be exorbitantly expensive, maybe because it was so far away. So I excluded most of the October 2024 data. 

![Avg Price by Day of Week](output/01-avg-price-by-dow.png)

Tuesdays and Wednesdays look like good days to fly!

![Avg Price by Month](output/02-avg-price-by-month.png)

January and February are looking pretty cheap as welL!

![Avg Price by Hour](output/04-avg-price-by-hour.png)

Not a whole lot to glean here in my opinion, except for the fact that the API, when queried for Denver-specific flights, didn't seem to have any flights which departed in the hours of 2am, 3am, or 4am. This is strange but maybe it's a trend that I'm not aware of for these specific flight paths or this specific API. 

<a name="results"/>

# Results

The pycaret package was able to generate a lot of different machine learning models in a short amount of time! These models were tweaked over time but gave a good foundation with which to start.

I explored two (2) dimensions in the machine learning context: different pycaret generators, and different date formats.

The two (2) pycaret generators I used were:

* KFolds Generator (default)

* Timeseries Generator

The different datetime formats I used were:

* Parsed Datetimes: parsing the datetime into separate Year/Month/Day/Hour numeric fields.

* Ordinal Datetimes: ordinal datetimes are an integer value which integrates Year/Month/Day. This value does not account for time of day so I included the Hour field as a separate field in these cases.

* time.mktime() Datetimes: the time.mktime() package creates a floating-point value which integrates Year/Month/Day/Hour. This seemed like the best method at first glance, although the results may show differently. 

* datetime: Just using the standard input datetime located in the data. This was only used for the timeseries pycaret models.

* date + separate hour field: Just taking the date from the datetime and formatting it as its own datetime, then including the hour as a separate field. This was also only used for the timeseries pycaret models. 

These two (2) dimensions of pycaret generator and datetime format gave me many combinations to work with. Overall, I had 8 datetime formats submitted to pycaret, 3 for the KFolds Generator and 5 for the Timeseries Generator. I also included one Linear Regression model that wasn't created with pycaret, but included as a baseline. 

The results of all these models are below:

![Model Output](output/05-error-by-model.png)

It appears that the Ordinal date won out! Interestingly enough, the pycaret Timeseries Generator didn't perform as well as the KFolds Generator. This was curious to me. Nevertheless, it appears that the best Mean Absolute Error (MAE) that the models achieved was 22.05. This means that the lowest average difference between the predictions and true flight prices was $22.05 using the Ordinal datetime and the KFolds Generator. The R-squared value is not shown in this chart but the corresponding R-squared value of this model was 0.83. Not bad!

# Conclusions

I reached a handful of conclusions throughout the course of this project, among a variety of contexts. Firstly, the main conclusion gleaned was that using the Booking.com API and the pycaret KFolds Generator, Random Forest Model, using Ordinal datetime and a separate Hour field, achieved a 22.05 MAE. 

Another conclusion gained is that there needs to be some regular scheduling of this flight data in order to reduce bias. November prices were shown as extremely high and while this may be true, it may also just be high because the flight data was scraped in early November, when Thanksgiving flight prices are extremely high. 

An additional conclusion gleaned was that the best models from the pycaret package tended to be the Random Forest model and the Extra Trees Regressor model. This was pretty consistent among all the different datetime formats submitted.

A final conclusion is that there is still more to be done with the Timeseries Generator in pycaret! I wasn't satisfied with the performance of the Timeseries Generator in pycaret and I'd like to still spend more time with it. 

<a name="future"/>

# Future Work

This project was a huge learning experience for me and I really enjoyed every aspect of it. I learned a lot about handling time-based data within a machine learning context and how it can perform the best. I also learned a lot about different visualization types like the calendar plots and Tableau dashboards. 

Some future work I have in mind so far is:

* More data! I only have 45,000 flights among a handful of airports and overall it's less than a year's worth of data. I'd like to continue adding to this sqlite3 database!

* Implement more feature engineering! There weren't a ton of features that I thought were useful (I didn't think many features from the API would correlate with flight price). The main features were datetime, origin location, destination location, and airline. This could be expanded upon in the future.

* I'd like to continue working with Tableau dashboards and implement more advanced features. Tableau seems like a really user-friendly tool and I had a great time putting together dashboards. It's a nice blend of art and science. 

Thank you!

Jeremy Beard 


<a name="references"/>

# References

I used a lot of references on this project for ensuring the way I handled the datetimes would be acceptable within a Machine Learning context. 

The Booking.com API link was another critical reference that enabled the rest of this project.

The total list of references and useful links is:

* https://github.com/jeremyabeard5/MSDS696 

* https://booking-com13.p.rapidapi.com/flights/one-way 

* https://stackoverflow.com/questions/40217369/python-linear-regression-predict-by-date 

* https://matplotlib.org/stable/gallery/style_sheets/style_sheets_reference.html 

* https://pandas.pydata.org/docs/reference/api/pandas.DatetimeIndex.dayofweek.html 

* https://pandas.pydata.org/docs/reference/api/pandas.Series.dt.month.html 

* https://stackoverflow.com/questions/71419004/how-to-plot-vertical-lines-at-specific-dates-in-matplotlib 

* https://medium.com/analytics-vidhya/calendar-heatmaps-a-perfect-way-to-display-your-time-series-quantitative-data-ad36bf81a3ed 

* https://calplot.readthedocs.io/en/latest/index.html 

* https://matplotlib.org/stable/users/explain/colors/colormaps.html 

* https://medium.com/analytics-vidhya/calendar-heatmaps-a-perfect-way-to-display-your-time-series-quantitative-data-ad36bf81a3ed 

* https://pypi.org/project/july/ 

* https://datascience.stackexchange.com/questions/2368/machine-learning-features-engineering-from-date-time-data 

* https://datascience.stackexchange.com/questions/112357/feature-engineering-for-datetime-column 

* https://www.reddit.com/r/learnpython/comments/chunas/correlation_with_day_of_week/ 

* https://mikulskibartosz.name/time-in-machine-learning 

* https://www.pycaret.org/tutorials/html/REG101.html 

* https://pycaret.readthedocs.io/en/latest/api/regression.html 






