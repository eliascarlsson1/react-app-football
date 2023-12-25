# App predicting if a football game will have over/under 2.5 scored goals.

# Note
This has been a side project of mine for some time. The aim of the project has always been casual: to learn data handling, fullstack development and machine learning models. The project was never meant for anyone else eyes than mine and that is very much reflected in the basic UI. This also means that I have not streamlined the process of installing this app on another machine. However there are requirement files (requirments.txt in the backend and package.json in the frontend) and the versions i use are python 3.11.1 and Node 20.5.0.

To see if the models actually say anything about the real world I have tracked ~200 bets that this project considers to be a "good bet" and the average rate of interest is ~2%. Considering that bookkeepers usually have a profit margin of ~5%, this means that my models are doing an ok job at predicting "good bets".

# General description
Historical football data from 12 european leagues are gathered (from https://www.football-data.co.uk). This data is processed to fit a machine learning algorithm. Then odds for future games are scraped from (www.oddsportal.com) and the machine learning algorithm is used to predict wether there will be over/under 2.5 goals scored in that game. All predicted games are then filtered to determine which games would be considered a profitable bet.

# Techniques

## Overview
The app is using a python flask API backend and a reactive frontend. Data is stored partly in csv files and partly in a sqlite database.

## Workflow
### Data preparation
Data is downloaded as csv files, containing pre-match odds and match results. This data is prepared in to columns suitable for a classification machine learning algorithm. Example of this input data can be:
- How many goals are scored on average when these two teams have played in the past
- How many goals are scored in an average game for the home team this season
- I also introduced an elo and an "tilt" model, based on historical matches from 2016-now, where teams are rated on their performance and "field tilt" (high tilt ~ many goals per game)
- What position is the team currently in the league
- The result of the classfication is 0 (under 2.5 goals) or 1 (over 2.5 goals)

### Model training
This data is then used to fit a XGBoost classification model, with some tweakable parameters.
- Number of classifiers
- Learning rate
- Tree depht
- Selecting which historical data to train on, to test on and to validate on
- Selecting which parameters should be included in the model

After training a model it is saved as a file. This file can then be loaded to apply the model on scraped data, or to see parameters for the training, such as:
- Feature importance
- Prediction probability
- Permutation 
- Rate of interest if betting according to the model on games

See example image

![model-statistics](https://github.com/eeliascarlsson/react_app_football/assets/106238885/1702f013-6bef-4490-a067-e4bdef2f65da)

(As you can see, my calculated parameters tilt and elo almost always turns out to be the most important feature)

### Scarping odds and predicting game
To determine which games would be a "good bet" i compare my calculated probability to the probability given by the odds. I also compare check if the odds is an outlier compared to other odds provided by other bookkeepers. 

The odds data is scraped using selenium and a chrome webdriver in python.

I then apply the model, and the filter for each scraped game and the if it is considered a "good bet" the end result looks like this:

![End result](https://github.com/eeliascarlsson/react_app_football/assets/106238885/a9e6de25-54e1-4b37-9c54-5380d4d4079a)
