from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from rest_framework.serializers import ModelSerializer

from .models import Profile

class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields= ["id", "full_name", "email", "password"]

class ProfileSerializer(ModelSerializer):
    class Meta:
        model= Profile
        fields= ["id", "user__full_name", "image", "email", "phone", "language",  "country", "biography", "twitter_profile", "linkedln_profile", "website"]
