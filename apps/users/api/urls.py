from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'', UserViewSet, basename='user')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    # JWT Authentication endpoints
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # User CRUD endpoints
    path('', include(router.urls)),
]