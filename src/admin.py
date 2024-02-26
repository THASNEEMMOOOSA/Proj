from django.contrib import admin

# Register your models here.
from .models import Bookpack,Order
admin.site.register(Bookpack)
admin.site.register(Order)