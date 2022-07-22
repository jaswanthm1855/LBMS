import datetime

from library_store.constants.enums import BookAvailabilityStatusEnum
from library_store.custom_exceptions import AvailabilityStatusUpdationIsNotAllowedException, \
    UserDoesNotBorrowedBookException, BookIsAlreadyBorrowedException, InvalidBookIdException
from library_store.interactors.storage_interface import StorageInterface


class UpdateBookAvailabilityStatusByMember:

    def __init__(self, storage: StorageInterface):
        self.storage = storage

    def update_availability_status_by_member(
            self, member_id: int, book_id: str,
            availability_status: BookAvailabilityStatusEnum
    ):
        self._validate_is_book_exists(book_id)

        book_details = self.storage.get_books_details([book_id])[0]
        self._validate_is_given_availability_status_updation_possible(
            given_availability_status=availability_status,
            existing_availability_status=book_details["availability_status"]
        )
        if availability_status == BookAvailabilityStatusEnum.available.value:
            self._validate_is_user_borrowed_book(
                member_id=member_id, book_id=book_id)
            self.storage.update_book_availability_status(
                book_id=book_id, availability_status=availability_status)
            return_datetime = datetime.datetime.now()
            self.storage.update_user_borrowed_book_return_status(
                member_id=member_id, book_id=book_id, return_datetime=return_datetime
            )

        elif availability_status == BookAvailabilityStatusEnum.borrowed.value:
            self._validate_is_book_available(
                book_availability_status=book_details["availability_status"])
            self.storage.update_book_availability_status(
                book_id=book_id, availability_status=availability_status)
            self.storage.create_user_borrowed_book(member_id=member_id, book_id=book_id)

    def _validate_is_user_borrowed_book(
            self, member_id: int, book_id: str):
        is_user_borrowed_book = self.storage.is_user_borrowed_book(
            member_id=member_id, book_id=book_id)
        if not is_user_borrowed_book:
            raise UserDoesNotBorrowedBookException()

    @staticmethod
    def _validate_is_book_available(book_availability_status: BookAvailabilityStatusEnum):
        if book_availability_status == BookAvailabilityStatusEnum.borrowed.value:
            raise BookIsAlreadyBorrowedException()

    @staticmethod
    def _validate_is_given_availability_status_updation_possible(
            given_availability_status: BookAvailabilityStatusEnum,
            existing_availability_status: BookAvailabilityStatusEnum
    ):
        existing_availability_status_wise_possible_availability_statuses = {
            BookAvailabilityStatusEnum.available.value: [BookAvailabilityStatusEnum.borrowed.value],
            BookAvailabilityStatusEnum.borrowed.value: [BookAvailabilityStatusEnum.available.value],
        }
        possible_statuses = existing_availability_status_wise_possible_availability_statuses[
            existing_availability_status
        ]
        if given_availability_status not in possible_statuses:
            raise AvailabilityStatusUpdationIsNotAllowedException()

    def _validate_is_book_exists(self, book_id):
        is_book_exists = self.storage.is_book_exists(book_id)
        if not is_book_exists:
            raise InvalidBookIdException()
