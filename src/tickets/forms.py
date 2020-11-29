from django.forms import ModelForm, SelectMultiple, DateInput

from tickets.models import Annotation


class AnnotationForm(ModelForm):
    class Meta:
        model = Annotation
        fields = [
            "no_deliverable",
            "title",
            "completed_date",
            "deliverable",
            "artifact",
            "abstract",
            "product",
            "topic",
            "tags",
        ]
        widgets = {
            "topic": SelectMultiple(attrs={"size": "15"}),
            "completed_date": DateInput(attrs={"type": "date"}),
        }
