from django.contrib import admin
from .models import Contact,Friendspost,Adminspost

# Register your models here.
#admin.site.register(Contact)
admin.site.register(Friendspost)
admin.site.register(Adminspost)

class ContactAdmin(admin.ModelAdmin):
    list_display =('name','email','phone','desc')
    search_fields=('name','email')

    list_per_page = 10

admin.site.register(Contact,ContactAdmin)
