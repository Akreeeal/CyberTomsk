from django import forms

class AvailabilityForm(forms.Form):
    PC_CATEGORIES = (
        ('VIP', 'VIP'),
        ('NVIP', 'NON_VIP'),
        ('BC', 'BOOT_CAMP')
    )
    pc_category = forms.ChoiceField(choices=PC_CATEGORIES, required=True)
    start_session = forms.DateTimeField(required=True, input_formats=["%Y-$m-%dT%H:%M"], )
    stop_session = forms.DateTimeField(required=True, input_formats=["%Y-$m-%dT%H:%M"], )

