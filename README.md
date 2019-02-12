# Sentiment Analysis of 2016 Presidential Election News Coverage

### Introduction
The intention of this application is to allow for visualization of sentiment trends from printed
media over the course of the 2016 presidential election.

### Approach
300 articles, with titles containing the candidate's last name, were collected for each week of 2016 from the top 20 US news sources (per Alexa Global Rank on 1/12/2019).  Additionally, the 100 articles with the most shares on facebook from each week of the election cycle were also collected for each candidate.  The sentiment of each article was then determined using [vaderSentiment](https://github.com/cjhutto/vaderSentiment).
All news articles and data were obtained using the python api for  [Event Registry](https://eventregistry.org/).  A web application to view the results of the analysis was created using plotly dash and is available [online](https://news-sentiment-analysis.herokuapp.com/).

### Using the Web Application
The application was created using dash to allow for interactive visualizations.  The control panel can be utilized to select if the mean sentiment is calculated based on the article title or article body.  The user can also select if the mean sentiment is calculated by week or month, and if news sources should be ranked by total shares or mean shares.

The Mean Article Sentiment chart shows how sentiment tracked throughout the election cycle for each candidate, both for articles from the top news sources as well as those that were most shared on facebook.  If the user selects a point on this chart the Word Frequency, Shares by News Source and Shares vs. Sentiment graphs are all updated accordingly.  

Selecting a bar in the Shares by News Source graph limits the Shares vs. Sentiment graph to only that news source (shift+click allows for multiple selections and deselections).  Selecting a point on the Shares vs. Sentiment graph displays the article title and news source at the bottom of the dashboard.

I intend to release an article outlining my methodology in the near future.
