from django.urls import path
from movie_app import views

urlpatterns = [
    path('directors/', views.directors_list_create_api_view),
    path('directors/<int:director_id>/', views.director_details_api_view),
    path('movies/', views.movies_list_create_api_view),
    path('movies/<int:movie_id>/', views.movie_detail_api_view),
    path('reviews/', views.reviews_list_create_api_view),
    path('reviews/<int:review_id>/', views.review_detail_api_view),
]