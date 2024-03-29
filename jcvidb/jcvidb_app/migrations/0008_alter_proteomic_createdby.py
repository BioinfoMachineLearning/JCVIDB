# Generated by Django 4.2.10 on 2024-02-22 20:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("jcvidb_app", "0007_alter_user_email_alter_user_role"),
    ]

    operations = [
        migrations.AlterField(
            model_name="proteomic",
            name="createdBy",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="jcvidb_app.user",
            ),
        ),
    ]
