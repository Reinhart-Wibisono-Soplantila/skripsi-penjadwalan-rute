from django import forms
from app_schedules.models import ScheduleOutlet

class StatusForm(forms.ModelForm):
    StatusChoices=(
        ('Finish', 'Finish'),
        ('On Progress', 'On Progress'),
    )
    Status = forms.ChoiceField(
        choices=StatusChoices,
        required=False,
        widget=forms.Select(
            attrs={
                'class' :'form-select form-control'
            }
        )
    )
    class Meta:
        model=ScheduleOutlet
        fields = [
            'Status',
        ]