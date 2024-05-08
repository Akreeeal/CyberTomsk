from django import forms

class AvailabilityForm(forms.Form):
    start_session = forms.DateTimeField(required=True, input_formats=["%Y-$m-%dT%H:%M"], )
    stop_session = forms.DateTimeField(required=True, input_formats=["%Y-$m-%dT%H:%M"], )

