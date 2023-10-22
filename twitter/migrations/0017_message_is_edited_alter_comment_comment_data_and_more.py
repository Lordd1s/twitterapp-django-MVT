# Generated by Django 4.2.3 on 2023-10-20 06:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("twitter", "0016_message_is_deleted_alter_comment_comment_data_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="message",
            name="is_edited",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="comment",
            name="comment_data",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2023, 10, 20, 6, 25, 33, 523277, tzinfo=datetime.timezone.utc
                ),
                verbose_name="Дата комментирования",
            ),
        ),
        migrations.AlterField(
            model_name="message",
            name="timestamp",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2023, 10, 20, 6, 25, 33, 523277, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]