# Generated by Django 4.2.10 on 2024-03-20 03:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("jcvidb_app", "0015_rename_type_basic_data_type_id"),
    ]

    operations = [
        migrations.RenameField(
            model_name="basic_data", old_name="type_id", new_name="type",
        ),
    ]