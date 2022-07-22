from typing import Dict, List

from django.contrib.auth.hashers import make_password

from library_store.constants.constants import DEFAULT_PASSWORD
from library_store.constants.enums import UserRoleEnum
from library_store.custom_exceptions import UserNotAuthorizedException, InvalidMemberIdException, \
    MemberUserNameAlreadyExistsException
from library_store.interactors.permission_class import PermissionMixin
from library_store.interactors.storage_interface import StorageInterface


class MemberCRUDInteractor(PermissionMixin):

    def __init__(self, storage: StorageInterface):
        self.storage = storage

    def add_member(self, user_id: int, member_details: Dict):
        self._validate_is_user_librarian(user_id)
        self._validate_is_username_already_exists(
            username=member_details["username"])

        password = member_details["password"]
        if not password:
            password = DEFAULT_PASSWORD
        member_details["password"] = make_password(password)

        member_id = self.storage.create_auth_user(member_details)
        member_details["member_id"] = member_id

        role = member_details["role"]
        if not role:
            member_details["role"] = UserRoleEnum.member.value

        self.storage.add_member(member_details)

        return member_id

    def get_all_users(self, user_id: int) -> List[Dict]:
        from library_store.constants.enums import UserRoleEnum

        self._validate_is_user_librarian(user_id)

        roles = [UserRoleEnum.member.value, UserRoleEnum.librarian.value]
        members = self.storage.get_all_users_details(roles=roles)
        return members

    def update_member_details(
            self, user_id: int, member_id: int, member_details: Dict):
        self._validate_is_user_librarian(user_id)
        self._validate_is_member_exists(member_id)
        username = member_details["username"]
        if username:
            self._validate_is_username_already_exists(username=username)
        else:
            member_details["username"] = None

        password = member_details["password"]
        if password:
            member_details["password"] = password
        else:
            member_details["password"] = None

        self.storage.update_auth_member_details(
            member_id=member_id, member_details=member_details)

        self.storage.update_member_details(
            member_id=member_id, member_details=member_details)

    def remove_member(self, user_id: int, member_id: int):
        self._validate_is_user_librarian(user_id)
        self._validate_is_member_exists(member_id)

        self.storage.remove_member(member_id=member_id)

    def _validate_is_user_librarian(self, user_id: int):
        is_librarian = self.is_librarian(user_id)
        if not is_librarian:
            raise UserNotAuthorizedException()

    def _validate_is_member_exists(self, member_id: int):
        is_user_exists = self.storage.is_user_exists(user_id=member_id)
        if not is_user_exists:
            raise InvalidMemberIdException()

    def _validate_is_username_already_exists(self, username: str):
        is_name_exists = self.storage.is_user_name_exists(username)
        if is_name_exists:
            raise MemberUserNameAlreadyExistsException()
