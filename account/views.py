from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.permissions import AllowAny,  IsAdminUser, IsAuthenticated


import requests

from .serializers import ProfileSerializer

from .models import Profile

class UserActivationView(APIView):
    def get (self, request, uid, token):
        protocol = 'https://' if request.is_secure() else 'http://'
        web_url = protocol + request.get_host()
        post_url = web_url + "/api/v1/users/activation/"
        post_data = {'uid': uid, 'token': token}
        result = requests.post(post_url, data = post_data)
        content = result.text
        return Response(content)

class ProfileView(APIView):

    def get(self, request, slug):
        profile= Profile.objects.prefetch_related('user').get(slug= slug)
        serializer= ProfileSerializer(profile)
        return Response(serializer.data, status= status.HTTP_200_OK)

    def put(self, request, slug):
        profile= Profile.objects.select_related('user').get(slug= slug)
        serializer= ProfileSerializer(profile, request.data)
        serializer.is_valid(raise_exception= True)
        serializer.save()
        return Response(serializer.data, status= status.HTTP_200_OK)

    def patch(self, request, slug):
        return self.put(request, slug)


class ProfileView(RetrieveUpdateAPIView):
    lookup_field= 'slug'
    serializer_class= ProfileSerializer

    def get_queryset(self):
        return Profile.objects.prefetch_related('user').all()