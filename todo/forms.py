from django import forms
from .models import Todo

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'description', 'deadline']
        widgets = {
            'deadline': forms.DateInput(format=('%Y-%m-%d'), attrs={'type': 'date'}),
        }