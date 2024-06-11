from django import forms
from .models import Document, DockSignGroup
from django.contrib.auth.models import User

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['name', 'file']

class SignDocumentForm(forms.Form):
    documents = forms.ModelMultipleChoiceField(queryset=Document.objects.filter(status='не подписан'), widget=forms.CheckboxSelectMultiple)


class AddUserForm(forms.Form):
    username = forms.CharField(max_length=150, help_text="Enter the username of the user to add")

    def clean_username(self):
        username = self.cleaned_data['username']
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError("User does not exist")
        return username

class SignDocumentForm2(forms.ModelForm):
    class Meta:
        model = DockSignGroup
        fields = []

class DockSignGroupForm(forms.ModelForm):
    class Meta:
        model = DockSignGroup
        fields = ['document', 'users']