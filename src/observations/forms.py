from django import forms
from django.utils import timezone
from .models import ObservingSession


class ObservingSessionForm(forms.ModelForm):
    class Meta:
        model = ObservingSession
        fields = ("datetime_start_ut", "datetime_end_ut", "site_name")
        # provides user with intuitive date/time picker that isn't user time zone biased
        widgets = {
            'datetime_start_ut': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'datetime_end_ut': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set default start time to current UTC time for new sessions
        if not self.instance.pk:
            self.fields['datetime_start_ut'].initial = timezone.now()