import json

from django.http import HttpResponse
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from library_store.custom_exceptions import UserHasBorrowedBooksException


class DeleteMemberAPI(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request, *args,  **kwargs):
        user_id = request.user.id

        response = self.delete_member_wrapper(member_id=user_id)
        return response

    @staticmethod
    def delete_member_wrapper(member_id: int):
        from library_store.storages.storage_implementation import StorageImplementation
        from library_store.interactors.delete_member_interactor import DeleteMemberInteractor

        storage = StorageImplementation()
        interactor = DeleteMemberInteractor(storage=storage)
        try:
            interactor.delete_member(member_id=member_id)
            response = {"message": "remove successful"}
            status = 200
        except UserHasBorrowedBooksException:
            response = {"message": "Please return the borrowed books before deleting account"}
            status = 400

        response = json.dumps(response)
        return HttpResponse(content=response, status=status)
