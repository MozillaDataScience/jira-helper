from django.contrib import admin

from .models import JiraTicket, Annotation

admin.site.register(JiraTicket)
admin.site.register(Annotation)
