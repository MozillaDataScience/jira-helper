from django.forms import ModelForm, SelectMultiple

from tickets.models import Annotation


class AnnotationForm(ModelForm):
    class Meta:
        model = Annotation
        fields = [
            "no_deliverable",
            "deliverable",
            "artifact",
            "abstract",
            "product",
            "topic",
            "tags",
        ]
        widgets = {"topic": SelectMultiple()}
