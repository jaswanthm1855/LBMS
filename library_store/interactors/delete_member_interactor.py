from library_store.custom_exceptions import UserHasBorrowedBooksException
from library_store.interactors.storage_interface import StorageInterface


class DeleteMemberInteractor:

    def __init__(self, storage: StorageInterface):
        self.storage = storage

    def delete_member(self, member_id: int):
        self._validate_is_member_borrowed_books(member_id=member_id)

        self.storage.remove_member(member_id)

        self.storage.update_auth_user_active_status(
            user_id=member_id, is_active=False)

    def _validate_is_member_borrowed_books(self, member_id: int):
        user_borrowed_book_ids = self.storage.get_user_borrowed_book_ids(
            user_id=member_id)
        if user_borrowed_book_ids:
            raise UserHasBorrowedBooksException()
