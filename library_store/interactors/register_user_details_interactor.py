from typing import Dict

from library_store.interactors.storage_interface import StorageInterface


class RegisterUserDetailsInteractor:

    def __init__(self, storage: StorageInterface):
        self.storage = storage

    def register_user_details_wrapper(self, user_profile_details: Dict):
        self.register_user_details(user_profile_details)

    def register_user_details(self, user_profile_details: Dict):
        self.storage.register_user_details(user_profile_details)
