# Generated by Django 4.2.10 on 2024-04-02 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("jcvidb_app", "0020_basic_data_code"),
    ]

    operations = [
        migrations.AddField(
            model_name="basic_data",
            name="is_delete",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="column_data",
            name="is_delete",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="data_type",
            name="is_delete",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="file_data",
            name="is_delete",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="role", name="is_delete", field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="user", name="is_delete", field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="basic_data",
            name="code",
            field=models.CharField(max_length=9, unique=True),
        ),
    ]
