from django import forms
from django.contrib.auth import get_user_model
from captcha.fields import ReCaptchaField


from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.forms import SetPasswordForm

User = get_user_model()


class RegisterForm(UserCreationForm):
    """
    The default

    """

    username = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
                "placeholder": " ",
                "autocomplete": False,
            }
        ),
        label="Username",
        required=True,
    )

    country = forms.CharField(
        max_length=50,
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
                "placeholder": "country",
                "autocomplete": False,
            }
        ),
        label="country",
        required=True,
    )

    phone = forms.CharField(
        max_length=50,
        widget=forms.TextInput(
            attrs={
                "type": "tel",
                "class": "form-control form--control checkUser",
                "placeholder": "mobile",
                "autocomplete": False,
            }
        ),
        label="",
        required=True,
    )

    mobile_code = forms.CharField(
        max_length=50,
        widget=forms.TextInput(
            attrs={
                "type": "hidden",
                "name": "mobile_code",
            }
        ),
        required=True,
    )

    email = forms.EmailField(
        max_length=80,
        widget=forms.TextInput(
            attrs={
                "type": "email",
                "class": "form-control",
                "placeholder": "Email",
                "autocomplete": False,
            }
        ),
        label="Email",
        required=True,
    )

    password1 = forms.CharField(
        max_length=10,
        min_length=6,
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control",
                "autocomplete": False,
            }
        ),
    )
    password2 = forms.CharField(
        max_length=10,
        min_length=6,
        label="Confirm Password",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Confirm Password",
                "class": "form-control",
                "autocomplete": False,
            }
        ),
    )

    captcha = ReCaptchaField()

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "country",
            "mobile_code",
            "phone",
            "password1",
            "password2",
            "captcha",
        ]

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)

        # Add custom logic here, for example, setting additional user attributes
        user.phone = f"{self.cleaned_data['mobile_code']}{self.cleaned_data['phone']}"

        if commit:
            user.save()
        return user


class LoginForm(forms.ModelForm):
    email = forms.EmailField(
        max_length=80,
        widget=forms.TextInput(
            attrs={"type": "email", "class": "form-control", "placeholder": "Email"}
        ),
        label="Email",
        required=True,
    )
    password = forms.CharField(
        max_length=10,
        min_length=6,
        label="",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control",
            }
        ),
    )

    captcha = ReCaptchaField()

    class Meta:
        model = User
        fields = ("email", "password", "captcha")

    def clean(self):
        if self.is_valid():
            if not authenticate(
                email=self.cleaned_data["email"], password=self.cleaned_data["password"]
            ):
                raise forms.ValidationError("Invalid Email or Password")


class SetPasswordForm(SetPasswordForm):
    class Meta:
        model = get_user_model()
        fields = ["new_password1", "new_password2"]
