# NBA-point-spread-bet

I am creating a model to calculate probability an NBA team beats the spread for any regular season matchup.

### Motivation
Basketball is my favorite sport to watch, specifically the NBA. Go Rockets!!
I thought it would be a fun endeavor to try to create a model to be at least break-even when betting on the spread.

### Getting Started
I started by gathering regular season spread data(closing line) from the 2014-2015 season through the 2017-2018 season. I also collected boxscore data for those seasons. With 5 seasons worth of data, I began exploring the data and coming up with ideas.

### Approach
My intial idea was come up with a method to estimate how many points each team would score. Then take that distribution of scoring differences and calculate a (1 - cumulative density function of the ((-1 * spread), avg scoring difference, avg score diff variance)

ex. if the spread for the Houston Rockets is -5.5 and their average scoring difference against the Dallas Mavericks is 7.5 points with variance say 20.

the probability of Houston scoring more than the spread would be (1 - cdf(5.5,7.5,20))) = 53.93%


