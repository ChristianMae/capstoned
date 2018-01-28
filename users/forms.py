from django import forms
from users.models import User
from django.contrib.auth import authenticate


class UserRegisterForm(forms.ModelForm):
    error_messages = {'password_mismatch':("The two password fields didn't match."), }
    
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder':('Email'),}))
    first_name = forms.CharField(label=("First Name"), min_length=2, widget=forms.TextInput(attrs={'placeholder':('First Name')}))
    last_name = forms.CharField(label=("Last Name"), min_length=2, widget=forms.TextInput(attrs={'placeholder':('Last Name'),}))
    school = forms.CharField(label=("School"), min_length=2, widget=forms.TextInput(attrs={'placeholder':('School'),}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'minLength': 8, 'placeholder':('Password'),}), required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'minLength':8, 'placeholder':('Retype Password'),}), required=True)


    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'school', 'password', 'confirm_password')


    def clean(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password  !=  confirm_password:
            raise forms.ValidationError('Password doesn\'t match.')
        return self.cleaned_data


    def clean_email(self):
        email = self.cleaned_data.get('email')
        email = email.lower()
        try:
            match = User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError('This email is already taken.')


    def save(self, commit=True):
        instance = super(UserRegisterForm, self).save(commit=False)
        if commit:
            instance.set_password(self.data['password'])
            instance.save()
        return instance


class LoginForm(forms.Form):

    user_cache = None

    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        email = self.cleaned_data.get('email')
        email = email.lower()
        password = self.cleaned_data.get('password')

        user = authenticate(email=email, password=password)
        if not user:
            raise forms.ValidationError('Invalid Email or Password.')
        else: 
            self.user_cache=user

        user = User.objects.filter(email=email).first()
        if user.is_confirmed == False:
            raise forms.ValidationError('Email Address is not verified.')

        return self.cleaned_data












