from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.db import IntegrityError
from django.urls import reverse
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from . models import User, Movie_log, Tv_show_log, Movie_review, Tv_review, Genre
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json
import requests
from collections import Counter
from datetime import datetime

# Create your views here.

API_KEY = "7992589328f0812ec36e2ff941606e1b"

#URLS for API query
## Add "&page={number}" to go to specific trending page
movie_genre_url = "https://api.themoviedb.org/3/genre/movie/list?language=en"
tv_genre_url = "https://api.themoviedb.org/3/genre/tv/list?language=en"
trending_url = "https://api.themoviedb.org/3/trending/all/day?language=en-US"
backdrop_url = "https://www.themoviedb.org/t/p/w440_and_h660_face"
empty_poster_url = "https://cdn.vectorstock.com/i/preview-1x/48/06/image-preview-icon-picture-placeholder-vector-31284806.jpg"

ON_WATCHLIST_MESSAGE = "On watchlist"
COMPLETED_WATCHING_MESSAGE = "Completed Watching"
PLAN_TO_WATCH_MESSAGE = "Plan to Watch"


headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI3OTkyNTg5MzI4ZjA4MTJlYzM2ZTJmZjk0MTYwNmUxYiIsInN1YiI6IjY0N2MxZGE1OTM4MjhlMDBiZjllYjkxNSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.2gDv5tzYMOJOHdNwEqfr7vvWU-zbALQfys14gyWt0pE"
}

movie_genre_response = requests.get(movie_genre_url, headers=headers)
movie_genre_json = movie_genre_response.json()['genres']
tv_genre_response = requests.get(tv_genre_url, headers=headers)
tv_genre_json = tv_genre_response.json()['genres']

for movie_genre in movie_genre_json:
    new_movie_genre = Genre(genre=movie_genre['name'], id=movie_genre['id'])
    new_movie_genre.save()
for tv_genre in tv_genre_json:
    new_tv_genre = Genre(genre=tv_genre['name'], id=tv_genre['id'])
    new_tv_genre.save()
    
def index(request):
    # Return later to include trending shows depending on user's genre preferences
    try:
        genre_list = []
        genre_names = []
        genre_numbers = []
        response = requests.get(trending_url+'&page=1', headers=headers)
        trending_json_text = response.json()
        trending_results = trending_json_text['results']
        movies_watching = Movie_log.objects.filter(movie_watcher__in=[request.user])
        movies_watched = Movie_log.objects.filter(finished_watcher__in=[request.user])
        movies_planned_watching = Movie_log.objects.filter(planned_watcher__in=[request.user])
        tv_watching = Tv_show_log.objects.filter(tv_watcher__in=[request.user])
        tv_watched = Tv_show_log.objects.filter(finished_watcher__in=[request.user])
        tv_planned_watching = Tv_show_log.objects.filter(planned_watcher__in=[request.user])
        for movie in movies_planned_watching:
            for genre in movie.movie_genre.all():
                genre_list.append(genre.genre)
        for movie in movies_watched:
            for genre in movie.movie_genre.all():
                genre_list.append(genre.genre)
        for movie in movies_watching:
            for genre in movie.movie_genre.all():
                genre_list.append(genre.genre)
        
        for tv in tv_planned_watching:
            for genre in tv.tv_genre.all():
                genre_list.append(genre.genre)
        for tv in tv_watched:
            for genre in tv.tv_genre.all():
                genre_list.append(genre.genre)
        for tv in tv_watching:
            for genre in tv.tv_genre.all():
                genre_list.append(genre.genre)
        counted_genre_list = Counter(genre_list).items()
        sorted_genre = []
        for item in counted_genre_list:
            sorted_genre.append(item)
        sorted_genre.sort(key=lambda x:x[1], reverse=True)
        top_3_genres = sorted_genre[:3]
        list_3_genres = [list(x) for x in top_3_genres]
        top_3_genre_query_result = []
        for genre in top_3_genres:
            temp_list = []
            page = 1
            for result in trending_results:
                if Genre.objects.get(pk=genre[0]).id in result['genre_ids']:
                    temp_list.append(result)
            while len(temp_list) < 20:
                page += 1
                response = requests.get(trending_url+f'&page={page}', headers=headers)
                search_more_json_text = response.json()
                search_more_results = search_more_json_text['results']
                for more_result in search_more_results:
                    if Genre.objects.get(pk=genre[0]).id in more_result['genre_ids']:
                        temp_list.append(more_result)
                    if len(temp_list) == 20:
                        break
            top_3_genre_query_result.append(temp_list)
        for i in range(len(top_3_genre_query_result)):
            list_3_genres[i].append(top_3_genre_query_result[i])
    except:
        return render(request,'index.html')
    return render(request, 'index.html', {
        "trending_results": trending_results,
        "backdrop_url": backdrop_url,
        "top_3_genres": list_3_genres
    })

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, "login.html", {
                "message": "You have entered invalid login credentials"
            })
    else:
        return render(request, "login.html")

