import json
from typing import Dict

from django.http import HttpResponse
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from library_store.custom_exceptions import \
    UserNotAuthorizedException, MemberUserNameAlreadyExistsException


class AddMemberAPI(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args,  **kwargs):
        user_id = request.user.id
        request_data = request.data
        member_details = {
            "username": request_data["username"],
            "role": request_data["role"],
            "password": request_data["password"]
        }

        response = self.add_member_wrapper(
            user_id=user_id, member_details=member_details)
        return response

    @staticmethod
    def add_member_wrapper(user_id: int, member_details: Dict):
        from library_store.storages.storage_implementation import StorageImplementation
        from library_store.interactors.member_crud_interactor import MemberCRUDInteractor

        storage = StorageImplementation()
        interactor = MemberCRUDInteractor(storage=storage)
        try:
            member_id = interactor.add_member(user_id=user_id, member_details=member_details)
            response = {"message": "Member added successfully", "member_id": member_id}
            status = 201
        except UserNotAuthorizedException:
            response = {"message": "UnAuthorized"}
            status = 401
        except MemberUserNameAlreadyExistsException:
            response = {"message": "Member username already exists"}
            status = 403

        response = json.dumps(response)

        return HttpResponse(content=response, status=status)
