import json
from typing import Dict

from django.http import HttpResponse
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from library_store.custom_exceptions import UserNotAuthorizedException, InvalidMemberIdException


class UpdateMemberDetailsAPI(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request, *args,  **kwargs):
        user_id = request.user.id
        request_data = request.data
        member_id = kwargs["member_id"]
        member_details = {
            "username": request_data.get("username"),
            "role": request_data.get("role"),
            "password": request_data.get("password")
        }

        response = self.update_user_details_wrapper(
            user_id=user_id, member_id=member_id, member_details=member_details)
        return response

    @staticmethod
    def update_user_details_wrapper(
            user_id: int, member_id: int, member_details: Dict):
        from library_store.storages.storage_implementation import StorageImplementation
        from library_store.interactors.member_crud_interactor import MemberCRUDInteractor

        storage = StorageImplementation()
        interactor = MemberCRUDInteractor(storage=storage)
        try:
            interactor.update_member_details(
                user_id=user_id, member_id=member_id,
                member_details=member_details)
            response = {"message": "update successful"}
            status = 200
        except UserNotAuthorizedException:
            response = {"message": "UnAuthorized"}
            status = 401
        except InvalidMemberIdException:
            response = {"message": "Invalid Member Id"}
            status = 404

        response = json.dumps(response)

        return HttpResponse(content=response, status=status)
