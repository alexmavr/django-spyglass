from django.forms import ModelForm
from django.forms import CharField
from .models import Query

class QueryRequestForm(ModelForm):
    query = CharField(label='What are you looking for?')
    class Meta:
        model = Query
        fields = ('params','site')


