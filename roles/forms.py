from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms.utils import ValidationError
from django.forms import ModelForm
from django.forms.widgets import SelectDateWidget
from roles.models import User, Profile
from django.http import Http404


class SellerSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    error_messages = {
        'password_mismatch': "Las contraseñas no coinciden.",
    }

    first_name = forms.CharField(label="Nombre", max_length=100, required=True)
    last_name = forms.CharField(label='Apellido', max_length=100, required=True)
    username = forms.CharField(label='Nombre de usuario', max_length=100, required=True,
                               error_messages={'invalid': "Error con el nombre de usuario."})
    email = forms.EmailField(label='Correo electrónico', max_length=60, required=True)
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(SellerSignUpForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )    

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_seller = True
        if commit:
            user.save()
        return user


class ClientSignUpForm(UserCreationForm):
    
    class Meta(UserCreationForm.Meta):
        model = User
    
    error_messages = {
        'password_mismatch': "Las contraseñas no coinciden.",
    }

    first_name = forms.CharField(label="Nombre", max_length=100, required=False)
    last_name = forms.CharField(label='Apellido', max_length=100, required=False)
    username = forms.CharField(label='Nombre de usuario', max_length=100, required=True,
                               error_messages={'invalid': "Error in username"})
    email = forms.EmailField(label='E-mail', max_length=60, required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput)
    
    def __init__(self, *args, **kwargs):
        super(ClientSignUpForm, self).__init__(*args, **kwargs)
        
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Ingresa el usuario que desees'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Ingresa tu nombre'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Ingresa tu apellido'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Ingresa tu E-mail'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Ingresa tu contraseña'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Re-Ingresa tu contraseña'})

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )

    @transaction.atomic 
    def save(self):
        user = super().save(commit=False)
        user.is_client = True
        user.email = self.cleaned_data.get("email")
        user.save()
        return user



#####################


class ProfileForm(ModelForm):
    MONTHS = {
        1:'ene', 2:'feb', 3:'mar', 4:'abr',
        5:'may', 6:'jun', 7:'jul', 8:'ago',
        9:'set', 10:'oct', 11:'nov', 12:'dic'
    }
    
    birthdate = forms.DateField(label='Fecha de nacimiento', widget=SelectDateWidget(years=range(1950, 2012), months=MONTHS))
    cedula_ruc = forms.CharField(label='Cédula', max_length=100, required=True)
    mobile = forms.CharField(label='Celular')
    telephone = forms.CharField(label='Teléfono', required=False)
    address = forms.CharField(label='Dirección', max_length=100, required=True)
    address_reference = forms.CharField(label='Referencia (opcional)', max_length=100, required=False)
    location = forms.CharField(label='Locación', max_length=100, required=False)
    shipping_address = forms.CharField(widget=forms.Textarea(attrs={'rows':4, 'cols':15}), label='Dirección de envío', max_length=100, required=True)    

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)        
        self.fields['cedula_ruc'].widget.attrs.update({'class': 'form-control','placeholder': 'Ingrese su cedula'})        
        self.fields['mobile'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Número de Celular'})
        self.fields['mobile'].label = "Telefono Celular"
        self.fields['telephone'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Número de Telefono'})        
        self.fields['address'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Direccion'})        
        self.fields['address_reference'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Direccion Referencial (Opcional)'})        
        self.fields['shipping_address'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Direccion De envio'})        
        
        
    class Meta:
        model = Profile
        fields = ('cedula_ruc', 'mobile','telephone', 'birthdate', 'address', 'address_reference',
                  'location', 'shipping_address')
