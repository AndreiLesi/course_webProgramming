from django import forms

class newEntryForm(forms.Form):
    title = forms.CharField(label="Entry Title")
    description = forms.CharField(label="Description", widget=forms.Textarea())