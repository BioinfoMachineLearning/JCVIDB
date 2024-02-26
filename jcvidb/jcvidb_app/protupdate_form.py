# forms.py
from django import forms
from .models import Proteomic, User


class ProtUpdateForm(forms.ModelForm):

    class Meta:
        model = Proteomic
        fields = ['id', 'freeGeneSet','createdBy', 'essentiality', 'PGAN', 'coverage','locusTag', 'attachment']

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

    def save(self, sessionid=None, commit=True):
        instance = super().save(commit=False)
        if sessionid and commit:
            instance.createdBy = User.objects.get(pk=sessionid)
            instance.approved= 0 #  Set the sessionid attribute
            instance.save()
        return instance