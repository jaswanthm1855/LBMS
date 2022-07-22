import json

from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView


class GetAllAvailableBooksForMemberAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user_id = request.user.id

        response = self.get_all_available_books_for_member(user_id)

        return response

    @staticmethod
    def get_all_available_books_for_member(user_id: int):
        from library_store.storages.storage_implementation import StorageImplementation
        from library_store.interactors.get_all_available_books_for_member_interactor import \
            GetAllAvailableBooksForMemberInteractor

        storage = StorageImplementation()
        interactor = GetAllAvailableBooksForMemberInteractor(storage=storage)

        available_books, user_borrowed_books = interactor.get_all_available_books_for_member(user_id)
        books = {
            "available_books": available_books,
            "user_borrowed_books": user_borrowed_books
        }
        books = json.dumps(books)

        return HttpResponse(content=books, status=200)
