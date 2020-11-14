from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Annotation, JiraTicket
from .forms import AnnotationForm


def index(request):
    tickets = JiraTicket.objects.all()
    annotations = Annotation.objects.all()
    annotated_ids = {a.jira_ticket_id for a in annotations}
    assignees = sorted({ticket.assignee for ticket in tickets})
    tickets_by_assignee = {}
    for a in assignees:
        completed = sorted(
            (t for t in tickets if t.assignee == a and t.issue_key in annotated_ids),
            key=lambda t: t.created,
        )
        todo = sorted(
            (
                t
                for t in tickets
                if t.assignee == a and t.issue_key not in annotated_ids
            ),
            key=lambda t: t.created,
        )
        score = "{:.0f}".format(len(completed) / len(todo + completed) * 100)
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

    next_ticket = None
    try:
        next_ticket = JiraTicket.objects.filter(
            assignee=ticket.assignee,
            created__gt=ticket.created,
            annotation__isnull=True,
        ).order_by("created")[0]
    except IndexError:
        pass

    if request.method == "POST":
        form = AnnotationForm(request.POST, instance=annotation)
        destination = request.path
        if "save_and_next" in request.POST and next_ticket:
            destination = reverse("detail", args=(next_ticket.issue_key,))
        if not form.is_valid():
            return HttpResponseRedirect(request.path + "?error=true")
        if not form.has_changed():
            return HttpResponseRedirect(destination)
        annotation = form.save(commit=False)
        annotation.jira_ticket = ticket
        annotation.save()
        return HttpResponseRedirect(destination + "?success=true")

    success = "success" in request.GET
    error = "error" in request.GET

    form = AnnotationForm(instance=annotation)
    return render(
        request,
        "tickets/detail.html",
        {
            "ticket": ticket,
            "form": form,
            "error": error,
            "success": success,
            "next_ticket": next_ticket,
        },
    )
