# =================================================================
# apps/users/urls.py
# -----------------------------------------------------------------
# KEEPS THE SYSTEM INTEGRATED: URLs are updated to support the new
# SPA-like functionality. Separate endpoints are now defined for the
# main page, the user list partial, and the form views (add/edit/delete).
# =================================================================

from django.urls import path
from .views import UserManagementView, UserListView, UserFormView, UserDeleteView

app_name = 'users'

urlpatterns = [
    # The main page that holds the SPA container
    path('manage/', UserManagementView.as_view(), name='user_management'),
    
    # URL to fetch the user list (for initial load and search)
    path('list/', UserListView.as_view(), name='user_list'),

    # URLs for the user form (modal)
    path('add/', UserFormView.as_view(), name='user_add'),
    path('<int:pk>/edit/', UserFormView.as_view(), name='user_edit'),
    
    # URL for deleting a user
    path('<int:pk>/delete/', UserDeleteView.as_view(), name='user_delete'),
]