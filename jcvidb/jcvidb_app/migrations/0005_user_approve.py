# Generated by Django 4.2.10 on 2024-02-21 23:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("jcvidb_app", "0004_rename_joined_date_user_creationdate_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="approve",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]