from django.contrib import admin


from .models import User,Role,Basic_data,Data_type,File_data,column_data
# Register your models here.
admin.site.register(User)
admin.site.register(Role)
admin.site.register(Basic_data)

admin.site.register(Data_type)
admin.site.register(File_data)
admin.site.register(column_data)