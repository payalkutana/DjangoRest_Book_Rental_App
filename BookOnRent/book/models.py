from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.
User = get_user_model()

class Book(models.Model):
    Title = models.CharField(max_length=200, null=False)
    Author = models.CharField(max_length=200, null=False)
    image  = models.ImageField()
    quantity = models.IntegerField()
    isbn_number = models.CharField(max_length=50)

    def __str__(self):
        return f"<Book Title : {self.Title}>"

    
class RentedBook(models.Model):

    BOOK_STATUS =(
        ("ONRENT","onrent"),
        ("PENDING","pending"),
        ("PAID","paid"),
        ("RETURNED","returned"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    rent = models.FloatField(default=0.0)
    duration = models.IntegerField(default=1)
    book_status = models.CharField(max_length=20, choices=BOOK_STATUS, default=BOOK_STATUS[0][0])
    penalty = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"<Book {self.book.Title} by {self.user.username}"

class RequestedBook(models.Model):
    STATUS =(
        ("REQUESTED","requested"),
        ("CANCELED","canceled"),
    )

    BOOK_TRACK_STATUS = (
        ("SEARCHING","searching"),
        ("ORDERD","orderd"),
        ("PENDING","pending"),
        ("DELIVERED","delivered")
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Title = models.CharField(max_length=200, null=False)
    Author = models.CharField(max_length=200, null=False)
    image  = models.ImageField(null=True)
    isbn_number = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    book_status = models.CharField(max_length=20, choices=BOOK_TRACK_STATUS, default=BOOK_TRACK_STATUS[0][0])
    request_status = models.CharField(max_length=20, choices=STATUS, default=STATUS[0][0])


    def __str__(self):
        return f"<Book Title : {self.Title}>"