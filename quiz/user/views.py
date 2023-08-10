
from django.views import generic
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from .forms import SignUpForm



class UserRegisterView(generic.CreateView):
    form_class = SignUpForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')



class HomePageView(TemplateView):
    template_name = 'home.html'



