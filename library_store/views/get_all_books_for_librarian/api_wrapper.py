import json

from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView


class GetAllBooksForLibrarianAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user_id = request.user.id

        response = self.get_all_books_for_librarian(user_id)

        return response

    @staticmethod
    def get_all_books_for_librarian(user_id: int):
        from library_store.storages.storage_implementation import StorageImplementation
        from library_store.custom_exceptions import UserNotAuthorizedException
        from library_store.interactors.book_crud_interactor import BookCRUDInteractor

        storage = StorageImplementation()
        interactor = BookCRUDInteractor(storage=storage)

        try:
            books_details = interactor.get_all_books_for_librarian(
                user_id=user_id)
            response = {"books_details": books_details}
            status = 200
        except UserNotAuthorizedException:
            response = {"message": "UnAuthorised"}
            status = 403

        response = json.dumps(response)

        return HttpResponse(content=response, status=status)
