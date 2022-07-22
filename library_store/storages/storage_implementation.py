import datetime
from typing import Dict, List

from django.contrib.auth import get_user_model

from library_store import models
from library_store.constants.enums import UserRoleEnum
from library_store.interactors.storage_interface import StorageInterface


class StorageImplementation(StorageInterface):

    @staticmethod
    def _get_user_obj_for_id(user_id: int):
        from django.contrib.auth import get_user_model

        User = get_user_model()
        user_obj = User.objects.get(id=user_id)

        return user_obj

    def register_user_details(self, user_details: Dict):
        models.UserDetails.objects.create(
            user=user_details["user"], role=user_details["role"]
        )

    def get_all_books_details(self, is_removed: bool) -> List[Dict]:
        books = models.Book.objects.filter(is_removed=is_removed).values(
            "book_id", "name", "description", "author", "availability_status"
        )
        return list(books)

    def add_book(self, user_id: int, book_details: Dict) -> str:
        user_obj = self._get_user_obj_for_id(user_id)
        book_obj = models.Book.objects.create(
            name=book_details["name"],
            description=book_details.get("description"),
            author=book_details["author"],
            availability_status=book_details["availability_status"],
            created_by_user=user_obj
        )
        return str(book_obj.book_id)

    def is_book_exists(self, book_id: str):
        is_book_exists = models.Book.objects.filter(
            book_id=book_id, is_removed=False).exists()
        return is_book_exists

    def update_book_details(self, book_id: str, book_details: Dict):
        book_obj = models.Book.objects.get(book_id=book_id)

        for field, value in book_details.items():
            if value:
                setattr(book_obj, field, value)
        book_obj.save()

    def remove_book(self, book_id: str):
        models.Book.objects.filter(
            book_id=book_id).update(is_removed=True)

    def get_book_borrowed_users_details(self, book_ids: List[str]):
        books = models.UserBookBorrowDetails.objects.filter(
            book_id__in=book_ids, is_returned=False)
        books_details = [{
                "book_id": book.book_id, "user_id": book.user_id,
                "borrowed_date_time": self._convert_datetime_to_str(book.borrowed_date_time)
            } for book in books
        ]
        return books_details

    @staticmethod
    def _convert_datetime_to_str(date_time: datetime.datetime) -> str:
        from library_store.constants.constants import DEFAULT_DATE_TIME_FORMAT

        date_time = date_time.strftime(DEFAULT_DATE_TIME_FORMAT)
        return date_time

    def get_user_role(self, user_id: int) -> UserRoleEnum:
        user_details = models.UserDetails.objects.get(user_id=user_id)
        return user_details.role

    def is_book_name_already_exists(self, name: str) -> bool:
        is_name_exists = models.Book.objects.filter(name=name).exists()
        return is_name_exists

    def get_all_users_details(self, roles: List[UserRoleEnum]) -> List[Dict]:
        users = models.UserDetails.objects.filter(role__in=roles, is_active=True)
        users_details = [
            {
                "user_id": user.user_id,
                "username": user.user.username,
                "role": user.role
            } for user in users
        ]
        return users_details

    def update_auth_member_details(
            self, member_id: int, member_details: Dict):
        User = get_user_model()
        user_obj = User.objects.get(id=member_id)

        if member_details["username"]:
            user_obj.username = member_details["username"]

        if member_details["password"]:
            user_obj.set_password(member_details["password"])

        user_obj.save()

    def update_member_details(self, member_id: int, member_details: Dict):
        if member_details["role"]:
            models.UserDetails.objects.filter(
                user_id=member_id
            ).update(role=member_details["role"])

    def remove_member(self, member_id: int):
        models.UserDetails.objects.filter(
            user_id=member_id).update(is_active=False)

    def is_user_exists(self, user_id: int) -> bool:
        is_user_exists = models.UserDetails.objects.filter(
            user_id=user_id, is_active=True).exists()
        return is_user_exists

    def is_user_name_exists(self, username: str) -> bool:
        from django.contrib.auth import get_user_model

        User = get_user_model()
        is_username_exists = User.objects.filter(username=username).exists()
        return is_username_exists

    def create_auth_user(self, member_details: Dict) -> int:
        from django.contrib.auth import get_user_model

        User = get_user_model()
        user = User.objects.create_user(
            username=member_details["username"],
            password=member_details['password']
        )
        return user.id

    def add_member(self, member_details: Dict):
        user_id = member_details["member_id"]
        user_obj = self._get_user_obj_for_id(user_id)

        models.UserDetails.objects.create(
            user=user_obj, role=member_details["role"]
        )
