from django.db import models


class JiraTicket(models.Model):
    summary = models.CharField(max_length=8192)
    issue_key = models.CharField(max_length=16, primary_key=True)
    resolution = models.CharField(max_length=16)
    assignee = models.EmailField(max_length=255)
    reporter = models.EmailField(max_length=255)
    created = models.DateTimeField()
    resolved = models.DateTimeField()
    description = models.TextField()
    last_comment = models.TextField()


class Annotation(models.Model):
    jira_ticket = models.ForeignKey(JiraTicket, on_delete=models.CASCADE)
    abstract = models.TextField()
    deliverable = models.URLField(max_length=8192)
