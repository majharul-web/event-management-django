from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django import forms 
from django.contrib.auth.models import Permission, Group
import re
from events.forms import StyledFormMixin
from django.contrib.auth import get_user_model
from users.models import CustomUser

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

class SignUpForm(UserCreationForm):
    class Meta:
        model = UserCreationForm.Meta.model
        fields = ('username','first_name', 'last_name', 'email', 'password', 'password2')

    def __init__(self, *args, **kwargs):
        super(UserCreationForm,self).__init__(*args, **kwargs)

        for field in self.fields.values():
            field.help_text= None

class SignUpModelForm(StyledFormMixin,forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'password', 'confirm_password', 'email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_exists = User.objects.filter(email=email).exists()

        if email_exists:
            raise forms.ValidationError("Email already exists")

        return email

    def clean_password1(self):
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