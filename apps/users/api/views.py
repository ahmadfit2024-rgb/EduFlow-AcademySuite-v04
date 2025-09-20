from rest_framework import viewsets, permissions
from apps.users.models import CustomUser
from .serializers import UserSerializer
from .permissions import IsAdminRole
from rest_framework_simplejwt.views import TokenObtainPairView

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    Access is restricted to Admin users only.
    """
    queryset = CustomUser.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [IsAdminRole] # Only Admins can manage users

class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom token view if you need to add more claims to the JWT payload.
    For now, it behaves like the default one.
    """
    # You can override the serializer_class here if needed
    pass