from django.urls import path

from library_store.views.add_book.api_wrapper import AddBookAPI
from library_store.views.add_member.api_wrapper import AddMemberAPI
from library_store.views.get_all_books_for_librarian.api_wrapper import GetAllBooksForLibrarianAPI
from library_store.views.get_all_users_for_librarian.ap_wrapper import GetAllUsersForLibrarianAPI
from library_store.views.remove_book.api_wrapper import RemoveBookAPI
from library_store.views.remove_member.api_wrapper import RemoveMemberAPI
from library_store.views.update_book_details.api_wrapper import UpdateBookDetailsAPI
from library_store.views.update_member_details.api_wrapper import UpdateMemberDetailsAPI

urlpatterns = [
      path('librarian/book/all', GetAllBooksForLibrarianAPI.as_view()),
      path('librarian/book/add', AddBookAPI.as_view()),
      path('librarian/book/<str:book_id>/update', UpdateBookDetailsAPI.as_view()),
      path('librarian/book/<str:book_id>/remove', RemoveBookAPI.as_view()),

      path('librarian/member/all', GetAllUsersForLibrarianAPI.as_view()),
      path('librarian/member/add', AddMemberAPI.as_view()),
      path('librarian/member/<int:member_id>/update', UpdateMemberDetailsAPI.as_view()),
      path('librarian/member/<int:member_id>/remove', RemoveMemberAPI.as_view()),
]
