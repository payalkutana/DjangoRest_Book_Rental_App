from datetime import datetime
from django.shortcuts import render, get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from django.db.models import Q
from . import serializers
from .models import Book, RentedBook, RequestedBook
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser


class BookCreateListView(generics.GenericAPIView):
    serializer_class = serializers.BookCreationSerializer
    queryset = Book.objects.all()
    permission_classes =[IsAuthenticatedOrReadOnly]

    def get(self,request,book_id=None):

        if book_id:
            books = get_object_or_404(Book, pk=book_id)
            serializer = self.serializer_class(instance=books)
        else:
            books = Book.objects.all()
            serializer = self.serializer_class(books, many=True)

        return Response(serializer.data, status = status.HTTP_200_OK)


    def post(self, request):

        data = request.data
        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookUpdateDeleteView(generics.GenericAPIView):
    serializer_class = serializers.BookCreationSerializer
    permission_classes = [IsAdminUser]

    def put(self, request, book_id):
        book = get_object_or_404(Book, pk=book_id)
        serializer = self.serializer_class(instance=book, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, book_id):
        book = get_object_or_404(Book, pk=book_id)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BookRentalCreationView(generics.GenericAPIView):
    serializer_class = serializers.BookRentalCreationSerializer
    permission_classes = [IsAuthenticated]
    
    def post(self, request, book_id):
        data = request.data
        serializer = self.serializer_class(data=data)
        total_bookOnRent = 0

        if serializer.is_valid():
            user = request.user
            book = Book.objects.get(pk=book_id)
            print(book)
            total_bookOnRent = RentedBook.objects.filter(Q(book=book) & Q(book_status__contains='ONRENT') | Q(book_status__contains='PENDING') | Q(book_status__contains='PAID') ).count()
            
            print(total_bookOnRent)
            if book.quantity > total_bookOnRent:
                print("Book is Available.")
                serializer.save(user=user, book=book)
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)

            else:
                return Response({"status": "Failed", "data": "Book Is Not Available"}, status=status.HTTP_400_BAD_REQUEST)
                
        return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class BookRentalUpdateDeleteDetailView(generics.GenericAPIView):
    serializer_class = serializers.BookRentalUpdateSerializer
    permission_classes = [IsAuthenticated]

        
    def get(self,request, book_id=None):
        
        user = request.user
        if book_id:
            book = get_object_or_404(Book, pk=book_id)
            userBooks = RentedBook.objects.filter(Q(user=user),Q(book=book))
            serializer = self.serializer_class(userBooks,many=True)
        else:
            userBooks = RentedBook.objects.filter(user=user)
            serializer = self.serializer_class(userBooks,many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def patch(self,request,rentedbook_id,Transaction):

        rentedBook = get_object_or_404(RentedBook,pk=rentedbook_id)
        
       
        if Transaction == "Penalty_Paid" :
    
            data = {"book_status" :"PAID", "penalty":request.POST["penalty"]}
            serializer = self.serializer_class(instance=rentedBook, data = data)
            
            if serializer.is_valid():
                serializer.save()
                return Response({"status": "success", "data": "Penalty is Paid."}, status=status.HTTP_200_OK)

        if Transaction == "Return_Book" or Transaction == "Check_Penalty":

            created_at = rentedBook.created_at
            print(created_at)

            TakenOn = created_at.strftime("%Y/%m/%d")   
            Today = datetime.now().strftime("%Y/%m/%d")
            print(TakenOn, Today)

            # convert string to date object
            d1 = datetime.strptime(TakenOn, "%Y/%m/%d")
            d2 = datetime.strptime(Today, "%Y/%m/%d")
            
            duration = d2 - d1
            print(duration.days)

            if Transaction == "Check_Penalty" :
                print("Inside IF")
                if duration.days > rentedBook.duration :
                    print("inside Days")
                    extradays = duration.days - rentedBook.duration
                    print(extradays)
                    penalty = extradays * 20
                    return Response({"data": "Please Pay Penalty In Order to return the book.","penalty":penalty}, status=status.HTTP_200_OK)
                else:
                    return Response({"status":"success","data": "No Penalty!!"}, status=status.HTTP_200_OK)                


            else:
                if rentedBook.book_status == "PENDING" or rentedBook.book_status == "ONRENT":
                    print("Inside Pending")
                    if duration.days > rentedBook.duration :
                        print("inside Days")
                        extradays = duration.days - rentedBook.duration
                        print(extradays)
                        penalty = extradays * 20
                        return Response({"status": "Failed", "data": "Please Pay Penalty In Order to return the book.","penalty":penalty}, status=status.HTTP_400_BAD_REQUEST)

                    else:
                        print("inside Else")
                        data = {"book_status" :"RETURNED"}
                        serializer = self.serializer_class(instance=rentedBook, data=data)

                        if serializer.is_valid():
                            print("Book Data is Valid")
                            serializer.save()
                            return Response(data=serializer.data, status=status.HTTP_200_OK)
                
                else:
                    print("inside Else")
                    data = {"book_status" :"RETURNED"}
                    serializer = self.serializer_class(instance=rentedBook, data=data)

                    if serializer.is_valid():
                        print("Book Data is Valid")
                        serializer.save()
                        return Response(data=serializer.data, status=status.HTTP_200_OK)

        return Response({"status": "Failed", "data": "Error !!!!"}, status=status.HTTP_400_BAD_REQUEST)

        
class RequestedBookCreation(generics.GenericAPIView):
    serializer_class = serializers.RequestedBookSerializer
    queryset = RequestedBook.objects.all()
    permission_classes =[IsAuthenticated]

    def get(self,request,book_id=None):
        if book_id:
            books = get_object_or_404(RequestedBook, pk=book_id)
            serializer = self.serializer_class(instance=books)
        else:
            books = RequestedBook.objects.all()
            serializer = self.serializer_class(books, many=True)

        return Response(serializer.data, status = status.HTTP_200_OK)


    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        user = request.user
        
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    



        