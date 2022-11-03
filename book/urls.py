from django.urls import path
from book.views import BookDetailAPI, BookAPI, revocer_book

urlpatterns = [
    path("<book_id>/recovery/", revocer_book),
    path("<book_id>/", BookDetailAPI.as_view()),
    path("", BookAPI.as_view()),
]
