# Generated by Django 4.2.10 on 2024-04-02 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("jcvidb_app", "0021_basic_data_is_delete_column_data_is_delete_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="basic_data", name="code", field=models.CharField(max_length=9),
        ),
    ]