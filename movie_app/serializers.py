from .models import Director, Movie, Review
from rest_framework import serializers

class DirectorsListSerializer(serializers.ModelSerializer):
    movies_count = serializers.SerializerMethodField()
    class Meta:
        model = Director
        fields = ['name', 'movies_count']

    def get_movies_count(self, director):
        return director.movies.count()
    
class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = ['id', 'name' ]

class MoviesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['title', 'director']

class MovieDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['title', 'description', 'duration', 'director']

class ReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['movie']
    
class ReviewDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class MoviesReviewsSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    reviews = ReviewDetailSerializer(many=True, read_only=True)
    class Meta:
        model = Movie
        fields = ['title', 'reviews', 'rating']

    def get_rating(self, movie):
        if movie.reviews.count() == 0:
            return 0
        else:
            reviews = movie.reviews.all()
            total = sum([review.stars for review in reviews if review.stars is not None])
            return total / movie.reviews.count()
