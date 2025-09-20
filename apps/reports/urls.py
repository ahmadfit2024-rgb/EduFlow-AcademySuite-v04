from django.urls import path
from .views import ReportDashboardView

urlpatterns = [
    path('', ReportDashboardView.as_view(), name='report_dashboard'),
]