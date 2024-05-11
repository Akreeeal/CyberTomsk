from django import forms

class AvailabilityForm(forms.Form):
    start_session = forms.DateTimeField(
        label='Дата и время',
        input_formats=["%Y-%m-%dT%H:%M"],  # Формат даты и времени
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'date-input'}),
        required=True
    )
    hours = forms.IntegerField(label='Выберите продолжительность (часы)')

    # Предоставьте метод clean_hours для проверки значения hours
    def clean_hours(self):
        hours = self.cleaned_data['hours']
        if hours not in [1, 3, 8]:
            raise forms.ValidationError("Выберите продолжительность из доступных вариантов: 1, 3, 8 часов")
        return hours

