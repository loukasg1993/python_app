from django.contrib import admin
from .models import personal_information,appointment


# username=admin, password=1234
admin.site.register(personal_information)
admin.site.register(appointment)

