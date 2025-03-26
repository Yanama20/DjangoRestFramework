from django.urls import path
from movie_app import views

urlpatterns = [
    path('directors/', views.directors_list_create_api_view),
    path('directors/<int:id>/', views.director_details_api_view),
    path('movies/', views.movies_list_create_api_view),
    path('movies/<int:id>/', views.movie_detail_api_view),
    path('reviews/', views.reviews_list_create_api_view),
    path('reviews/<int:id>/', views.review_detail_api_view),
    path('movies/<int:id>/reviews/', views.movies_reviews_list_api_view),
    path('directors_cbv/', views.DirectorsListCreateAPIView.as_view()),
    path('directors_cbv/<int:id>/', views.DirectorDetailsAPIView.as_view()),
    path('movies_cbv/', views.MoviesAPIViewSet.as_view({
        'get': 'list', 'post': 'create',
        })),
    path('movies_cbv/<int:id>/', views.MoviesAPIViewSet.as_view({
        'get': 'retrieve', 'put': 'update', 'delete': 'destroy',
        })),
    path('reviews_cbv/', views.ReviewsAPIViewSet.as_view({
        'get': 'list', 'post': 'create',
        })),
    path('reviews_cbv/<int:id>/', views.ReviewsAPIViewSet.as_view({
        'get': 'retrieve', 'put': 'update', 'delete': 'destroy',
        })),
    path('movies_cbv/<int:movie_id>/reviews/', views.MoviesReviewsListAPIView.as_view()),
]