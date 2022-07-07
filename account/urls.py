
from django.contrib.auth import get_user_model
from django.urls import path

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt import views as simple_jwt_views
from djoser import views as djoser_views

import account.views as user_views

router = DefaultRouter()
router.register("", djoser_views.UserViewSet)


User = get_user_model()

# urlpatterns = router.urls


custom_urls= [
    #Token
    path("auth/login/", simple_jwt_views.TokenObtainPairView.as_view(), name="login"),
    path("auth/refresh/", simple_jwt_views.TokenRefreshView.as_view(), name="refresh-token"),
    path("auth/verify/", simple_jwt_views.TokenVerifyView.as_view(), name="verify-token"),

    #social auth
    path('social-auth/login/', user_views.social_login),
    path('social-auth/', user_views.social_auth, name='authorize'),

    path("activate/<uid>/<token>/", user_views.UserActivationView.as_view(), name="activate-account"),
    path("profile/<slug:slug>", user_views.ProfileView.as_view(), name="profile"),
    
    ]

urlpatterns = custom_urls + router.urls
