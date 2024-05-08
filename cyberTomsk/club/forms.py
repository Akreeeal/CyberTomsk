from django import forms

class AvailabilityForm(forms.Form):
    start_session = forms.DateTimeField(required=True, input_formats=["%Y-$m-%dT%H:%M"], label= "Дата и время")
    hours = forms.IntegerField(label='Количество часов')

