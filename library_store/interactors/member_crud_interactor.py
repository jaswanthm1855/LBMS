from typing import Dict

from library_store.interactors.storage_interface import StorageInterface


class MemberCRUDInteractor:

    def __init__(self, storage: StorageInterface):
        self.storage = storage

    def get_all_users(self):
        from library_store.constants.enums import UserRoleEnum
        roles = [UserRoleEnum.member.value]
        members = self.storage.get_all_users_details(roles=roles)
        return members

    def update_member_details(self, member_details: Dict):
        self.storage.update_member_details(member_details)

    def remove_member(self, member_id: str):
        self.storage.remove_member(member_id=member_id)
