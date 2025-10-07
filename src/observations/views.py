from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib import messages
from .forms import ObservingSessionForm
from allauth.account.forms import LoginForm


# renders home.html with observing session form if user is authenticated, login form if not
class Home(TemplateView):
    template_name = 'observations/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Only show the observing sessions form if user is logged in
        if self.request.user.is_authenticated:
            context['observing_session_form'] = ObservingSessionForm()
        else:
            context['login_form'] = LoginForm()
            
        return context
    
    def post(self, request, **kwargs):
        # Only handle POST if user is authenticated
        if not request.user.is_authenticated:
            messages.warning(request, 'You must be logged in to create an observation.')
            return redirect('home')
        
        form = ObservingSessionForm(request.POST)
        if form.is_valid():
            # Save the form with the current user
            observing_session = form.save(commit=False)
            observing_session.user = request.user
            observing_session.save()
            messages.success(request, 'New observing session created successfully! Click the "My Observations" link at the top of the page, to add observations to this session.')
            return redirect('home')
        else:
            # If form is invalid, redisplay with errors
            messages.error(request, 'Please correct the errors below and try again.')
            # ensures nothing is missing from the template context
            context = self.get_context_data(**kwargs)
            # displays again the users invalid input on form
            context['observing_session_form'] = form
            # renders the template_name with above context
            return self.render_to_response(context)