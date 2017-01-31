from django.forms import ModelForm
from core.models import Link


class LinkForm(ModelForm):
    def validate_unique(self):
        pass

    class Meta:
        model = Link
        fields = ['url']
