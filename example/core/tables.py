import django_tables2 as tables
from spyglass.models import Query
from core.models import NewsStory
from spyglass.models import Notification

class ProfileTable(tables.Table):
    id = tables.Column(visible=False)
    edit = tables.TemplateColumn(orderable=False, template_name='ui/edit_button.html')
    delete = tables.TemplateColumn(orderable=False, template_name='ui/delete_button.html')

    class Meta:
        model = Query
        fields = ("site", "params", "completed", "next_check")
        attrs = {'class': 'table table-striped table-bordered'}

class NotificationTable(tables.Table):

    class Meta:
        model = Notification
        attrs = {'class': 'table table-striped table-bordered'}
        fields = ("result", "time")
