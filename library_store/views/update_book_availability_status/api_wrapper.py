import json

from django.http import HttpResponse
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from library_store.constants.enums import BookAvailabilityStatusEnum
from library_store.custom_exceptions import InvalidBookIdException, AvailabilityStatusUpdationIsNotAllowedException, \
    UserDoesNotBorrowedBookException, BookIsAlreadyBorrowedException


class UpdateBookAvailabilityStatusAPI(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request, *args, **kwargs):
        user_id = request.user.id
        request_data = request.data
        book_id = kwargs["book_id"]
        availability_status = request_data["availability_status"]

        response = self.update_book_availability_status_wrapper(
            user_id=user_id, book_id=book_id, availability_status=availability_status)
        return response

    @staticmethod
    def update_book_availability_status_wrapper(
            user_id: int, book_id: str,
            availability_status: BookAvailabilityStatusEnum):
        from library_store.storages.storage_implementation import StorageImplementation
        from library_store.interactors.update_book_availability_status_by_member import \
            UpdateBookAvailabilityStatusByMember

        storage = StorageImplementation()
        interactor = UpdateBookAvailabilityStatusByMember(storage=storage)

        try:
            interactor.update_availability_status_by_member(
                member_id=user_id, book_id=book_id, availability_status=availability_status)
            response = {"message": "update successful"}
            status = 200
        except InvalidBookIdException:
            response = {"message": "Invalid Book Id"}
            status = 404
        except AvailabilityStatusUpdationIsNotAllowedException:
            response = {"message": "Updation of availability status is not allowed"}
            status = 401
        except UserDoesNotBorrowedBookException:
            response = {"message": "Book is not borrowed by user"}
            status = 401
        except BookIsAlreadyBorrowedException:
            response = {"message": "Book is already borrowed"}
            status = 401

        response = json.dumps(response)
        return HttpResponse(content=response, status=status)
