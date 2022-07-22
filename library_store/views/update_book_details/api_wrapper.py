import json
from typing import Dict

from django.http import HttpResponse
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from library_store.custom_exceptions import \
    UserNotAuthorizedException, InvalidBookIdException, BookNameAlreadyExistsException


class UpdateBookDetailsAPI(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request, *args,  **kwargs):
        user_id = request.user.id
        request_data = request.data
        book_id = kwargs["book_id"]
        book_details = {
            "name": request_data.get("name"),
            "description": request_data.get("description"),
            "author": request_data.get("author"),
            "availability_status": request_data.get("availability_status")
        }

        response = self.update_book_details_wrapper(
            user_id=user_id, book_id=book_id, book_details=book_details)
        return response

    @staticmethod
    def update_book_details_wrapper(user_id: int, book_id: str, book_details: Dict):
        from library_store.storages.storage_implementation import StorageImplementation
        from library_store.interactors.book_crud_interactor import BookCRUDInteractor

        storage = StorageImplementation()
        interactor = BookCRUDInteractor(storage=storage)
        try:
            interactor.update_book_details(
                user_id=user_id, book_id=book_id, book_details=book_details)
            response = {"message": "update successful"}
            status = 200
        except UserNotAuthorizedException:
            response = {"message": "UnAuthorized"}
            status = 401
        except InvalidBookIdException:
            response = {"message": "Invalid Book Id"}
            status = 404
        except BookNameAlreadyExistsException:
            response = {"message": "Book name already exists"}
            status = 403

        response = json.dumps(response)

        return HttpResponse(content=response, status=status)
