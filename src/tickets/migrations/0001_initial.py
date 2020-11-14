# Generated by Django 3.1.3 on 2020-11-14 02:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="JiraTicket",
            fields=[
                ("summary", models.CharField(max_length=8192)),
                (
                    "issue_key",
                    models.CharField(max_length=16, primary_key=True, serialize=False),
                ),
                ("resolution", models.CharField(max_length=16)),
                ("assignee", models.EmailField(max_length=255)),
                ("reporter", models.EmailField(max_length=255)),
                ("created", models.DateTimeField()),
                ("resolved", models.DateTimeField()),
                ("description", models.TextField()),
                ("last_comment", models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name="Annotation",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("abstract", models.TextField()),
                ("deliverable", models.URLField(max_length=8192)),
                (
                    "jira_ticket",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="tickets.jiraticket",
                    ),
                ),
            ],
        ),
    ]