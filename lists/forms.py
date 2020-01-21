from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import List
from django.forms.widgets import SelectDateWidget


class ListForm(ModelForm):
    
    def __init__(self, lista_de_listas, *args, **kwargs):
        super(ListForm, self).__init__(*args, **kwargs)
        self.fields['name'] = forms.ChoiceField(label='Lista', choices=tuple([(name, name) for name in lista_de_listas]))
       
    class Meta:
        model = List
        fields = ('name',)