from django.shortcuts import render
from django.views.generic import TemplateView
from allauth.account.forms import LoginForm

# Create your views here.

# simply renders home.html for testing purposes
class Home(TemplateView):
    template_name = 'home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = LoginForm()
        return context
