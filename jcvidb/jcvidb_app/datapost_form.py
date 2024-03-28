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

    def generate_code(self):
        latest_serial = Basic_data.objects.order_by('id').last()
        if latest_serial:
            # Extract the serial number from the custom_id and increment it
            serial_number = int(latest_serial.id) + 1
        else:
            serial_number = 1  # Start with 1 if no previous serial exists

            # Format the serial number to ensure it has 8 digits and starts with "P"
        self.code = 'P' + str(serial_number).zfill(8)
        return self.code

    def save(self, sessionid=None, commit=True):

        instance = super().save(commit=False)
        if sessionid and commit:
            instance.createdBy = User.objects.get(pk=sessionid)
            instance.code = self.generate_code()
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