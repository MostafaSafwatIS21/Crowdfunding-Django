from django import forms
from .models import Project, Fund

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'details', 'total_target', 'start_time', 'end_time']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'details': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'w-full px-4 py-2 border rounded-md focus:outline-none focus:border-blue-600 focus:ring-1 focus:ring-blue-600',
            })

class FundForm(forms.ModelForm):
    class Meta:
        model = Fund
        fields = ['amount']
        widgets = {
            'amount': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:border-blue-600 focus:ring-1 focus:ring-blue-600',
                'placeholder': 'Amount (EGP)',
                'min': '0.01',
                'step': '0.01'
            })
        }
