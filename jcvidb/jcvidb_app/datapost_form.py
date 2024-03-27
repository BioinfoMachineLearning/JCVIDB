# forms.py
from django import forms
from .models import Basic_data, User, column_data, File_data


class DataPostForm(forms.ModelForm):

    class Meta:
        model = Basic_data
        fields = ['id','createdBy', 'references',  'details' ,'funding', 'type','attachment']

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

class FileUploadPostForm(forms.ModelForm):
    class Meta:
        model = File_data
        fields = ['basic_data_id','attachment', ]

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
    def save(self, basic_data_id=None, commit=True):
        instance = super().save(commit=False)
        if basic_data_id and commit:
            instance.basic_data_id = Basic_data.objects.get(pk=basic_data_id)
            instance.save()
        return instance

class ColumnDataPostForm(forms.ModelForm):
    class Meta:
        model = column_data
        fields = ['file_data_id','col_index', 'sheet_index']

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

    def save(self, file_id=None, commit=True,option_str=None):
        instance = super().save(commit=False)
        if file_id and commit:
            instance.file_data_id = file_id
            instance.column_names = option_str
            instance.save()
        return instance