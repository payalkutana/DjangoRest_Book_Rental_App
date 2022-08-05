from datetime import datetime
from email.policy import default
from .models import Book, RentedBook, RequestedBook
from rest_framework import serializers

class BookCreationSerializer(serializers.ModelSerializer):
    Title = serializers.CharField(max_length=200)
    Author = serializers.CharField(max_length=200)
    image  = serializers.ImageField()
    quantity = serializers.IntegerField()
    isbn_number = serializers.CharField(max_length=50)

    class Meta:
        model = Book
        fields = ['Title','Author','image','quantity','isbn_number']

class BookRentalCreationSerializer(serializers.ModelSerializer):
    rent = serializers.FloatField()
    duration = serializers.IntegerField()
    book_status = serializers.CharField(default='ONRENT')
    created_at = serializers.DateTimeField(default=datetime.now)
   
    class Meta:
        model = RentedBook
        fields = ['rent','duration','book_status','created_at']

class BookRentalUpdateSerializer(serializers.ModelSerializer):
    book_status = serializers.CharField(default='ONRENT')
    penalty = serializers.FloatField(default=0.0)
    created_at = serializers.DateTimeField(default=datetime.now)
    updated_at = serializers.DateTimeField(default=datetime.now)

    class Meta:
        model = RentedBook
        fields = ['rent','duration','book_status','penalty','created_at','updated_at']

class RequestedBookSerializer(serializers.ModelSerializer):
    Title = serializers.CharField(max_length=200)
    Author = serializers.CharField(max_length=200)
    isbn_number = serializers.CharField(max_length=50,required=False)
    description = serializers.CharField(required=False)
    request_status = serializers.CharField(default="SEARCHING")

    class Meta:
        model = RequestedBook
        fields = ['Title','Author','isbn_number','description','request_status']