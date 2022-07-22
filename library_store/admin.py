from django.contrib import admin
from library_store import models

# Register your models here.

admin.site.register(models.Book)
admin.site.register(models.UserDetails)
admin.site.register(models.UserBookBorrowDetails)
