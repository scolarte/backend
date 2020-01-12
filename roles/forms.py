from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms.utils import ValidationError
from django.forms import ModelForm
from django.forms.widgets import SelectDateWidget
from roles.models import User, Profile


class SellerSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    error_messages = {
        'password_mismatch': "Las contraseñas no coinciden.",
    }

    first_name = forms.CharField(label="Nombre", max_length=100, required=True)
    last_name = forms.CharField(label='Apellido', max_length=100, required=True)
    username = forms.CharField(label='Nombre de usuario', max_length=100, required=True,
                               error_messages={'invalid': "you custom error message"})
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

    first_name = forms.CharField(label="Nombre", max_length=100, required=True)
    last_name = forms.CharField(label='Apellido', max_length=100, required=True)
    username = forms.CharField(label='Nombre de usuario', max_length=100, required=True,
                               error_messages={'invalid': "you custom error message"})
    email = forms.EmailField(label='Correo electrónico', max_length=60, required=True)
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(ClientSignUpForm, self).__init__(*args, **kwargs)

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


    @transaction.atomic #llama a otro modelo
    def save(self):
        user = super().save(commit=False)
        user.is_client = True
        #user.is_client = True
        user.save()
        # student = Student.objects.create(user=user)
        # student.interests.add(*self.cleaned_data.get('interests'))
        return user



#####################


class ProfileForm(ModelForm):
    MONTHS = {
        1:'ene', 2:'feb', 3:'mar', 4:'abr',
        5:'may', 6:'jun', 7:'jul', 8:'ago',
        9:'set', 10:'oct', 11:'nov', 12:'dic'
    }

    def __init__(self, provincias_list, cantones_list, parroquias_list, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['shipping_provincia'] = forms.ChoiceField(label='Provincia', choices=tuple([(name, name) for name in provincias_list]))
        self.fields['shipping_canton'] = forms.ChoiceField(label='Cantón', choices=tuple([(name, name) for name in cantones_list]))
        self.fields['shipping_parroquia'] = forms.ChoiceField(label='Parroquia', choices=tuple([(name, name) for name in parroquias_list]))


    birthdate = forms.DateField(label='Fecha de nacimiento', widget=SelectDateWidget(years=range(1950, 2012), months=MONTHS))
    cedula_ruc = forms.CharField(label='Cédula', max_length=100, required=True)
    mobile = forms.CharField(label='Celular')
    telephone = forms.CharField(label='Teléfono')
    address = forms.CharField(label='Dirección', max_length=100, required=True)
    address_reference = forms.CharField(label='Referencia (opcional)', max_length=100, required=False)
    location = forms.CharField(label='Locación', max_length=100, required=False)
    shipping_address = forms.CharField(label='Dirección de envío', max_length=100, required=True)
    shipping_provincia = forms.CharField(label='Provincia', max_length=100, required=True)
    shipping_canton = forms.CharField(label='Cantón', max_length=100, required=True)
    shipping_parroquia = forms.CharField(label='Parroquia', max_length=100, required=True)

    class Meta:
        model = Profile
        fields = ('cedula_ruc', 'mobile','telephone', 'birthdate', 'address', 'address_reference',
                  'location', 'shipping_address', 'shipping_provincia', 'shipping_canton', 'shipping_parroquia')