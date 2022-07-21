from typing import Dict

from library_store import models
from library_store.interactors.storage_interface import StorageInterface


class StorageImplementation(StorageInterface):

    def register_user_details(self, user_details: Dict):
        models.UserDetails.objects.create(
            user=user_details["user"], role=user_details["role"]
        )
