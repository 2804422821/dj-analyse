from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):
    password = forms.CharField()
    password_confirm = forms.CharField()

    class Meta:
        model = User
        fields = ("username", "email")

    def clean_password_confirm(self):
        clean_data = self.cleaned_data
        if clean_data["password"] != clean_data["password_confirm"]:
            raise forms.ValidationError("两次密码不一致")
        return clean_data["password_confirm"]
