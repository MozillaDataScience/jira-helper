from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render

from .models import Annotation, JiraTicket
from .forms import AnnotationForm


def _annotated(ticket):
    try:
        ticket.annotation
        return True
    except Annotation.DoesNotExist:
        return False


def index(request):
    tickets = JiraTicket.objects.all()
    assignees = sorted({ticket.assignee for ticket in tickets})
    tickets_by_assignee = {}
    for a in assignees:
        completed = sorted(
            (t for t in tickets if t.assignee == a and _annotated(t)),
            key=lambda t: t.created,
        )
        todo = sorted(
            (t for t in tickets if t.assignee == a and not _annotated(t)),
            key=lambda t: t.created,
        )
        score = "{:.0f}%".format(len(completed) / len(todo + completed) * 100)
        tickets_by_assignee[a or "Unassigned"] = {
            "completed": completed,
            "todo": todo,
            "n": len(todo) + len(completed),
            "score": score,
        }
    return render(
        request, "tickets/index.html", {"tickets_by_assignee": tickets_by_assignee}
    )


def detail(request, issue_key):
    ticket = get_object_or_404(JiraTicket, issue_key=issue_key)
    annotation = None
    try:
        annotation = ticket.annotation
    except Annotation.DoesNotExist:
        pass

    if request.method == "POST":
        form = AnnotationForm(request.POST, instance=annotation)
        if not form.is_valid():
            return HttpResponseRedirect(request.path)
        annotation = form.save(commit=False)
        annotation.jira_ticket = ticket
        annotation.save()
        return HttpResponseRedirect(request.path)

    form = AnnotationForm(instance=annotation)
    return render(request, "tickets/detail.html", {"ticket": ticket, "form": form})
