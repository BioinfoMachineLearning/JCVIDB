from django import forms
from .models import Proteomic


class DetailsForm(forms.ModelForm):
    session_id = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Proteomic
        fields = ['freeGeneSet', 'PGAN', 'locusTag', 'createdBy', 'essentiality', 'transporters', 'coverage',
                  'attachment', 'creationDate']

# def save(self, sessionid=None, commit=True):
#      instance = super().save(commit=False)
#      if sessionid:
#          print(sessionid)
#          instance.session_id = sessionid  # Set the sessionid attribute
#      if commit:
#
#          instance.save()
#      return instance
