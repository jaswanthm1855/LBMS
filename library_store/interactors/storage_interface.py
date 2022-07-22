import abc
import datetime
from typing import Dict, List

from library_store.constants.enums import UserRoleEnum, BookAvailabilityStatusEnum


class StorageInterface:

    @abc.abstractmethod
    def register_user_details(self, user_details: Dict):
        pass

    @abc.abstractmethod
    def get_all_books_details(self, is_removed: bool) -> List[Dict]:
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
    def get_user_role(self, user_id: int) -> UserRoleEnum:
        pass

    @abc.abstractmethod
    def is_book_name_already_exists(self, name: str) -> bool:
        pass

    @abc.abstractmethod
    def get_all_users_details(self, roles: List[UserRoleEnum]) -> List[Dict]:
        pass

    @abc.abstractmethod
    def update_auth_member_details(
            self, member_id: int, member_details: Dict):
        pass

    @abc.abstractmethod
    def update_member_details(self, member_id: int, member_details: Dict):
        pass

    @abc.abstractmethod
    def remove_member(self, member_id: int):
        pass

    @abc.abstractmethod
    def update_auth_user_active_status(self, user_id: int, is_active: bool):
        pass

    @abc.abstractmethod
    def is_user_exists(self, user_id: int) -> bool:
        pass

    @abc.abstractmethod
    def is_user_name_exists(self, username: str) -> bool:
        pass

    @abc.abstractmethod
    def add_member(self, member_details: Dict):
        pass

    @abc.abstractmethod
    def create_auth_user(self, member_details: Dict) -> int:
        pass

    @abc.abstractmethod
    def get_all_available_books_details(self) -> List[Dict]:
        pass

    @abc.abstractmethod
    def get_user_borrowed_book_ids(self, user_id: int) -> List[str]:
        pass

    @abc.abstractmethod
    def get_books_details(self, book_ids: List[str]) -> List[Dict]:
        pass

    @abc.abstractmethod
    def update_book_availability_status(
            self, book_id: str, availability_status: BookAvailabilityStatusEnum):
        pass

    @abc.abstractmethod
    def update_user_borrowed_book_return_status(
            self, member_id: int, book_id: str, return_datetime: datetime.datetime):
        pass

    @abc.abstractmethod
    def is_user_borrowed_book(self, member_id: int, book_id: str) -> bool:
        pass

    @abc.abstractmethod
    def create_user_borrowed_book(self, member_id: int, book_id: str):
        pass

    @abc.abstractmethod
    def is_book_borrowed(self, book_id: str) -> bool:
        pass
