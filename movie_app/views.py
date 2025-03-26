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
    MoviesReviewsSerializer,
    DirectorValidateSerializer,
    MovieValidateSerializer,
    ReviewValidateSerializer
)
from django.db import transaction
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView


class CustomPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            'total': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data,
        })
    

#Directors:

class DirectorsListCreateAPIView(ListCreateAPIView):
    queryset = Director.objects.all()
    serializer_class = DirectorsListSerializer
    pagination_class = CustomPagination
    def post(self, request, *args, **kwargs):
        serilazer = DirectorValidateSerializer(data=request.data)
        if not serilazer.is_valid():
            return Response(data=serilazer.errors, status=status.HTTP_400_BAD_REQUEST)
        name = serilazer.validated_data.get('name')
        director = Director.objects.create(name=name)
        return Response(data=DirectorSerializer(director).data, status=status.HTTP_201_CREATED)
    

@api_view(http_method_names=['GET', 'POST'])
def directors_list_create_api_view(request):
    if request.method == 'GET':
        directors = Director.objects.all()
        data = DirectorsListSerializer(directors, many=True).data
        return Response(data=data)
    elif request.method == 'POST':
        serilazer = DirectorValidateSerializer(data=request.data)
        if not serilazer.is_valid():
            return Response(data=serilazer.errors, status=status.HTTP_400_BAD_REQUEST)
        name = serilazer.validated_data.get('name')
        director = Director.objects.create(name=name)
        return Response(data=DirectorSerializer(director).data, status=status.HTTP_201_CREATED)
            


class DirectorDetailsAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer
    lookup_field = 'id'
    def put(self, request, *args, **kwargs):
        director = Director.objects.get(id=id)
        serilazer = DirectorValidateSerializer(data=request.data)
        if not serilazer.is_valid():
            return Response(data=serilazer.errors, status=status.HTTP_400_BAD_REQUEST)
        director.name = serilazer.validated_data.get('name')
        director.save()
        return Response(data=DirectorSerializer(director).data, status=status.HTTP_201_CREATED)


