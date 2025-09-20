from django.urls import path
from .views.authentication import CustomLoginView, CustomLogoutView
from .views.dashboards import DashboardView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    
    # The root path will redirect to the dashboard if logged in, or login page if not
    path('', DashboardView.as_view(), name='home'), 
]