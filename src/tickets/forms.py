from django.forms import ModelForm

from tickets.models import Annotation


class AnnotationForm(ModelForm):
    class Meta:
        model = Annotation
        fields = ["no_deliverable", "deliverable", "abstract", "product"]
