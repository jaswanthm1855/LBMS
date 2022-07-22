import json

from django.http import HttpResponse
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from library_store.custom_exceptions import \
    UserNotAuthorizedException, InvalidBookIdException


class RemoveBookAPI(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args,  **kwargs):
        user_id = request.user.id
        book_id = kwargs["book_id"]

        response = self.remove_book_wrapper(
            user_id=user_id, book_id=book_id)
        return response

    @staticmethod
    def remove_book_wrapper(user_id: int, book_id: str):
        from library_store.storages.storage_implementation import StorageImplementation
        from library_store.interactors.book_crud_interactor import BookCRUDInteractor

        storage = StorageImplementation()
        interactor = BookCRUDInteractor(storage=storage)
        try:
            interactor.remove_book(user_id=user_id, book_id=book_id)
            response = {"message": "remove successful"}
            status = 200
        except UserNotAuthorizedException:
            response = {"message": "UnAuthorized"}
            status = 401
        except InvalidBookIdException:
            response = {"message": "Invalid Book Id"}
            status = 404

        response = json.dumps(response)

        return HttpResponse(content=response, status=status)
