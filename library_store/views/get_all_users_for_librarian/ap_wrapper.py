import json

from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView


class GetAllUsersForLibrarianAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user_id = request.user.id

        response = self.get_all_users_for_librarian(user_id)

        return response

    @staticmethod
    def get_all_users_for_librarian(user_id: int):
        from library_store.storages.storage_implementation import StorageImplementation
        from library_store.custom_exceptions import UserNotAuthorizedException
        from library_store.interactors.member_crud_interactor import MemberCRUDInteractor

        storage = StorageImplementation()
        interactor = MemberCRUDInteractor(storage=storage)

        try:
            users_details = interactor.get_all_users(user_id=user_id)
            response = {"users_details": users_details}
            status = 200
        except UserNotAuthorizedException:
            response = {"message": "UnAuthorised"}
            status = 403

        response = json.dumps(response)

        return HttpResponse(content=response, status=status)
