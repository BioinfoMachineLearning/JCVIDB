# Generated by Django 4.2.10 on 2024-03-20 03:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("jcvidb_app", "0014_alter_data_type_code"),
    ]

    operations = [
        migrations.RenameField(
            model_name="basic_data", old_name="type", new_name="type_id",
        ),
    ]
