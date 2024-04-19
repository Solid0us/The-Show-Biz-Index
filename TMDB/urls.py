from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path("login/", views.login_view, name='login_view'),
    path("logout/", views.logout_view, name="logout_view"),
    path("register/", views.register_view, name="register_view"),
    path("media/<str:media_type>/<int:media_id>/", views.media_page, name="media_page"),
    path("account/<int:user_id>/", views.account_view, name="account_view"),
    path("query/", views.search_all_type, name="search_all_type"),
    path("add_watching/<str:media_type>/<int:media_id>/", views.add_watchlist, name="add_watchlist"),
    path("remove_watch_status/<str:media_type>/<int:media_id>/", views.remove_watchstatus, name="remove_watchstatus"),
    path("plan_to_watch/<str:media_type>/<int:media_id>/", views.add_plan_to_watch, name="add_plan_to_watch"),
    path("finished_watching/<str:media_type>/<int:media_id>/", views.add_finished_watching, name="add_finished_watching"),
    path("review/<str:media_type>/<int:media_id>/", views.add_review, name="add_review"),
    path("editReview/<str:media_type>/<int:media_id>/", views.edit_review, name="edit_review"),
    path("movie_user_watchlist/<str:username>/", views.movie_watchlist, name="movie_watchlist"),
    path("tv_user_watchlist/<str:username>/", views.tv_watchlist, name="tv_watchlist")
]