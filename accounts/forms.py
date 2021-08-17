from django.contrib.auth.forms import UserCreationForm, UsernameField, PasswordResetForm
from django.core.validators import validate_email
from django.forms.widgets import TextInput


class SignupForm(UserCreationForm):
    # 각 필드에 대한 validators, clean_필드명, clean(멤버함수)
    # https://github.com/django/django/blob/main/django/contrib/auth/models.py#L321

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields["username"] 는 아래와 같음
        # <django.contrib.auth.forms.UsernameField object at 0x11009b220>
        # <django.contrib.auth.forms.UsernameField object at 0x11009b220>
        # self.fields["username"].__dict__
        # special variables:
        # function variables:
        # 'max_length': 150
        # 'min_length': None
        # 'strip': True
        # 'empty_value': ''
        # 'required': True
        # 'label': 'Username'
        # 'initial': None
        # 'show_hidden_initial': False
        # 'help_text': 'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'
        # 'disabled': False
        # 'label_suffix': None
        # 'localize': False
        # 'widget': <django.forms.widgets.TextInput object at 0x11009bc40>
        # 'error_messages': {'required': 'This field is required.'}
        # 'validators': [<django.core.validat...10f460220>]
        # len(): 15

        self.fields["username"].validators = [validate_email]
        self.fields["username"].help_text = "Enter Email Format"
        self.fields["username"].label = "Email"
        # self.fields["username"].widget = TextInput(attrs={"autofocus": True})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = user.username
        if commit:
            user.save()
        return user

    # # clean_필드명으로 유효성 검사한 방식
    # def clean_username(self):
    #     value = self.cleaned_data.get("username")
    #     if value:
    #         validate_email(value)
    #     return value


# class TestForm(PasswordResetForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)

#     def save(self, *args, **kwargs):
#         if self.title == "Using E-mail":
#             super().save(*args, **kwargs)
#         else:
#             return
