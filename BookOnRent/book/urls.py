from django.urls import path
from .views import BookCreateListView,BookUpdateDeleteView,BookRentalCreationView,BookRentalUpdateDeleteDetailView,RequestedBookCreation

urlpatterns = [
    path('book/',BookCreateListView.as_view(),name='add_book'),
    path('book/<int:book_id>/',BookCreateListView.as_view(),name='search_book'),
    path('book/<int:book_id>/update',BookUpdateDeleteView.as_view(),name='update_book'),
    path('book/<int:book_id>/delete',BookUpdateDeleteView.as_view(),name='delete_book'),

    # path('book/<int:book_id>/UserRecord',BookRentalCreationView.as_view(),name='book_records'),
    path('book/<int:book_id>/onRent',BookRentalCreationView.as_view(),name='book_on_rent'),

    path('book/<int:rentedbook_id>/<str:Transaction>',BookRentalUpdateDeleteDetailView.as_view(),name='return_book'),
    path('book/userRecord/',BookRentalUpdateDeleteDetailView.as_view(),name='user_record'),
    path('book/userRecord/<int:book_id>/',BookRentalUpdateDeleteDetailView.as_view(),name='user_record'),

    path('RequestBook/',RequestedBookCreation.as_view(),name='book_request'),
    
]
