from django.contrib import admin

from .models import *

admin.site.register(Service)
admin.site.register(Mailaddr)
admin.site.register(Address)
admin.site.register(Phonenum)
admin.site.register(Account)

