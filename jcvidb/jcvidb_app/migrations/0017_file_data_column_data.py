# Generated by Django 4.2.10 on 2024-03-24 23:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("jcvidb_app", "0016_rename_type_id_basic_data_type"),
    ]

    operations = [
        migrations.CreateModel(
            name="File_data",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("attachment", models.FileField(blank=True, null=True, upload_to="")),
                (
                    "basic_data_id",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="jcvidb_app.basic_data",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="column_data",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("col_index", models.IntegerField(blank=True, default=0, null=True)),
                ("sheet_index", models.IntegerField(blank=True, default=0, null=True)),
                (
                    "file_data_id",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="jcvidb_app.file_data",
                    ),
                ),
            ],
        ),
    ]