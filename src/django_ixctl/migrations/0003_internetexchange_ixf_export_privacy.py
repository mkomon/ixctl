# Generated by Django 2.2.17 on 2021-01-21 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("django_ixctl", "0002_ix_slug_field"),
    ]

    operations = [
        migrations.AddField(
            model_name="internetexchange",
            name="ixf_export_privacy",
            field=models.CharField(
                choices=[
                    ("public", "IX-F export feed is public"),
                    ("private", "IX-F export feed requires secret key to view"),
                ],
                default="public",
                max_length=32,
            ),
        ),
    ]
