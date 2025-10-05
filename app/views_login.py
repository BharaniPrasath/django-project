from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from django.contrib.auth import authenticate, login as auth_login 
from django.contrib.auth import logout as django_logout

from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.tokens import RefreshToken

from . import serializers

User = get_user_model()

@api_view(['POST'])
def signup(request):
    username = request.data.get("username")
    email = request.data.get("email")
    password = request.data.get("password")

    # --- Username checks 
    if User.objects.filter(username=username).exists():
        return Response({"username": "This username is already taken."}, status=status.HTTP_400_BAD_REQUEST)

    # --- Email checks 
    if User.objects.filter(email=email).exists():
        return Response({"email": "This email is already registered."}, status=status.HTTP_400_BAD_REQUEST)

    # --- Password validation 
    try:
        validate_password(password, user=User(username=username, email=email))
    except ValidationError as e:
        return Response({"password": e.messages}, status=status.HTTP_400_BAD_REQUEST)

    # --- Save user with hashed password 
    user = User(username=username, email=email)
    user.set_password(password)
    user.save()

    return Response(
        {"message": "User created successfully!"},
        status=status.HTTP_201_CREATED
    )
    
    

@api_view(['POST'])
def login(request):   # ✅ renamed
    username = request.data.get("username")
    password = request.data.get("password")
    
    user = authenticate(username=username, password=password)
    if user is not None:
        auth_login(request, user)  # Django session login

        # Generate JWT token
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        return Response({
            "message": "Login successful",
            "access": access_token,
            "refresh": refresh_token
        }, status=status.HTTP_200_OK)
    else:
        return Response(
            {"error": "Invalid username or password"},
            status=status.HTTP_400_BAD_REQUEST
        )
        
        
        
        
@api_view(["POST"])
def logout(request):
    django_logout(request)  # ✅ just pass request
    return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)