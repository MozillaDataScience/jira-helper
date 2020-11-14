from django.db import models


class JiraTicket(models.Model):
    summary = models.CharField(max_length=8192)
    issue_key = models.CharField(max_length=16, primary_key=True)
    resolution = models.CharField(max_length=16)
    assignee = models.EmailField(max_length=255, blank=True)
    reporter = models.EmailField(max_length=255)
    created = models.DateTimeField()
    resolved = models.DateTimeField(blank=True, null=True)
    description = models.TextField(blank=True)
    last_comment = models.TextField(blank=True)


class Annotation(models.Model):
    jira_ticket = models.OneToOneField(JiraTicket, on_delete=models.CASCADE)
    abstract = models.TextField(blank=True)
    deliverable = models.URLField(
        blank=True, max_length=8192, help_text="URL to a deliverable for this ticket"
    )
