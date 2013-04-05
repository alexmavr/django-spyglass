from django.forms import ModelForm
from django.forms import CharField
from django.forms import EmailField
from .models import Query

class QueryForm(ModelForm):
    params = CharField(label='What are you looking for?')
    email = EmailField(max_length=75)

    class Meta:
        model = Query
        fields = ('params','site','persistent')

class EditQueryForm(ModelForm):
    params = CharField(label='What are you looking for?')

    class Meta:
        model = Query
        fields = ('params','site','persistent')
