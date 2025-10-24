from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django import forms 
from django.contrib.auth.models import Permission, Group
import re
from events.forms import StyledFormMixin
from django.contrib.auth import get_user_model
from users.models import CustomUser
from django.contrib.auth.forms import PasswordChangeForm,PasswordResetForm,SetPasswordForm
from django.core.exceptions import ValidationError

User = get_user_model()

class StyledFormMixinA:
    """ Mixing to apply style to form field"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styled_widgets()

    default_classes = "border border-primary w-full px-4 py-2 rounded-lg shadow-sm ring-primary focus:outline-none focus:ring-2 focus:ring-opacity-50"

    def apply_styled_widgets(self):
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({
                    'class': 'form-input-guest',
                    'placeholder': f"Enter {field.label.lower()}"
                })
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                    'class': 'form-input-guest resize-none',
                    'placeholder':  f"Enter {field.label.lower()}",
                    'rows': 5
                })
            elif isinstance(field.widget, forms.SelectDateWidget):          
                field.widget.attrs.update({
                    'class': 'border border-primary w-full px-4 py-2 rounded-lg shadow-sm ring-primary focus:outline-none focus:ring-2 focus:ring-opacity-50 mb-4',
                })
            elif isinstance(field.widget, forms.TimeInput):  
                field.widget.attrs.update({
                    'class': 'form-input-guest',
                })
            elif isinstance(field.widget, forms.CheckboxSelectMultiple):                
                field.widget.attrs.update({
                    'class': "space-y-2 "
                })
            else:
                field.widget.attrs.update({
                    'class': 'form-input-guest',
                })

class SignUpModelForm(StyledFormMixin,forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username','email', 'first_name', 'last_name',
                  'password', 'confirm_password', ]

    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_exists = User.objects.filter(email=email).exists()

        if email_exists:
            raise forms.ValidationError("Email already exists")

        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        errors = []

        if len(password) < 8:
            errors.append('Password must be at least 8 character long')

        if not re.search(r'[A-Z]', password):
            errors.append(
                'Password must include at least one uppercase letter.')

        if not re.search(r'[a-z]', password):
            errors.append(
                'Password must include at least one lowercase letter.')

        if not re.search(r'[0-9]', password):
            errors.append('Password must include at least one number.')

        if not re.search(r'[@#$%^&+=]', password):
            errors.append(
                'Password must include at least one special character.')

        if errors:
            raise forms.ValidationError(errors)

        return password

    def clean(self):  # non field error
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Password do not match")

        return cleaned_data

class SignInModelForm(StyledFormMixin,AuthenticationForm, ):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
class AssignRoleForm(StyledFormMixin,forms.Form):
    
    role = forms.ModelChoiceField(
        queryset= Group.objects.all(),
        empty_label="Select Role",
    )

class CreateGroupForm(StyledFormMixin,forms.ModelForm):
    permissions= forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Permissions"
    )
    class Meta:
        model = Group
        fields = ['name', 'permissions']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Group.objects.filter(name=name).exists():
            raise forms.ValidationError("Group with this name already exists.")
        return name
 
class EditProfileForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'phone_number', 'profile_image']
    
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if not re.fullmatch(r'01[0-9]{9}', phone_number):
            raise ValidationError("Enter a valid 11-digit Bangladeshi phone number starting with '01'.")

        return phone_number


class CustomPasswordChangeForm(StyledFormMixin, PasswordChangeForm):
    pass
class CustomPasswordResetForm(StyledFormMixin, PasswordResetForm):
    pass

class CustomPasswordResetConfirmForm(StyledFormMixin, SetPasswordForm):
    pass

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, label="Your Name", widget=forms.TextInput(attrs={
        'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-primary-400 outline-none'
    }))
    email = forms.EmailField(label="Your Email", widget=forms.EmailInput(attrs={
        'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-primary-400 outline-none'
    }))
    message = forms.CharField(label="Message", widget=forms.Textarea(attrs={
        'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-primary-400 outline-none h-28 resize-none'
    }))