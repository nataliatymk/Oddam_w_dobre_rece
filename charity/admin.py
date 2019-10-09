from django.contrib import admin
from charity.models import Donation, Institution, Category


# Register your models here.

admin.site.register(Institution)
admin.site.register(Donation)
admin.site.register(Category)