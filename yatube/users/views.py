from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import CreationForm


class SignUp(CreateView):
    """View class for the registration page template."""
    form_class = CreationForm
    success_url = reverse_lazy('signup')
    template_name = 'users/signup.html'