def logout_view(request):
    if request.method == "GET":
        logout(request)
        return render(request, "login.html")
    
def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if username == None:
            return render(request, "register.html", {
                "message": "Username cannot be empty."
            })
        if password != confirmation:
            return render(request, "register.html", {
                "message": "Passwords do not match."
            })
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "register.html", {
                "message": "Username already exists."
            })
        login(request, user)
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, 'register.html')
    
def account_view(request, user_id):
    if request.method == "GET":
        movie_genre_list = []
        movie_pie_genre_names = []
        movie_pie_genre_numbers = []
        tv_genre_list = []
        tv_pie_genre_names = []
        tv_pie_genre_numbers = []
        login_user = User.objects.get(id=user_id)
        # Checking number of objects whose manytomany field contains the logged in user
        movies_watching = Movie_log.objects.filter(movie_watcher__in=[request.user])
        movies_watched = Movie_log.objects.filter(finished_watcher__in=[request.user])
        movies_planned_watching = Movie_log.objects.filter(planned_watcher__in=[request.user])
        tv_watching = Tv_show_log.objects.filter(tv_watcher__in=[request.user])
        tv_watched = Tv_show_log.objects.filter(finished_watcher__in=[request.user])
        tv_planned_watching = Tv_show_log.objects.filter(planned_watcher__in=[request.user])
        
        for movie in movies_planned_watching:
            for genre in movie.movie_genre.all():
                movie_genre_list.append(genre.genre)
        for movie in movies_watched:
            for genre in movie.movie_genre.all():
                movie_genre_list.append(genre.genre)
        for movie in movies_watching:
            for genre in movie.movie_genre.all():
                movie_genre_list.append(genre.genre)
        movie_counted_genre_list = Counter(movie_genre_list).items()
        for item in movie_counted_genre_list:
            movie_pie_genre_names.append(item[0])
            movie_pie_genre_numbers.append(item[1])
        for tv in tv_planned_watching:
            for genre in tv.tv_genre.all():
                tv_genre_list.append(genre.genre)
        for tv in tv_watched:
            for genre in tv.tv_genre.all():
                tv_genre_list.append(genre.genre)
        for tv in tv_watching:
            for genre in tv.tv_genre.all():
                tv_genre_list.append(genre.genre)
        tv_counted_genre_list = Counter(tv_genre_list).items()
        for item in tv_counted_genre_list:
            tv_pie_genre_names.append(item[0])
            tv_pie_genre_numbers.append(item[1])

        top_5_movie_genre_names = movie_pie_genre_names[:5]
        top_5_movie_genre_numbers = movie_pie_genre_numbers[:5]
        top_5_tv_genre_names = tv_pie_genre_names[:5]
        top_5_tv_genre_numbers = tv_pie_genre_numbers[:5]
        movie_reviews = Movie_review.objects.filter(reviewer=request.user).order_by("-review_date")
        tv_reviews = Tv_review.objects.filter(reviewer=request.user).order_by("-review_date")
        
        return render(request, "account.html", {
            "user": login_user,
            "movies_watched": movies_watched,
            "movies_watching": movies_watching,
            "tv_watched": tv_watched,
            "tv_watching": tv_watching,
            "empty_poster_url": empty_poster_url,
            "movies_planned_watching": movies_planned_watching,
            "movie_pie_genre_names": json.dumps(top_5_movie_genre_names),
            "movie_pie_genre_numbers": json.dumps(top_5_movie_genre_numbers),
            "tv_pie_genre_names": json.dumps(top_5_tv_genre_names),
            "tv_pie_genre_numbers": json.dumps(top_5_tv_genre_numbers),
            "tv_planned_watching": tv_planned_watching,
            "movie_reviews": movie_reviews,
            "tv_reviews": tv_reviews
        })
    