@api_view(http_method_names=['GET', 'PUT', 'DELETE'])
def director_details_api_view(request, id):
    try:
        director = Director.objects.get(id=id)
    except Director.DoesNotExist:
        return Response({'error': 'Director not found'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = DirectorSerializer(director).data
        return Response(data=data)
    elif request.method == 'DELETE':
        director.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        serilazer = DirectorValidateSerializer(data=request.data)
        if not serilazer.is_valid():
            return Response(data=serilazer.errors, status=status.HTTP_400_BAD_REQUEST)
        director.name = serilazer.validated_data.get('name')
        director.save()
        return Response(data=DirectorSerializer(director).data, status=status.HTTP_201_CREATED)
    



#Movies:


class MoviesAPIViewSet(ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MoviesSerializer
    pagination_class = CustomPagination
    lookup_field = 'id'

    def post(self, request, *args, **kwargs):
        serialazer = MovieValidateSerializer(data=request.data)
        if not serialazer.is_valid():
            return Response(data=serialazer.errors, status=status.HTTP_400_BAD_REQUEST)
        title = serialazer.validated_data.get('title')
        description = serialazer.validated_data.get('description')
        duration = serialazer.validated_data.get('duration')
        director_id = serialazer.validated_data.get('director')

    def put(self, request, *args, **kwargs):
        movie_id = self.kwargs['id']
        movie = Movie.objects.get(id=movie_id)
        serialazer = MovieValidateSerializer(data=request.data)
        if not serialazer.is_valid():
            return Response(data=serialazer.errors, status=status.HTTP_400_BAD_REQUEST)
        movie.title = serialazer.validated_data.get('title')
        movie.description = serialazer.validated_data.get('description')
        movie.duration = serialazer.validated_data.get('duration')
        movie.director = serialazer.validated_data.get('director')
        movie.save()
        return Response(data=MovieDetailSerializer(movie).data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        movie_id = self.kwargs['id']
        movie = Movie.objects.get(id=movie_id)
        data = MovieDetailSerializer(movie).data
        return Response(data=data)
    
    def put(self, request, *args, **kwargs):
        movie_id = self.kwargs['id']
        movie = Movie.objects.get(id=movie_id)
        serialazer = MovieValidateSerializer(data=request.data)
        if not serialazer.is_valid():
            return Response(data=serialazer.errors, status=status.HTTP_400_BAD_REQUEST)
        movie.title = serialazer.validated_data.get('title')
        movie.description = serialazer.validated_data.get('description')
        movie.duration = serialazer.validated_data.get('duration')
        movie.director = serialazer.validated_data.get('director')
        movie.save()
        return Response(data=MovieDetailSerializer(movie).data, status=status.HTTP_201_CREATED)

@api_view(http_method_names=['GET', 'POST'])
def movies_list_create_api_view(request):
    if request.method == 'GET':
        movies = Movie.objects.all()
        data = MoviesSerializer(movies, many=True).data
        return Response(data=data)
    elif request.method == 'POST':
        serialazer = MovieValidateSerializer(data=request.data)
        if not serialazer.is_valid():
            return Response(data=serialazer.errors, status=status.HTTP_400_BAD_REQUEST)
        title = serialazer.validated_data.get('title')
        description = serialazer.validated_data.get('description')
        duration = serialazer.validated_data.get('duration')
        director_id = serialazer.validated_data.get('director')
        # with transaction.atomic():
        movie = Movie.objects.create(
            title=title,
            description=description,
            duration=duration,
            director_id=director_id
        )
        return Response(data=MovieDetailSerializer(movie).data, status=status.HTTP_201_CREATED)

@api_view(http_method_names=['GET', 'PUT', 'DELETE'])
def movie_detail_api_view(request, id):
    try:
        movie = Movie.objects.get(id=id)
    except Movie.DoesNotExist:
        return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = MovieDetailSerializer(movie).data
        return Response(data=data)
    if request.method == 'DELETE':
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        serialazer = MovieValidateSerializer(data=request.data)
        if not serialazer.is_valid():
            return Response(data=serialazer.errors, status=status.HTTP_400_BAD_REQUEST)
        movie.title = serialazer.validated_data.get('title')
        movie.description = serialazer.validated_data.get('description')
        movie.duration = serialazer.validated_data.get('duration')
        movie.director = serialazer.validated_data.get('director')
        movie.save()
        return Response(data=MovieDetailSerializer(movie).data, status=status.HTTP_201_CREATED)



#Reviews:

class ReviewsAPIViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewsSerializer
    pagination_class = CustomPagination
    lookup_field = 'id'
    def post(self, request, *args, **kwargs):
        serializer = ReviewValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        text = serializer.validated_data.get('text')
        stars = serializer.validated_data.get('stars')
        movie_id = serializer.validated_data.get('movie')
        review = Review.objects.create(
            text=text,
            stars=stars,
            movie_id=movie_id
        )
        return Response(data=ReviewDetailSerializer(review).data, status=status.HTTP_201_CREATED)
    def retrieve(self, request, *args, **kwargs):
        review_id = self.kwargs['id']
        review = Review.objects.get(id=review_id)
        data = ReviewDetailSerializer(review).data
        return Response(data=data, status=status.HTTP_200_OK)
    def put(self, request, *args, **kwargs):
        review_id = self.kwargs['id']
        review = Review.objects.get(id=review_id)
        serializer = ReviewValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        review.text = serializer.validated_data.get('text')
        review.stars = serializer.validated_data.get('stars')
        review.movie = serializer.validated_data.get('movie')
        review.save()
        return Response(data=ReviewDetailSerializer(review).data, status=status.HTTP_201_CREATED)

@api_view(http_method_names=['GET', 'POST'])
def reviews_list_create_api_view(request):
    if request.method == 'GET':
        reviews = Review.objects.all()
        data = ReviewsSerializer(reviews, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = ReviewValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        text = serializer.validated_data.get('text')
        stars = serializer.validated_data.get('stars')
        movie_id = serializer.validated_data.get('movie')
        review = Review.objects.create(
            text=text,
            stars=stars,
            movie_id=movie_id
        )
        return Response(data=ReviewDetailSerializer(review).data, status=status.HTTP_201_CREATED)

@api_view(http_method_names=['GET','DELETE', 'PUT'])
def review_detail_api_view(request, id):
    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response({'error': 'Review not found'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = ReviewDetailSerializer(review).data
        return Response(data=data, status=status.HTTP_200_OK)
    if request.method == 'DELETE':
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        serializer = ReviewValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        review.text = serializer.validated_data.get('text')
        review.stars = serializer.validated_data.get('stars')
        review.movie = serializer.validated_data.get('movie')
        review.save()
        return Response(data=ReviewDetailSerializer(review).data, status=status.HTTP_201_CREATED)


class MoviesReviewsListAPIView(ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MoviesReviewsSerializer
    pagination_class = CustomPagination

@api_view(http_method_names=['GET'])
def movies_reviews_list_api_view(request):
    movies = Movie.objects.all()
    data = MoviesReviewsSerializer(movies, many=True).data
    return Response(data=data)      