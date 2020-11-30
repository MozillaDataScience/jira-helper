from django.db import models
from multiselectfield import MultiSelectField


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
    PRODUCT_CHOICES = [
        ("desktop", "Firefox desktop"),
        ("fenix", "Firefox for Android (Fenix)"),
        ("fennec", "Firefox for Android (Fennec)"),
        ("fennec_ios", "Firefox for iOS"),
        ("other_mobile", "Other mobile/non-desktop"),
        ("many", "Many products"),
    ]

    TOPICS = (
        ("accounts", "Accounts"),
        ("activity_stream", "Activity Stream"),
        ("bookmarks", "Bookmarks"),
        ("devtools", "Devtools"),
        ("download", "Download page"),
        ("enterprise", "Enterprise"),
        ("heartbeat", "Heartbeat"),
        ("nav", "Navigation"),
        ("newtab", "New tab"),
        ("onboarding", "Onboarding"),
    )

    ARTIFACTS = (
        ("dashboard", "Dashboard"),
        ("experiment", "Experiment"),
        ("investigation", "Investigation report"),
    )

    jira_ticket = models.OneToOneField(JiraTicket, on_delete=models.CASCADE)
    abstract = models.TextField(
        "tl;dr",
        blank=True,
        help_text="<a href='https://docs.google.com/document/d/1QiymsHOvyNoaSL5GfY_9yWMOl8qAZy6yomTld3Twfws/edit'>How to write an abstract</a>",
    )
    deliverable = models.URLField(
        blank=True, max_length=8192, help_text="URL to a deliverable for this ticket"
    )
    no_deliverable = models.BooleanField(
        "This ticket had no deliverable", default=False
    )
    product = models.TextField(choices=PRODUCT_CHOICES, blank=True)

    topic = MultiSelectField(
        "Topics",
        choices=TOPICS,
        max_length=1024,
        blank=True,
        help_text="Ctrl- or ⌘-click to select multiple topics",
    )
    tags = models.CharField(
        max_length=1024,
        blank=True,
        help_text="Comma-separated list of any additional tags you'd like to apply.",
    )

    artifact = models.CharField(blank=True, max_length=1024, choices=ARTIFACTS)
    title = models.CharField(max_length=1024, blank=True)
    completed_date = models.DateField(blank=True, null=True)

    def is_empty(self):
        if self.title and (self.title != self.jira_ticket.summary):
            return False
        if self.completed_date and (
            self.completed_date != self.jira_ticket.resolved.date
        ):
            return False
        return not (
            self.abstract
            or self.artifact
            or self.deliverable
            or self.no_deliverable
            or self.product
            or self.topic
            or self.tags
        )

    def is_complete(self):
        if self.no_deliverable:
            return True
        if (
            self.abstract
            and self.deliverable
            and self.product
            and self.topic
            and self.artifact
        ):
            return True
        return False

    def save(self, *args, **kwargs):
        if self.is_empty():
            self.delete()
        else:
            super().save(*args, **kwargs)
