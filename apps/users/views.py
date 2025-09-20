# =================================================================
# apps/users/views.py
# -----------------------------------------------------------------
# KEEPS THE SYSTEM INTEGRATED: This file is completely refactored
# to support a full Single-Page Application (SPA) experience for
# user management using HTMX. It now handles requests for modals
# and partial updates, eliminating page reloads entirely.
# =================================================================

from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm

class UserManagementView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    """
    The main container view for the User Management SPA.
    Renders the main template which includes modals and the user list container.
    """
    template_name = 'users/user_management.html'

    def test_func(self):
        return self.request.user.role == CustomUser.Roles.ADMIN

class UserListView(LoginRequiredMixin, UserPassesTestMixin, View):
    """
    Handles rendering the list of users. Responds to initial loads
    and HTMX-powered search/filter requests by returning just the list partial.
    """
    def test_func(self):
        return self.request.user.role == CustomUser.Roles.ADMIN

    def get(self, request, *args, **kwargs):
        search_query = request.GET.get('q', '')
        users = CustomUser.objects.all().order_by('full_name')
        if search_query:
            users = users.filter(
                Q(username__icontains=search_query) |
                Q(full_name__icontains=search_query) |
                Q(email__icontains=search_query)
            )
        context = {
            'users': users,
            'search_query': search_query,
            'is_search': bool(search_query)
        }
        return render(request, 'partials/_user_list.html', context)

class UserFormView(LoginRequiredMixin, UserPassesTestMixin, View):
    """
    Handles both creating (GET/POST) and updating (GET/POST) users.
    It intelligently returns the form partial to be rendered in a modal.
    """
    def test_func(self):
        return self.request.user.role == CustomUser.Roles.ADMIN

    def get(self, request, pk=None):
        if pk:
            user = get_object_or_404(CustomUser, pk=pk)
            form = CustomUserChangeForm(instance=user)
            context = {'form': form, 'user': user, 'title': 'Edit User'}
        else:
            form = CustomUserCreationForm()
            context = {'form': form, 'title': 'Add New User'}
        return render(request, 'users/_user_form.html', context)

    def post(self, request, pk=None):
        user = get_object_or_404(CustomUser, pk=pk) if pk else None
        form = CustomUserChangeForm(request.POST, instance=user) if user else CustomUserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            response = HttpResponse()
            response['HX-Trigger'] = 'userListChanged' # Trigger event to refresh list
            return response
        
        # If form is invalid, re-render the form with errors
        context = {'form': form, 'user': user}
        return render(request, 'users/_user_form.html', context)

class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, View):
    """
    Handles the deletion of a user and returns an HX-Trigger to refresh the list.
    """
    def test_func(self):
        return self.request.user.role == CustomUser.Roles.ADMIN

    def post(self, request, pk):
        user = get_object_or_404(CustomUser, pk=pk)
        user.delete()
        response = HttpResponse()
        response['HX-Trigger'] = 'userListChanged' # Trigger event to refresh list
        return response