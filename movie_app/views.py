from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Director, Movie, Review
from .serializers import (
    DirectorsListSerializer,
    DirectorSerializer,
    MoviesSerializer,
    MovieDetailSerializer,
    ReviewsSerializer,
    ReviewDetailSerializer,
    MoviesReviewsSerializer
)
# Create your views here.

@api_view(http_method_names=['GET'])
def directors_list_api_view(request):
    directors = Director.objects.all()
    data = DirectorsListSerializer(directors, many=True).data
    return Response(data=data)

@api_view(http_method_names=['GET'])
def director_api_view(request, id):
    try:
        director = Director.objects.get(id=id)
    except Director.DoesNotExist:
        return Response({'error': 'Director not found'}, status=status.HTTP_404_NOT_FOUND)
    data = DirectorSerializer(director).data
    return Response(data=data)

@api_view(http_method_names=['GET'])
def movies_list_api_view(request):
    movies = Movie.objects.all()
    data = MoviesSerializer(movies, many=True).data
    return Response(data=data)

@api_view(http_method_names=['GET'])
def movie_detail_api_view(request, id):
    try:
        movie = Movie.objects.get(id=id)
    except Movie.DoesNotExist:
        return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
    data = MovieDetailSerializer(movie).data
    return Response(data=data)

@api_view(http_method_names=['GET'])
def reviews_list_api_view(request):
    reviews = Review.objects.all()
    data = ReviewsSerializer(reviews, many=True).data
    return Response(data=data, status=status.HTTP_200_OK)

@api_view(http_method_names=['GET'])
def review_detail_api_view(request, id):
    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response({'error': 'Review not found'}, status=status.HTTP_404_NOT_FOUND)
    data = ReviewDetailSerializer(review).data
    return Response(data=data, status=status.HTTP_200_OK)

@api_view(http_method_names=['GET'])
def movies_reviews_list_api_view(request):
    movies = Movie.objects.all()
    data = MoviesReviewsSerializer(movies, many=True).data
    return Response(data=data)