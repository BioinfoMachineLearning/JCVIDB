from django import forms
from .models import Basic_data


class DetailsForm(forms.ModelForm):
    session_id = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Basic_data
        fields = ['id','createdBy', 'references',  'details' ,'funding', 'type']


# def save(self, sessionid=None, commit=True):
#      instance = super().save(commit=False)
#      if sessionid:
#          print(sessionid)
#          instance.session_id = sessionid  # Set the sessionid attribute
#      if commit:
#
#          instance.save()
#      return instance
