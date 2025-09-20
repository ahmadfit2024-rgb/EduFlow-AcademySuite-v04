from django.contrib.auth import views as auth_views

class CustomLoginView(auth_views.LoginView):
    """
    Custom login view to use our branded login template.
    """
    template_name = 'login.html'
    redirect_authenticated_user = True

class CustomLogoutView(auth_views.LogoutView):
    """
    Custom logout view to redirect to the login page after logout.
    """
    next_page = 'login'