from django.contrib import admin
from .models import URL


# Register your models here.
class URLInline(admin.StackedInline):
    model = URL
    can_delete = False
    verbose_name_plural = 'URLs'


admin.site.register(URL)