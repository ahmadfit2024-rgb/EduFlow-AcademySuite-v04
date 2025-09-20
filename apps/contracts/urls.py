from django.urls import path
from .views import ExportContractReportView

app_name = 'contracts'

urlpatterns = [
    path('<str:pk>/export/', ExportContractReportView.as_view(), name='export_contract_report'),
]