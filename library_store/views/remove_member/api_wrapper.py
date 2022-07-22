import json

from django.http import HttpResponse
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from library_store.custom_exceptions import UserNotAuthorizedException, InvalidMemberIdException


class RemoveMemberAPI(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args,  **kwargs):
        user_id = request.user.id
        member_id = kwargs["member_id"]

        response = self.remove_user_wrapper(
            user_id=user_id, member_id=member_id)
        return response

    @staticmethod
    def remove_user_wrapper(user_id: int, member_id: int):
        from library_store.storages.storage_implementation import StorageImplementation
        from library_store.interactors.member_crud_interactor import MemberCRUDInteractor

        storage = StorageImplementation()
        interactor = MemberCRUDInteractor(storage=storage)
        try:
            interactor.remove_member(user_id=user_id, member_id=member_id)
            response = {"message": "remove successful"}
            status = 200
        except UserNotAuthorizedException:
            response = {"message": "UnAuthorized"}
            status = 401
        except InvalidMemberIdException:
            response = {"message": "Invalid Member Id"}
            status = 404

        response = json.dumps(response)

        return HttpResponse(content=response, status=status)
