# The Show Biz Index

## Introduction
The Show Biz Index is a web application which leverages TMDB's API to obtain movie and show data in which users can add to their watchlists, keep track of their progress, write reviews, and see what others have reviewed.

## Distinctiveness and Complexity
This project is unlike the other projects in the CS50W course. I believe the quality that stands out is that the core function of this web application is using TMDB's API and managing the data into how I wanted to be displayed in my own database. This added quite some complexity to the project since it made me question on how to best store the information that is received from API calls. On top of that, learning the API and seeing how its structured affected my approach in setting up Django templates and manipulating the database. Initially I assumed movie-related API calls were the same as TV shows until I read the documentation and studied the API structure. 

I experimented with the frontend by incorporating more interesting UI functions such as side scrolling, infinite scrolling and fetching API data when the bottom of the screen is reached, and showing/hiding divs using tabs in modals and web pages. It is worth mentioning that the infinite scrolling method saved a lot of time in loading the database. Initially, upon searching, **all** of the search results were loaded. This was not efficient. I opted to only call the API if the user reaches the bottom of the page. This also requires checking to see how many pages of search queries are there before making another API request.  

The movie and show data obtained from TMDB is saved to the local database everytime the user visits the movie/show page. This was a decision I made so that the backend doesn't always have to rely on fetching TMDB's API if it doesn't have to. This will reduce API call traffic in general. There are only two areas where TMDB's API is called for information and that is in the main page where the purpose is to get real time data from the site, and the search function since it would be unrealistic to store a huge amount of data in the local database and updating the database in the future will be an inconvenience.

## Created Files
### layout.html
This is the main layout template for the web application. It displays the general navigation bar at the top and filters elements depending on whether the user is logged in or not. 
### login.html
This is where the user logs in.
### register.html
This is where users register new accounts.
### index.html
This is the home page of the web application. The top 20 trending movies/shows queried from TMDB's API will always be displayed. The trending list will always be up-to-date upon refreshing of the page. Clicking on one of the media posters will lead the user to the respective web page. 

If the user has some movies or shows in the watchlist, the database keeps track of the top genres that the user tends to put on their watchlist. Up to three lists of movies and shows will be displayed filtered by the top three genres.

### search.html
To reach this page, the user will need to type in some keyword(s) into the search bar on the top right of any page. This will interact with TMDB's API to present a list of movies and TV shows. The first page of results will be displayed, but with the help of JavaScript, as the user scrolls to the bottom of the page, TMDB will query for the next page of search results as long as the last page has not been reached, resulting in an infinite scroll effect.

### media_info.html
Every movie and TV show will have its own media page where it displays the title, background poster, overview, and languages available. The user can write a review or edit an existing review if already written. The user can give a score and text for the review. If there are already at least one review for the movie/show, the average score will be displayed. The user can see all the reviews for that media as well. The user can add the media to one of three types of watchlists via a drop down menu. They are "Watching", "Completed", and "Plan to Watch". The media can be removed from these watchlists as well.

### account.html
Displays the movie and show statistics depending on the user. It will display number of movies and shows in each watchlist as well as a graphical representation of the top 5 genres in the movie and TV show list. There are three interactable elements in this page. The first is the "My Reviews" text which displays a modal when clicked. In the modal, reviews are divided into two tabs, one for movie and one for TV shows. The reviews are listed in reverse chronological order based on the last review edit. The other two elements are "My Movie Watchlist" and "My TV Watchlist". They will lead to "movie_watchlist.html" and "tv_watchlist.html" respectively. 

### movie_watchlist.html and tv_watchlist.html
These two pages are mirrors of each other except that one displays movies and the other displays TV shows. In these pages, the user can view the movies and shows in their watchlists. At the top of the page, there are three tabs in which the user can filter between different watchlists.

## tmdb.js
This file contains all the JavaScript functions for this project. 

## styles.css
This .css file contains most of the syling of the web application.

## models.py
There are several models in this module. It comes the *User* model that contains the default user data such as username and password. One is called *Genre* that contains all the genres and their ids from TMDB. The *Movie_log* model shows essential information about each movie and many-to-many fields for the watchlists. Similarly, the *Tv_show_log* model does the same thing but with TV shows instead. The *Movie_review* holds information about each movie's review left by users. Lastly, The *Tv_review* model mimics the same thing, but with TV shows.

## views.py
Handles all the backend part of the web application. 

## How to Run the Application
To run the application, start by issuing the *manage.py* runserver command. Depending on the PATH variable name it would look like "python3 manage.py runserver". Python module requirements can be found in *requirements.txt*. To start interacting with the web application, create an account to log in.




