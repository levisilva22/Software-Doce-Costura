from rest_framework import serializers
from .models import Product, UserProfile, UserInteraction, Recommendation, SimilarProducts

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

class UserInteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInteraction
        fields = '__all__'

class RecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recommendation
        fields = '__all__'

class SimilarProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SimilarProducts
        fields = '__all__'