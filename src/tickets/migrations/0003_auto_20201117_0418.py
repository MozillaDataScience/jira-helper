# Generated by Django 3.1.3 on 2020-11-17 04:18

from django.db import migrations, models
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ("tickets", "0002_auto_20201114_2143"),
    ]

    operations = [
        migrations.AddField(
            model_name="annotation",
            name="tags",
            field=models.CharField(blank=True, max_length=1024),
        ),
        migrations.AddField(
            model_name="annotation",
            name="topic",
            field=multiselectfield.db.fields.MultiSelectField(
                blank=True,
                choices=[
                    ("accounts", "Accounts"),
                    ("activity_stream", "Activity Stream"),
                    ("bookmarks", "Bookmarks"),
                ],
                max_length=1024,
                verbose_name="Topics",
            ),
        ),
    ]
