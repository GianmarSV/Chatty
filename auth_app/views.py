from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from .serializers import UserSerializer, LoginSerializer
from django.shortcuts import render
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse



@extend_schema(
    request=UserSerializer,
    responses={
        201: OpenApiResponse(response=UserSerializer, description='User created successfully'),
        400: OpenApiResponse(description='Bad Request')
    },
    tags=["Authentication"],
    summary="User Sign-Up",
    description="Endpoint for user registration"
)
class SignUpView(APIView):
    permission_classes = (AllowAny,)
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    request=LoginSerializer,
    responses={
        200: OpenApiResponse(response=LoginSerializer, description='User signed in successfully'),
        400: OpenApiResponse(description='Bad Request'),
        401: OpenApiResponse(description='Unauthorized')
    },
    tags=["Authentication"],
    summary="User Sign-In",
    description="Endpoint for user login"
)
class SignInView(APIView):
    permission_classes = (AllowAny,)
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        print(serializer)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)

def signin_view(request):
    return render(request, 'auth_app/signin.html')
