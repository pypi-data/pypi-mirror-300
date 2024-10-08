from django.contrib.gis.admin import GISModelAdmin
from .forms.widgets import WMTSWidget


class WMTSGISModelAdmin(GISModelAdmin):
    gis_widget = WMTSWidget
