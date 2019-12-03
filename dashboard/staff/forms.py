from django import forms
from account.models import User

class StaffForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['email', 'is_staff', 'is_active']
