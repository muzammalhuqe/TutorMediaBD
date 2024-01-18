from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import UserAccount

class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'id' : 'required'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'id' : 'required'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'id' : 'required'}))
    ssc_roll = forms.CharField(widget=forms.TextInput(attrs={'id' : 'required'}))
    ssc_gpa = forms.CharField(widget=forms.TextInput(attrs={'id' : 'required'}))
    hsc_roll = forms.CharField(widget=forms.TextInput(attrs={'id' : 'required'}))
    hsc_gpa = forms.CharField(widget=forms.TextInput(attrs={'id' : 'required'}))
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email','ssc_roll','ssc_gpa','hsc_roll','hsc_gpa','password1', 'password2']
        
    def save(self, commit = True):
        our_user = super().save(commit=False)
        if commit == True:
            our_user.save()
            ssc_roll = self.cleaned_data.get('ssc_roll')
            ssc_gpa = self.cleaned_data.get('ssc_gpa')
            hsc_roll = self.cleaned_data.get('hsc_roll')
            hsc_gpa = self.cleaned_data.get('hsc_gpa')

            UserAccount.objects.create(
                user = our_user,
                ssc_roll = ssc_roll,
                ssc_gpa = ssc_gpa,
                hsc_roll = hsc_roll,
                hsc_gpa = hsc_gpa,
            )
            return our_user
        
        username = self.cleaned_data['username']
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        email = self.cleaned_data['email']
        password = self.cleaned_data['password1']

        account = User(username = username, email=email, first_name = first_name, last_name = last_name)
        print(account)
        account.set_password(password)
        account.is_active = False
        account.save()
        return account
    

class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'id' : 'required'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'id' : 'required'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'id' : 'required'}))
    ssc_roll = forms.CharField(widget=forms.TextInput(attrs={'id' : 'required'}))
    ssc_gpa = forms.CharField(widget=forms.TextInput(attrs={'id' : 'required'}))
    hsc_roll = forms.CharField(widget=forms.TextInput(attrs={'id' : 'required'}))
    hsc_gpa = forms.CharField(widget=forms.TextInput(attrs={'id' : 'required'}))
    password = None
    class Meta:
        model = User
        # fields = '__all__'
        fields = ['first_name','last_name','email','ssc_roll','ssc_gpa','hsc_roll','hsc_gpa']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # for field in self.fields:
        #     self.fields[field].widget.attrs.update({
        #         'class': (
        #             'appearance-none block w-full bg-gray-200 '
        #             'text-gray-700 border border-gray-200 rounded '
        #             'py-3 px-4 leading-tight focus:outline-none '
        #             'focus:bg-white focus:border-gray-500'
        #         )
        #     })
        # jodi user er account thake 
        if self.instance:
            try:
                user_account = self.instance.account
            except UserAccount.DoesNotExist:
                user_account = None

            if user_account:
                self.fields['ssc_roll'].initial = user_account.ssc_roll
                self.fields['ssc_gpa'].initial = user_account.ssc_gpa
                self.fields['hsc_roll'].initial = user_account.hsc_roll
                self.fields['hsc_gpa'].initial = user_account.hsc_gpa
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit == True:
            user.save()
            user_account, created = UserAccount.objects.get_or_create(user=user)
            user_account.ssc_roll = self.cleaned_data['ssc_roll']
            user_account.ssc_gpa = self.cleaned_data['ssc_gpa']
            user_account.hsc_roll = self.cleaned_data['hsc_roll']
            user_account.hsc_gpa = self.cleaned_data['hsc_gpa']
            user_account.save()
        return user
