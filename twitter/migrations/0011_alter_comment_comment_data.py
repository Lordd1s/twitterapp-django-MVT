# Generated by Django 4.2.3 on 2023-10-11 14:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("twitter", "0010_alter_comment_comment_data"),
    ]

    operations = [
        migrations.AlterField(
            model_name="comment",
            name="comment_data",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2023, 10, 11, 14, 22, 16, 179394, tzinfo=datetime.timezone.utc
                ),
                verbose_name="Дата комментирования",
            ),
        ),
    ]
