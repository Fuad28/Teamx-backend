from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from rest_framework.serializers import ModelSerializer, SerializerMethodField, CharField

from .models import Profile, User

class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields= ["id", "full_name", "email", "password"]

class ProfileSerializer(ModelSerializer):
    full_name= CharField(source= 'user.full_name')
    email= CharField(source= 'user.email')
    class Meta:
        model= Profile
        fields= ["id", "full_name", "image",  "phone", "email" ,"language",  "country", "biography", "twitter_profile", "linkedln_profile", "website"]


    def update(self, instance, validated_data):
        user= User.objects.filter(email=instance.user.email).update(**validated_data["user"])
        instance.user= User.objects.get(pk= user)
        validated_data.pop("user", None)
        return super().update(instance, validated_data)