def media_page(request, media_type, media_id):
    if request.method == "GET":
        #Query TMDB by media id to get information
        media_result = search_by_media_type(media_type, media_id)
        add_local_database(media_type, media_result)
        watch_status = ""
        if media_type == "tv":
            media = Tv_show_log.objects.get(tv_id=media_id)
            reviews = Tv_review.objects.filter(tv_id=media_id).order_by("-review_date")
            try:
                user_review_score = reviews.get(reviewer=request.user, tv_id=media_id).score
                user_review_text = reviews.get(reviewer=request.user).review
            except:
                user_review_score = ""
                user_review_text = ""
            tally_score = 0
            if len(reviews) > 0:
                for review in reviews:
                    tally_score += review.score
                average_score = round(tally_score/len(reviews),2)
            else:
                average_score = "No reviews"
            if media.tv_watcher.filter(username=request.user).exists():
                watch_status = ON_WATCHLIST_MESSAGE
            elif media.finished_watcher.filter(username=request.user).exists():
                watch_status = COMPLETED_WATCHING_MESSAGE
            elif media.planned_watcher.filter(username=request.user).exists():
                watch_status = PLAN_TO_WATCH_MESSAGE
            if len(Tv_review.objects.filter(tv_id=media_id, reviewer=request.user)) >= 1:
                reviewed = True
            else:
                reviewed = False
        else:
            media = Movie_log.objects.get(movie_id=media_id)
            reviews = Movie_review.objects.filter(movie_id=media_id).order_by("-review_date")
            try:
                user_review_score = reviews.get(reviewer=request.user, movie_id=media_id).score
                user_review_text = reviews.get(reviewer=request.user, movie_id=media_id).review
            except:
                user_review_score = ""
                user_review_text = ""
            tally_score = 0
            if len(reviews) > 0:
                for review in reviews:
                    tally_score += review.score
                average_score = round(tally_score/len(reviews),2)
            else:
                average_score = "No reviews"
            if media.movie_watcher.filter(username=request.user).exists():
                watch_status = ON_WATCHLIST_MESSAGE
            elif media.finished_watcher.filter(username=request.user).exists():
                watch_status = COMPLETED_WATCHING_MESSAGE
            elif media.planned_watcher.filter(username=request.user).exists():
                watch_status = PLAN_TO_WATCH_MESSAGE
            if len(Movie_review.objects.filter(movie_id=media_id, reviewer=request.user)) >= 1:
                reviewed = True
            else:
                reviewed = False
        return render(request, 'media_info.html', {
            "media": media_result,
            "backdrop_url": backdrop_url,
            "media_type": media_type,
            "media_id": media_id,
            "media_str_json": json.dumps(media_result),
            "empty_poster_url": empty_poster_url,
            "watch_status": watch_status,
            "reviewed": reviewed,
            "average_score": average_score,
            "reviews": reviews,
            "user_review_score": user_review_score,
            "user_review_text": user_review_text
        })

