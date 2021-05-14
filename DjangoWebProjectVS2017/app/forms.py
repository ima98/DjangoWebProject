"""
Definition of forms.
"""

from django import forms
from app.models import Question2,Choice2,User2
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _

class QuestionForm(forms.ModelForm):

        class Meta:
            model = Question2
            fields = ('question_text','subject', 'numChoices',)

class ChoiceForm(forms.ModelForm):

        class Meta:
            model = Choice2
            fields = ('choice_text','isCorrect',)

class UserForm(forms.ModelForm):

        class Meta:
            model = User2
            fields = ('email','nombre',)

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))
