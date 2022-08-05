from django.contrib import admin
from .models import Book,RentedBook,RequestedBook
# Register your models here.
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['Title','Author','image','quantity',"isbn_number"]

@admin.register(RentedBook)
class RentedBookAdmin(admin.ModelAdmin):
    list_display = ['pk','user','book','rent','duration','book_status','penalty','created_at','updated_at']

@admin.register(RequestedBook)
class RequestedBookAdmin(admin.ModelAdmin):
    list_display = ['pk','Title','Author',"isbn_number"]
# admin.site.register(RequestedBook)