def search_by_media_type(media_type, media_id):
    if media_type == 'tv':
        search_tv_url = f"https://api.themoviedb.org/3/tv/{media_id}?api_key={API_KEY}"
        tv_response = requests.get(search_tv_url, headers=headers)
        tv_response_json = tv_response.json()
        #see json tv response
        return tv_response_json
    elif media_type == 'movie':
        search_movie_url = f"https://api.themoviedb.org/3/movie/{media_id}?api_key={API_KEY}"
        movie_response = requests.get(search_movie_url, headers=headers)
        movie_response_json = movie_response.json()
        return movie_response_json
    else:
        return 1

# Searches for either all movie and tv shows. Displays 20 results per query.
def search_all_type(request):
    if request.method == "GET":
        search_query = request.GET['query']
        search_results_list = []
        page_number = 1
        search_url = f"https://api.themoviedb.org/3/search/multi?query={search_query}&include_adult=false&language=en-US&page={page_number}"
        search_response = requests.get(search_url, headers=headers)
        search_response_json = search_response.json()
        search_response_json_results = search_response_json['results']
        search_results_list.append(search_response_json_results)
        total_pages = search_response_json['total_pages']
        return render(request, 'search.html', {
            "search_query": search_query,
            "search_results": search_response_json_results,
            "total_pages": total_pages,
            "backdrop_url":backdrop_url,
            "empty_poster_url": empty_poster_url
        })

def add_watchlist(request, media_type, media_id):
    if media_type == "tv":
        media = Tv_show_log.objects.get(tv_id=media_id)
        media.tv_watcher.add(request.user)
    else:
        media = Movie_log.objects.get(movie_id=media_id)
        media.movie_watcher.add(request.user)
    watch_status = ON_WATCHLIST_MESSAGE
    media.finished_watcher.remove(request.user)
    media.planned_watcher.remove(request.user)
    return JsonResponse({"message": f"Added to {media_type} watchlist. ID is {media_id}", "watch_status": watch_status})

def add_plan_to_watch(request, media_type, media_id):
    if media_type == "tv":
        media = Tv_show_log.objects.get(tv_id=media_id)
        media.tv_watcher.remove(request.user)
    else:
        media = Movie_log.objects.get(movie_id=media_id)
        media.movie_watcher.remove(request.user)
    watch_status = PLAN_TO_WATCH_MESSAGE
    media.planned_watcher.add(request.user)
    media.finished_watcher.remove(request.user)
    return JsonResponse({"message": "Added to Plan to Watch", "watch_status": watch_status})

def add_finished_watching(request, media_type, media_id):
    if media_type == "tv":
        media = Tv_show_log.objects.get(tv_id=media_id)
        media.tv_watcher.remove(request.user)
    else:
        media = Movie_log.objects.get(movie_id=media_id)
        media.movie_watcher.remove(request.user)
    watch_status = COMPLETED_WATCHING_MESSAGE
    media.planned_watcher.remove(request.user)
    media.finished_watcher.add(request.user)
    return JsonResponse({"message": "Added to Finished Watching.", "watch_status": watch_status})

def remove_watchstatus(request, media_type, media_id):
    if media_type == "tv":
        media = Tv_show_log.objects.get(tv_id=media_id)
        media.tv_watcher.remove(request.user)
    else:
        media = Movie_log.objects.get(movie_id=media_id)
        media.movie_watcher.remove(request.user)
    watch_status = ""
    media.finished_watcher.remove(request.user)
    media.planned_watcher.remove(request.user)
    return JsonResponse({"message": "Removed all watch statuses.", "watch_status": watch_status})

def add_local_database(media_type, media_json):
    if media_json['poster_path'] is None:
        poster_path = empty_poster_url
    else:
        poster_path = backdrop_url + media_json['poster_path']
    if media_type == 'movie':
        media = Movie_log(movie_id=media_json['id'], movie_name=media_json['original_title'], backdrop_url=poster_path)
        media.save()
        for genre in media_json['genres']:
            media.movie_genre.add(genre['name'])
    else:
        media = Tv_show_log(tv_id=media_json['id'], tv_name=media_json['name'], backdrop_url=poster_path)
        media.save()
        for genre in media_json['genres']:
            media.tv_genre.add(genre['name'])

