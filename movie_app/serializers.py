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

#Validators
class DirectorValidateSerializer(serializers.Serializer):
    name = serializers.CharField(min_length=3, max_length=55)


class MovieValidateSerializer(serializers.Serializer):
    title = serializers.CharField(min_length=2, max_length=50)
    description = serializers.CharField(max_length=255)
    duration = serializers.FloatField(min_value=0)
    director = serializers.IntegerField()

    def validate(self, director):
        try:
            Director.objects.get(id = director)
        except Director.DoesNotExist:
            raise serializers.ValidationError('Director not found')
        return director


class ReviewValidateSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=255)
    stars = serializers.IntegerField(min_value=1, max_value=5)
    movie = serializers.IntegerField()

    def validate_movie(self, movie):
        try:
            Movie.objects.get(id=movie)
        except Movie.DoesNotExist:
            raise serializers.ValidationError('Movie not found')
        return movie