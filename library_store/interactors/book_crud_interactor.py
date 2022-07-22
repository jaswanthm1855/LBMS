from typing import Dict, List

from library_store.constants.enums import BookAvailabilityStatusEnum
from library_store.custom_exceptions import UserNotAuthorizedException, InvalidBookIdException, \
    BookNameAlreadyExistsException, BookIsBorrowedException, InvalidAvailabilityStatusException
from library_store.interactors.permission_class import PermissionMixin
from library_store.interactors.storage_interface import StorageInterface


class BookCRUDInteractor(PermissionMixin):

    def __init__(self, storage: StorageInterface):
        self.storage = storage

    def add_book(self, user_id: int, book_details: Dict):
        self._validate_is_user_librarian(user_id)
        self._validate_is_book_name_already_exists(name=book_details["name"])
        self._validate_availability_status(book_details["availability_status"])

        book_id = self.storage.add_book(user_id, book_details)
        return book_id

    @staticmethod
    def _validate_availability_status(availability_status: BookAvailabilityStatusEnum):
        if availability_status not in BookAvailabilityStatusEnum.values_list():
            raise InvalidAvailabilityStatusException()

    def _validate_is_book_name_already_exists(self, name: str):
        is_name_exists = self.storage.is_book_name_already_exists(name=name)
        if is_name_exists:
            raise BookNameAlreadyExistsException()

    def get_all_books_for_librarian(self, user_id: int) -> Dict:
        self._validate_is_user_librarian(user_id)

        is_removed = False
        books = self.get_all_books(is_removed=is_removed)

        return books

    def _validate_is_user_librarian(self, user_id):
        is_librarian = self.is_librarian(user_id)
        if not is_librarian:
            raise UserNotAuthorizedException()

    def get_all_books(self, is_removed: bool):
        books = self.storage.get_all_books_details(is_removed=is_removed)
        book_ids = [book["book_id"] for book in books]
        book_id_wise_borrowed_users_details = \
            self.get_book_id_wise_borrowed_users_details(book_ids)

        for book in books:
            user_details = book_id_wise_borrowed_users_details.get(book["book_id"])
            if user_details:
                book["borrowed_by_user"] = user_details
        return books

    def update_book_details(self, user_id: int, book_id: str, book_details: Dict):
        self._validate_is_user_librarian(user_id)
        book_name = book_details.get("name")
        if book_name:
            self._validate_is_book_name_already_exists(name=book_details["name"])

        self._validate_is_book_exists(book_id)

        self.storage.update_book_details(book_id=book_id, book_details=book_details)

    def remove_book(self, user_id: int, book_id: str):
        self._validate_is_user_librarian(user_id)
        self._validate_is_book_exists(book_id)
        self._validate_is_book_borrowed(book_id)

        self.storage.remove_book(book_id)

    def _validate_is_book_exists(self, book_id):
        is_book_exists = self.storage.is_book_exists(book_id)
        if not is_book_exists:
            raise InvalidBookIdException()

    def get_book_id_wise_borrowed_users_details(self, book_ids: List[str]) -> Dict:
        book_ids = list(set(book_ids))
        user_details = self.storage.get_book_borrowed_users_details(book_ids)
        user_id_wise_user_details = {
            user["id"]: user for user in user_details
        }
        return user_id_wise_user_details

    def _validate_is_book_borrowed(self, book_id: str):
        is_book_borrowed = self.storage.is_book_borrowed(book_id)
        if is_book_borrowed:
            raise BookIsBorrowedException()
