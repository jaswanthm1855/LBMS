import abc
from typing import Dict


class StorageInterface:

    @abc.abstractmethod
    def register_user_details(self, user_details: Dict):
        pass
