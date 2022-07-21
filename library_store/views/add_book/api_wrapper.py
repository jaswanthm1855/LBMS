import json
from typing import Dict

from django.http import HttpResponse
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from library_store.custom_exceptions import \
    UserNotAuthorizedException, BookNameAlreadyExistsException


class AddBookAPI(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args,  **kwargs):
        user_id = request.user.id
        request_data = request.data
        book_details = {
            "name": request_data["name"],
            "description": request_data["description"],
            "author": request_data["author"],
            "availability_status": request_data["availability_status"]
        }

        response = self.add_book_wrapper(
            user_id=user_id, book_details=book_details)
        return response

    @staticmethod
    def add_book_wrapper(user_id: int, book_details: Dict):
        from library_store.storages.storage_implementation import StorageImplementation
        from library_store.interactors.book_crud_interactor import BookCRUDInteractor

        storage = StorageImplementation()
        interactor = BookCRUDInteractor(storage=storage)
        try:
            book_id = interactor.add_book(user_id=user_id, book_details=book_details)
            response = {"message": "Book added successfully", "book_id": book_id}
            status = 201
        except UserNotAuthorizedException:
            response = {"message": "UnAuthorized"}
            status = 401
        except BookNameAlreadyExistsException:
            response = {"message": "Book name already exists"}
            status = 403

        response = json.dumps(response)

        return HttpResponse(content=response, status=status)
