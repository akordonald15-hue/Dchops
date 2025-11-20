from django.urls import path
from .views import RegisterView, LoginView, RefreshTokenView, LogoutView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),

    # Custom login endpoint (sets HttpOnly refresh cookie)
    path('login/', LoginView.as_view(), name='login'),

    # Custom refresh endpoint (reads cookie, returns new access token)
    path('refresh/', RefreshTokenView.as_view(), name='token_refresh'),

    # Logout endpoint
    path('logout/', LogoutView.as_view(), name='logout'),
]