def add_review(request, media_type, media_id):
    if request.method == "POST":
        data = json.loads(request.body)
        review_text = data.get('review')
        try:
            review_score = int(data.get('score'))
        except ValueError:
            return HttpResponse('Value Error')
        if review_score < 1 or review_score > 10:
            return HttpResponse("Review score must be between 1-10.")
        if media_type == "movie":
            id = Movie_log.objects.get(pk=media_id)
            if len(Movie_review.objects.filter(reviewer=request.user, movie_id=id)) >= 1:
                return JsonResponse({"message":"Already wrote a review.", "reviewed":True})
            review = Movie_review(reviewer=request.user, movie_id=id, review=review_text, score=review_score)
        else:
            id = Tv_show_log.objects.get(pk=media_id)
            if len(Tv_review.objects.filter(reviewer=request.user, tv_id=id)) >= 1:
                return JsonResponse({"message":"Already wrote a review.", "reviewed":True})
            review = Tv_review(reviewer=request.user, tv_id=id, review=review_text, score=review_score)
        review.save()
        return JsonResponse({"message": "Left a review", "average_review":"", "user_review_score":review_score})
    
def edit_review(request, media_type, media_id):
    if request.method == "POST":
        data = json.loads(request.body)
        review_text = data.get('review')
        try:
            review_score = int(data.get('score'))
        except ValueError:
            return HttpResponse('Value Error')
        if review_score < 1 or review_score > 10:
            return HttpResponse("Review score must be between 1-10.")
        if media_type == "movie":
            id = Movie_log.objects.get(pk=media_id)
            review = Movie_review.objects.filter(reviewer=request.user, movie_id=id).update(review=review_text, score=review_score, review_date=datetime.now())
        else:
            id = Tv_show_log.objects.get(pk=media_id)
            review = Tv_review.objects.filter(reviewer=request.user, tv_id=id).update(review=review_text, score=review_score, review_date=datetime.now())
        if media_type == "tv":
            reviews = Tv_review.objects.filter(tv_id=media_id)
        elif media_type == "movie":
            reviews = Movie_review.objects.filter(movie_id=media_id)
        tally_score = 0
        for user_review in reviews:
            tally_score += user_review.score
        average_score = round(tally_score/len(reviews),2)
        return JsonResponse({"message": "Edited a review", "average_score": average_score, "user_review_score":review_score})

def movie_watchlist(request, username):
    if request.method == "GET":
        movies_watching = Movie_log.objects.filter(movie_watcher__in=[request.user])
        movies_watched = Movie_log.objects.filter(finished_watcher__in=[request.user])
        movies_planned_watching = Movie_log.objects.filter(planned_watcher__in=[request.user])
        movie_reviews = Movie_review.objects.filter(reviewer=request.user).values("reviewer", "score", "movie_id")
        return render(request, "movie_watchlist.html", {
            "movies_watching": movies_watching,
            "movies_watched": movies_watched,
            "movies_planned_watching": movies_planned_watching,
            "movie_reviews": movie_reviews
        })
    
def tv_watchlist(request, username):
    if request.method == "GET":
        tv_watching = Tv_show_log.objects.filter(tv_watcher__in=[request.user])
        tv_watched = Tv_show_log.objects.filter(finished_watcher__in=[request.user])
        tv_planned_watching = Tv_show_log.objects.filter(planned_watcher__in=[request.user])
        tv_reviews = Tv_review.objects.filter(reviewer=request.user).values("reviewer", "score", "tv_id")
        return render(request, "tv_watchlist.html", {
            "tv_watching": tv_watching,
            "tv_watched": tv_watched,
            "tv_planned_watching": tv_planned_watching,
            "tv_reviews": tv_reviews
        })
