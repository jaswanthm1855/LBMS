from library_store.constants.enums import UserRoleEnum


class PermissionMixin:

    def is_library_member(self, user_id: int) -> bool:
        user_role = self.storage.get_user_role(user_id=user_id)
        if user_role == UserRoleEnum.member.value:
            return True
        return False

    def is_librarian(self, user_id: int) -> bool:
        user_role = self.storage.get_user_role(user_id=user_id)
        if user_role == UserRoleEnum.librarian.value:
            return True
        return False
