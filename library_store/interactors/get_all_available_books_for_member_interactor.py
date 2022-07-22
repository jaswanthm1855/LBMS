from typing import Tuple, List, Dict

from library_store.interactors.storage_interface import StorageInterface


class GetAllAvailableBooksForMemberInteractor:

    def __init__(self, storage: StorageInterface):
        self.storage = storage

    def get_all_available_books_for_member(self, user_id: int) -> Tuple[List[Dict], List[Dict]]:
        available_books = self.storage.get_all_available_books_details()

        borrowed_book_ids = self.storage.get_user_borrowed_book_ids(user_id)
        user_borrowed_books = self.storage.get_books_details(book_ids=borrowed_book_ids)

        return available_books, user_borrowed_books
