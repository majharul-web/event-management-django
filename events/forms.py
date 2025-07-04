from django import forms
from .models import Category, Event, Participant
from datetime import date,datetime

class StyledFormMixin:
    """ Mixing to apply style to form field"""

    default_classes = "border border-primary w-full px-4 py-2 rounded-lg shadow-sm ring-primary focus:outline-none focus:ring-2 focus:ring-opacity-50"

    def apply_styled_widgets(self):
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                print("Inside TextInput")
                field.widget.attrs.update({
                    'class': self.default_classes,
                    'placeholder': f"Enter {field.label.lower()}"
                })
            elif isinstance(field.widget, forms.Textarea):
                print("Inside Textarea")
                field.widget.attrs.update({
                    'class': f"{self.default_classes} resize-none",
                    'placeholder':  f"Enter {field.label.lower()}",
                    'rows': 5
                })
            elif isinstance(field.widget, forms.SelectDateWidget):
                print("Inside Date")
                field.widget.attrs.update({
                    'class': 'border border-primary px-4 py-2 rounded-lg shadow-sm ring-rose-500 focus:outline-none focus:ring-2 focus:ring-opacity-50',
                })
            elif isinstance(field.widget, forms.TimeInput):
                print("Inside Time")
                field.widget.attrs.update({
                    'class': self.default_classes,
                })
            elif isinstance(field.widget, forms.CheckboxSelectMultiple):
                print("Inside checkbox")
                field.widget.attrs.update({
                    'class': "space-y-2 "
                })
            else:
                print("Inside else")
                field.widget.attrs.update({
                    'class': self.default_classes
                })


class CategoryForm(forms.ModelForm, StyledFormMixin):
    class Meta:
        model = Category
        fields = ['name', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styled_widgets()


class EventForm(forms.ModelForm, StyledFormMixin):
    class Meta:
        model = Event
        fields = ['name', 'description', 'date', 'time', 'location', 'category']
        widgets = {
            'date': forms.SelectDateWidget(years=range(date.today().year, date.today().year + 5)),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styled_widgets()

        self.fields['category'].empty_label = "Select Category"
        
        if not self.initial.get('time'):
            now = datetime.now().strftime('%H:%M')
            self.fields['time'].initial = now
    


class ParticipantForm(forms.ModelForm, StyledFormMixin):
    class Meta:
        model = Participant
        fields = '__all__'
        widgets = {
            'event': forms.CheckboxSelectMultiple()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styled_widgets()
