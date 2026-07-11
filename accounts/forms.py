from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'mobile_phone')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'w-full px-4 py-2 border rounded-md focus:outline-none focus:border-blue-600 focus:ring-1 focus:ring-blue-600'
            })

class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={
        'autofocus': True,
        'class': 'w-full px-4 py-2 border rounded-md focus:outline-none focus:border-blue-600 focus:ring-1 focus:ring-blue-600',
        'placeholder': 'Email address'
    }))
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'current-password',
            'class': 'w-full px-4 py-2 border rounded-md focus:outline-none focus:border-blue-600 focus:ring-1 focus:ring-blue-600',
            'placeholder': 'Password'
        }),
    )
