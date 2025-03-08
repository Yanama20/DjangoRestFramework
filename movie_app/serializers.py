from .models import Director, Movie, Review
from rest_framework import serializers

class DirectorsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        exclude = ['id']    
    
class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = ['name', 'id' ]

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