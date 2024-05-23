from django.urls import path
from .views import SignUpView, SignInView, signin_view
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('api/signup/', SignUpView.as_view(), name='signup'),
    path('api/signin/', SignInView.as_view(), name='signin'),
    path('signin/', signin_view, name='signin_view')
]