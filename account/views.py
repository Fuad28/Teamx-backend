from django.urls import reverse
from django.shortcuts import render, redirect
from django.http import HttpResponse

from rest_framework.views import APIView
# from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.response import Response
from  rest_framework.renderers import JSONRenderer
# from rest_framework.decorators import action
from rest_framework import status
from rest_framework.permissions import AllowAny,  IsAdminUser, IsAuthenticated


import requests
import json
from authlib.integrations.django_client import OAuth


from .serializers import ProfileSerializer

from .models import Profile,  User

class UserActivationView(APIView):
    def get (self, request, uid, token):
        protocol = 'https://' if request.is_secure() else 'http://'
        web_url = protocol + request.get_host()
        post_url = web_url + "/api/v1/users/activation/"
        post_data = {'uid': uid, 'token': token}
        result = requests.post(post_url, data = post_data)
        content = result.text
        return Response(content)

# class ProfileView(APIView):

#     def get(self, request, slug):
#         profile= Profile.objects.prefetch_related('user').get(slug= slug)
#         serializer= ProfileSerializer(profile)
#         return Response(serializer.data, status= status.HTTP_200_OK)

#     def put(self, request, slug):
#         profile= Profile.objects.select_related('user').get(slug= slug)
#         serializer= ProfileSerializer(profile, request.data)
#         serializer.is_valid(raise_exception= True)
#         serializer.save()
#         return Response(serializer.data, status= status.HTTP_200_OK)

#     def patch(self, request, slug):
#         return self.put(request, slug)


class ProfileView(RetrieveUpdateAPIView):
    lookup_field= 'slug'
    serializer_class= ProfileSerializer

    def get_queryset(self):
        return Profile.objects.prefetch_related('user').all()


#social authentication
CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
oauth = OAuth()
oauth.register(
    name='google',
    server_metadata_url=CONF_URL,
    client_kwargs={'scope': 'openid email profile'}
    )

def social_login(request):
    redirect_uri = request.build_absolute_uri(reverse('authorize')) #prompt=consent&access_type=offline need to be appended to the redirect uri 
    return oauth.google.authorize_redirect(request, redirect_uri)


def social_auth(request):
    token = oauth.google.authorize_access_token(request)
    user_info= token.get('userinfo')

    #check if user does not exit and save user
    if not User.objects.filter(email= user_info["email"]).exists():
        User.objects.create(email=user_info["email"], full_name= user_info["name"])

    return HttpResponse(json.dumps({"access_token": token.get('access_token')}))