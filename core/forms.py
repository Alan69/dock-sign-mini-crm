from django import forms
from .models import Document

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['name', 'file']

class SignDocumentForm(forms.Form):
    documents = forms.ModelMultipleChoiceField(queryset=Document.objects.filter(status='не подписан'), widget=forms.CheckboxSelectMultiple)