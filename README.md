# NBA-point-spread-bet

I am creating a classification model that predicts the winning of regular season NBA games relative to the spread so I can win more lunch bets against my friend Eric.

## Motivation
Basketball is my favorite sport to watch, specifically the NBA. Go Rockets!!
It's even more exciting when you personally have something on the line. 
I have a friend named Eric who loves the NBA just as much as I do, maybe even more.
Eric and I will usually wager a meal on the points spread of a game. 

The probability of either outcome of the spread is usually 50%, so you have practically even odds for whatever side you end up choosing. If this is true then my long term expected value of lunches won against Eric will be about 0. I really, really, really wanted to win more lunch bets than him so I thought I could use machine learning to help acheive that goal.

## Getting Started
I started by gathering regular season spread data(closing line) from the 2014-2015 season through the 2017-2018 season. I also collected boxscore data for those seasons. With 5 seasons worth of data, I starting doing exploratory data analysis.

## Approach
Train some classification models with greater than 50% accuracy when betting on the spread.
I chose Logistic Regression, Random Forest Classifier and Gradient Boosting Classifier to work with.

## Thoughts on Feature Selection
The idea I had was to use all rolling averages of each team in a particular matchup. I started with a window length of 5 (previous 5 games) and that became the main features I used to transform my data for training. I also included the each team's record against the spread. The record was represented as the proportion of wins against the spread to total games played. 
This column was a little tricky to create because if you just took the cumulative sum of a team's result against the spread and added it as a feature column it would introduce data leakage. So I took the cumulative sum then shifted the results and inserted a row above with 0.0 for the first game of the season. It also meant excluding the last row of the cumulative sum.

## Results
Logistic Regression was the most consistent over every iteration of the train/test setup. There were only 3 instances of the 28 train/test scenarios where it failed to return at least 50.0% accuracy. I will try to include graphs of the information as well as a cleaned up jupyter notebook of my work soon.

![alt text](https://github.com/jonlin84/NBA-point-spread-bet/blob/master/images/Logistic%20Regression%20Avgs%20Graph.png)

Random Forest and Gradient Boosting both had several instances where the model performed well below 50.0% (47-48% range)

![alt text](https://github.com/jonlin84/NBA-point-spread-bet/blob/master/images/Logistic%20Regression%20Graph.png)

Using a rolling average of 6 games back offered the best results in terms of overall accuracy so I decided to train my model for next season using that window length. 

Using a 6-game 
