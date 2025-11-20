from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer
import logging
from rest_framework.throttling import UserRateThrottle
from rest_framework.decorators import action
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

# --------------------------
# YOUR EXISTING SECURITY CODE
# --------------------------
admin_logger = logging.getLogger('admin_actions')

# inside your endpoint
# admin_logger.info(f"Admin {request.user.username} updated order {order.id} status from '{old_status}' to '{new_status}'")

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class AdminThrottle(UserRateThrottle):
    rate = '50/hour'  # max 50 requests per hour for admin users

# inside your ViewSet
# @action(detail=True, methods=['patch'], permission_classes=[permissions.IsAdminUser], throttle_classes=[AdminThrottle])
# def update_status(self, request, pk=None):
#     ...

# --------------------------
# STEP 10 AUTHENTICATION CODE (APPENDED)
# --------------------------

# --------------------------
# Login View
# --------------------------
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            response = Response({
                'access': str(refresh.access_token),
                'user': {'username': user.username, 'email': user.email}
            }, status=status.HTTP_200_OK)

            # Set HttpOnly refresh token cookie
            response.set_cookie(
                key='refresh_token',
                value=str(refresh),
                httponly=True,
                secure=True,       # True in production (HTTPS)
                samesite='Lax',
                max_age=7*24*60*60
            )
            return response

        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# --------------------------
# Refresh Token View
# --------------------------
class RefreshTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')

        if not refresh_token:
            return Response({'detail': 'Refresh token missing'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            token = RefreshToken(refresh_token)
            new_access = str(token.access_token)
            return Response({'access': new_access})
        except Exception:
            return Response({'detail': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)

# --------------------------
# Logout View
# --------------------------
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        response = Response({'detail': 'Logged out successfully'}, status=status.HTTP_200_OK)
        response.delete_cookie('refresh_token')
        return response
