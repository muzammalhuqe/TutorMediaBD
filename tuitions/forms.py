from django import forms
from .models import Tution, TutionDetails,TuitionApplication, Comment

class CategoryForm(forms.ModelForm):
    class Meta: 
        model = Tution
        fields = '__all__'

class AddBookForm(forms.ModelForm):
    class Meta: 
        model = TutionDetails
        fields = '__all__'


class TuitionApplicationForm(forms.ModelForm):
    class Meta:
        model = TuitionApplication
        fields = ['applicant']


class CommentForm(forms.ModelForm):
    class Meta: 
        model = Comment
        fields = ['name', 'email', 'body']