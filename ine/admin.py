from django.contrib import admin
from ine.models import dict_ccaa, dict_provinces, dict_municipalities, metadata

admin.site.register(dict_ccaa)
admin.site.register(dict_provinces)
admin.site.register(dict_municipalities)
admin.site.register(metadata)
