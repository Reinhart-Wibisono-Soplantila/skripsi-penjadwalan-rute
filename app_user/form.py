from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError
from django.contrib.auth.models import Group, Permission

class ProfileForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['username', 'email']
        widgets={
            'username':forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'email':forms.EmailInput(
                attrs={
                    'class':'form-control'
                }
            )
        } 
        labels={
            'username':'Username',
            'email' : 'Email'
        }
        help_texts = {
            'username': '',
        }

class UpdateForm(forms.ModelForm):
    email=forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    group = forms.ModelChoiceField(
        queryset=Group.objects.all(),  # Ambil semua grup
        label="Select Group",  # Label yang ditampilkan
        empty_label=None,  # Hilangkan pilihan kosong ('-----')
        widget=forms.Select(
            attrs={
                'class' :'form-select form-control'
            }
        )
    )
    class Meta:
        model=User
        fields=['username', 'email', 'group']
        widgets = {
            'username': forms.TextInput(
                attrs = {
                    'class' : 'form-control',
                }
            )
        }
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError("Email already exists.")
        return email
    
    def clean_username(self):
        username= self.cleaned_data.get('username')
        if User.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            raise ValidationError("Username already exists.")
        return username
    
    def __init__(self, *args, **kwargs):
        # Ambil user_id dari kwargs
        self.user_id = kwargs.pop('user_id', None)
        super().__init__(*args, **kwargs)
        if self.instance.pk:  # Jika instance sudah ada (user yang ada)
            # Mengatur initial value berdasarkan grup user
            if self.instance.groups.exists():
                self.fields['group'].initial = self.instance.groups.first()  # Ambil grup pertama
    

class RegisterForm(UserCreationForm):
    email=forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class':'form-control'}))
    group = forms.ModelChoiceField(
        queryset=Group.objects.all(),  # Ambil semua grup
        required=True,  # Set sebagai field yang harus diisi
        label="Select Group",  # Label yang ditampilkan
        empty_label=None,  # Hilangkan pilihan kosong ('-----')
        initial=Group.objects.get(name="Admin"),  # Set default value ke grup "admin"
        widget=forms.Select(
            attrs={
                'class' :'form-select form-control'
            }
        )
    )
    password1=forms.CharField(
        label='Password',
        widget=forms.PasswordInput(
            attrs={
                'class':'form-control', 
                }))
    password2=forms.CharField(
        label='Confirmation Password',
        widget=forms.PasswordInput(
            attrs={
                'class':'form-control', 
                }))
    class Meta:
        model=User
        fields=['username', 'email', 'group', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(
                attrs = {
                    'class' : 'form-control',
                }
            )
        }
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError("Email already exists.")
        return email
             
class LoginForm(AuthenticationForm):
    username=forms.CharField(
        label='Username', widget=forms.TextInput(
            attrs={
                'placeholder' : 'Username'
            }
        )
    )
    password=forms.CharField(
        label='Password', widget=forms.PasswordInput(
            attrs={
                'placeholder' : 'Password'
            }
        )
    )
    
class MyPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(MyPasswordChangeForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label