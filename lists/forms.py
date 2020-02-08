from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import List, School
from django.forms.widgets import SelectDateWidget


class ListForm(ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(ListForm, self).__init__(*args, **kwargs)
        #self.fields['school'] = forms.ChoiceField(label='Escuela', choices=self.List.school)
        #self.fields['school'].label_from_instance = "Escuela"
    
    name = forms.CharField(label='Nombre de la lista', max_length=100, required=True)
    school = forms.ModelChoiceField(queryset=School.objects, empty_label="Eliga una escuela", label="Escuela", required=False)

    class Meta:
        model = List
        exclude = ["user"]
        fields = ('name', 'school', 'status')


class ListFormAllLists(ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(ListFormAllLists, self).__init__(*args, **kwargs)
        #self.fields['school'] = forms.ChoiceField(label='Escuela', choices=self.List.school)
        #self.fields['school'].label_from_instance = "Escuela"
    
    name = forms.CharField(label='Nombre de la lista', max_length=100, required=True)
    #school = forms.ModelChoiceField(queryset=School.objects, empty_label="Eliga una escuela", label="Escuela", required=False)

    class Meta:
        model = List
        exclude = ('user', 'school')
        fields = ('name',)        

