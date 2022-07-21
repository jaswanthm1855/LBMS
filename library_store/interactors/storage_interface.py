import abc
from typing import Dict, List


class StorageInterface:

    @abc.abstractmethod
    def register_user_details(self, user_details: Dict):
        pass

    @abc.abstractmethod
    def get_all_books_details(self, is_removed: bool):
        pass

    @abc.abstractmethod
    def add_book(self, user_id: int, book_details: Dict) -> str:
        pass

    @abc.abstractmethod
    def is_book_exists(self, book_id: str):
        pass

    @abc.abstractmethod
    def update_book_details(self, book_id: str, book_details: Dict):
        pass

    @abc.abstractmethod
    def remove_book(self, book_id: str):
        pass

    @abc.abstractmethod
    def get_book_borrowed_users_details(self, book_ids: List[str]):
        pass

    @abc.abstractmethod
    def get_user_role(self, user_id: int):
        pass

    @abc.abstractmethod
    def is_book_name_already_exists(self, name: str) -> bool:
        pass
